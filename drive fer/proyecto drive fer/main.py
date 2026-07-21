"""
Main Script - Project Scheduler
Orchestrates the complete workflow for project planning system
"""

import logging
import sys
import os
import json
from datetime import datetime, timedelta
from config import Config
from menu import select_gmail_account
from modules.auth import GoogleAuth
from modules.drive_manager import DriveManager
from modules.sheets_manager import SheetsManager
from modules.scheduler import Scheduler
from modules.consolidator import Consolidator
from modules.notifier import Notifier
from google.oauth2.credentials import Credentials
import pandas as pd

logger = logging.getLogger(__name__)


class ProjectSchedulerApp:
    """Main application for project scheduling"""
    
    def __init__(self, token_path: str = None):
        """
        Initialize the application
        
        Args:
            token_path: Path to OAuth token file (optional)
        """
        self.config = Config
        
        # Load cached IDs from previous runs
        self.config.load_cached_ids()
        
        # Use provided token path or prompt user to select account
        if token_path:
            logger.info(f"Using provided token: {token_path}")
            auth_token = token_path
        else:
            # Display interactive menu
            account = select_gmail_account()
            auth_token = account.get('token_path')
            logger.info(f"Selected account: {account['email']} ({account['name']})")
            logger.info(f"Using token: {auth_token}")
        
        self.auth = GoogleAuth(token_path=auth_token)
        self.drive_mgr = DriveManager(self.auth)
        self.sheets_mgr = SheetsManager(self.auth)
        self.scheduler = Scheduler(self.config.ALERT_DAYS_THRESHOLD)
        self.consolidator = Consolidator()
        self.notifier = Notifier(
            self.config.LOG_FILE_PATH,
            self.config.SMTP_SERVER,
            self.config.SMTP_PORT,
            self.config.SMTP_USER,
            self.config.SMTP_PASSWORD,
            self.config.ALERT_RECIPIENTS
        )
        
        logger.info("Application initialized successfully")
    
    def setup_folder_structure(self) -> str:
        """
        Create or get root folder and set up department folders
        
        Returns:
            Root folder ID
        """
        logger.info("=" * 70)
        logger.info("STEP 1: Setting up folder structure")
        logger.info("=" * 70)
        
        # Create/get root folder
        root_folder_id = self.config.DRIVE_ROOT_FOLDER_ID
        if not root_folder_id:
            root_folder_id = self.drive_mgr.get_or_create_folder(
                self.config.DRIVE_ROOT_FOLDER_NAME
            )
            logger.info(f"Root folder created with ID: {root_folder_id}")
        else:
            logger.info(f"Using existing root folder: {root_folder_id}")
        
        # Create/get department folders
        for dept_name in self.config.DEPARTMENTS_LIST:
            dept_name = dept_name.strip()
            dept_folder_id = self.drive_mgr.get_or_create_folder(dept_name, root_folder_id)
            clients_folder_id = self.drive_mgr.get_or_create_folder('Clientes', dept_folder_id)
            
            self.config.DEPARTMENTS[dept_name]['folder_id'] = dept_folder_id
            logger.info(f"{dept_name} department folder: {dept_folder_id}")
            logger.info(f"{dept_name} clients folder: {clients_folder_id}")
        
        # Save root folder ID to config
        self.config.DRIVE_ROOT_FOLDER_ID = root_folder_id
        
        return root_folder_id
    
    def setup_spreadsheets(self, root_folder_id: str):
        """
        Create or get spreadsheets for all departments and master
        
        Args:
            root_folder_id: Root folder ID
        """
        logger.info("")
        logger.info("=" * 70)
        logger.info("STEP 2: Setting up spreadsheets")
        logger.info("=" * 70)
        
        # Create/get spreadsheets for each department
        for dept_name in self.config.DEPARTMENTS_LIST:
            dept_name = dept_name.strip()
            dept_folder_id = self.config.DEPARTMENTS[dept_name]['folder_id']
            sheet_title = f"Cronograma_{dept_name}"
            
            sheet_id = self.sheets_mgr.get_or_create_spreadsheet(sheet_title, dept_folder_id)
            self.config.DEPARTMENTS[dept_name]['sheet_id'] = sheet_id
            
            # Create headers if new sheet
            try:
                self.sheets_mgr.create_headers(
                    sheet_id,
                    dept_name,
                    self.config.DEPARTMENT_SHEET_HEADERS
                )
                logger.info(f"Headers created for {dept_name}")
            except Exception as e:
                logger.warning(f"Headers may already exist for {dept_name}: {str(e)}")
            
            logger.info(f"Spreadsheet for {dept_name}: {sheet_id}")
        
        # Create/get master schedule
        master_title = self.config.MASTER_SCHEDULE_NAME
        master_sheet_id = self.sheets_mgr.get_or_create_spreadsheet(master_title, root_folder_id)
        self.config.SHEET_MAESTRO_ID = master_sheet_id
        
        try:
            self.sheets_mgr.create_headers(
                master_sheet_id,
                master_title,
                self.config.MASTER_SHEET_HEADERS
            )
            logger.info("Headers created for master schedule")
        except Exception as e:
            logger.warning(f"Headers may already exist for master: {str(e)}")
        
        logger.info(f"Master schedule spreadsheet: {master_sheet_id}")
        
        # Save IDs to cache for persistence
        self.config.save_cached_ids()
    
    def _get_first_sheet_name(self, spreadsheet_id: str) -> str:
        """
        Get the first sheet name from a spreadsheet
        
        Args:
            spreadsheet_id: Spreadsheet ID
            
        Returns:
            First sheet name
        """
        try:
            sheets = self.sheets_mgr.get_sheet_names(spreadsheet_id)
            if sheets:
                return sheets[0]
        except Exception as e:
            logger.warning(f"Could not get sheet names: {e}")
        
        return 'Sheet1'  # Fallback
    
    def consolidate_schedules(self):
        """Consolidate data from all department schedules"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("STEP 3: Consolidating schedules")
        logger.info("=" * 70)
        
        department_data = {}
        
        # Read data from all departments
        for dept_name in self.config.DEPARTMENTS_LIST:
            dept_name = dept_name.strip()
            sheet_id = self.config.DEPARTMENTS[dept_name].get('sheet_id')
            
            if not sheet_id:
                logger.warning(f"No sheet ID for {dept_name}, skipping...")
                continue
            
            # Read all data from the sheet
            try:
                # Get actual sheet name from the spreadsheet
                actual_sheet_name = self._get_first_sheet_name(sheet_id)
                # Read all columns: A:K (11 columns for: COTIZACIÓN, Última Rev., Cliente, Rubro de Cotización, Vendedor, Fecha de pedido, Fecha primer envío, Fecha último estado, Diferencia de días, Estado, Descripción)
                range_ = self.sheets_mgr._build_range(actual_sheet_name, "A:K")
                data = self.sheets_mgr.read_data(sheet_id, range_)
                department_data[dept_name] = data
                logger.info(f"Read {len(data)} rows from {dept_name}")
            except Exception as e:
                logger.error(f"Error reading {dept_name}: {str(e)}")
                continue
        
        if not department_data:
            logger.warning("No department data available for consolidation")
            return None
        
        # Consolidate using consolidator
        consolidated_df = self.consolidator.consolidate_all_departments(
            department_data,
            self.config.DEPARTMENT_SHEET_HEADERS
        )
        
        if consolidated_df is None or consolidated_df.empty:
            logger.warning("Consolidated DataFrame is empty")
            return None
        
        # Validate data
        is_valid, errors = self.consolidator.validate_data_integrity(
            consolidated_df,
            self.config.DEPARTMENT_SHEET_HEADERS
        )
        
        if not is_valid:
            logger.warning(f"Data validation issues: {errors}")
        
        # Write to master schedule
        master_sheet_id = self.config.SHEET_MAESTRO_ID
        if master_sheet_id:
            # Convert DataFrame to sheet format
            sheet_data = self.consolidator.dataframe_to_sheet_data(consolidated_df)
            
            # Get actual sheet name
            actual_sheet_name = self._get_first_sheet_name(master_sheet_id)
            
            # Clear existing data (keep headers)
            try:
                range_ = self.sheets_mgr._build_range(actual_sheet_name, "A2:H")
                self.sheets_mgr.clear_sheet(master_sheet_id, range_)
            except Exception as e:
                logger.warning(f"Could not clear master sheet: {str(e)}")
            
            # Write new data
            if sheet_data and len(sheet_data) > 1:  # More than just headers
                try:
                    range_ = self.sheets_mgr._build_range(actual_sheet_name, "A1")
                    self.sheets_mgr.write_data(
                        master_sheet_id,
                        range_,
                        sheet_data
                    )
                    logger.info(f"Consolidated {len(consolidated_df)} projects to master schedule")
                except Exception as e:
                    logger.error(f"Error writing to master: {str(e)}")
        
        # Generate summaries
        try:
            summaries = self.consolidator.get_all_summaries(consolidated_df)
            for dept, summary in summaries.items():
                logger.info(f"{dept}: {summary}")
        except Exception as e:
            logger.warning(f"Could not generate summaries: {str(e)}")
        
        return consolidated_df
    
    def evaluate_alerts(self, consolidated_df=None):
        """Evaluate and log alerts for deadline issues"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("STEP 4: Evaluating alerts")
        logger.info("=" * 70)
        
        projects = []
        
        if consolidated_df is not None:
            projects = consolidated_df.to_dict('records')
        else:
            # Read from master if no DataFrame provided
            master_sheet_id = self.config.SHEET_MAESTRO_ID
            if not master_sheet_id:
                logger.warning("No master sheet ID, cannot evaluate alerts")
                return [], []
            
            try:
                # Get actual sheet name
                actual_sheet_name = self._get_first_sheet_name(master_sheet_id)
                range_ = self.sheets_mgr._build_range(actual_sheet_name, "A:H")
                data = self.sheets_mgr.read_data(
                    master_sheet_id,
                    range_
                )
                
                if len(data) <= 1:
                    logger.info("No project data to evaluate")
                    return [], []
                
                headers = data[0]
                projects = [dict(zip(headers, row)) for row in data[1:]]
            except Exception as e:
                logger.error(f"Error reading master for alerts: {str(e)}")
                return [], []
        
        if not projects:
            logger.info("No projects to evaluate")
            return [], []
        
        # Evaluate alerts
        try:
            overdue, approaching = self.scheduler.evaluate_all_alerts(projects)
        except Exception as e:
            logger.error(f"Error evaluating alerts: {str(e)}")
            return [], []
        
        # Log alerts
        total_logged = 0
        try:
            total_logged += self.notifier.log_alerts_batch(overdue)
            total_logged += self.notifier.log_alerts_batch(approaching)
            logger.info(f"Total alerts logged: {total_logged}")
        except Exception as e:
            logger.error(f"Error logging alerts: {str(e)}")
        
        # Generate summary
        try:
            summary_text = self.scheduler.generate_alert_summary(overdue, approaching)
            logger.info(summary_text)
        except Exception as e:
            logger.warning(f"Could not generate alert summary: {str(e)}")
        
        # Send email if configured
        if self.config.ALERT_RECIPIENTS:
            try:
                self.notifier.send_alerts_summary(overdue, approaching)
            except Exception as e:
                logger.error(f"Error sending email alerts: {str(e)}")
        
        return overdue, approaching
    
    def get_date_range_for_report(self, report_type: str) -> tuple:
        """
        Get date range based on report type
        
        Args:
            report_type: 'dia', 'semana', 'mes', or 'global'
            
        Returns:
            Tuple of (start_date, end_date) or None for global
        """
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if report_type == "dia":
            # Entire day: 00:00:00 to 23:59:59
            return today, today.replace(hour=23, minute=59, second=59)
        
        elif report_type == "semana":
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            end = end.replace(hour=23, minute=59, second=59)
            return start, end
        
        elif report_type == "mes":
            start = today.replace(day=1)
            if today.month == 12:
                end = start.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end = start.replace(month=today.month + 1, day=1) - timedelta(days=1)
            end = end.replace(hour=23, minute=59, second=59)
            return start, end
        
        else:  # global
            return None, None
    
    def filter_dataframe_by_dates(self, df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
        """
        Filter DataFrame by date range
        
        Args:
            df: DataFrame to filter
            start_date: Start date or None
            end_date: End date or None
            
        Returns:
            Filtered DataFrame
        """
        if start_date is None or end_date is None:
            return df
        
        try:
            # Try parsing dates - compatible with multiple pandas versions
            df_copy = df.copy()
            
            # Try different approaches for different pandas versions
            try:
                # Try with infer_datetime_format (newer pandas)
                df_copy['Fecha_Entrega_dt'] = pd.to_datetime(
                    df_copy['Fecha_Entrega'],
                    infer_datetime_format=True,
                    errors='coerce'
                )
            except TypeError:
                # Fall back to format='mixed' (pandas 2.0+)
                try:
                    df_copy['Fecha_Entrega_dt'] = pd.to_datetime(
                        df_copy['Fecha_Entrega'],
                        format='mixed',
                        errors='coerce'
                    )
                except TypeError:
                    # Final fallback - just try without extra parameters
                    df_copy['Fecha_Entrega_dt'] = pd.to_datetime(
                        df_copy['Fecha_Entrega'],
                        errors='coerce'
                    )
            
            # Filter by date range AND exclude NaT (null) values
            filtered = df_copy[
                (df_copy['Fecha_Entrega_dt'].notna()) &  # Exclude nulls
                (df_copy['Fecha_Entrega_dt'] >= start_date) &
                (df_copy['Fecha_Entrega_dt'] <= end_date)
            ].copy()
            
            filtered = filtered.drop('Fecha_Entrega_dt', axis=1)
            logger.info(f"Filtered {len(df_copy)} rows to {len(filtered)} rows for date range {start_date} to {end_date}")
            return filtered
            
        except Exception as e:
            logger.warning(f"Error filtering by date: {e}")
            logger.warning(f"Returning unfiltered dataframe with {len(df)} rows")
            return df
    
    def generate_report(self, report_type: str = "semana"):
        """
        Generate a report and create it as a new Google Sheet in Drive
        
        Args:
            report_type: 'dia', 'semana', 'mes', or 'global'
        """
        logger.info("")
        logger.info("=" * 70)
        logger.info(f"REPORTE: {report_type.upper()}")
        logger.info("=" * 70)
        
        # Check if IDs are cached, if not run setup first
        if not self.config.SHEET_MAESTRO_ID or not any(
            self.config.DEPARTMENTS[dept].get('sheet_id') 
            for dept in self.config.DEPARTMENTS_LIST
        ):
            logger.info("No cached IDs found, running setup...")
            print("\n🔧 Configurando estructura de carpetas y hojas...\n")
            root_folder_id = self.setup_folder_structure()
            self.setup_spreadsheets(root_folder_id)
        
        try:
            print(f"\n📖 Leyendo datos de departamentos...\n")
            
            # Read data from all departments
            department_data = {}
            
            for dept_name in self.config.DEPARTMENTS_LIST:
                dept_name = dept_name.strip()
                sheet_id = self.config.DEPARTMENTS[dept_name].get('sheet_id')
                
                if not sheet_id:
                    logger.warning(f"No sheet ID for {dept_name}, skipping...")
                    print(f"⚠️ Sin datos para {dept_name}")
                    continue
                
                try:
                    # Read data from department sheet
                    # Get actual sheet name from the spreadsheet
                    actual_sheet_name = self._get_first_sheet_name(sheet_id)
                    # Read all columns A:K (11 columns for all departmental data)
                    range_ = self.sheets_mgr._build_range(actual_sheet_name, "A:K")
                    data = self.sheets_mgr.read_data(sheet_id, range_)
                    department_data[dept_name] = data
                    logger.info(f"Read {len(data)} rows from {dept_name}")
                    print(f"✓ {dept_name}: {len(data)} filas")
                except Exception as e:
                    logger.error(f"Error reading {dept_name}: {str(e)}")
                    print(f"❌ Error leyendo {dept_name}: {e}")
                    continue
            
            if not department_data:
                print("❌ No hay datos en los departamentos")
                return
            
            # Consolidate data
            print(f"\n🔄 Consolidando datos...\n")
            consolidated_df = self.consolidator.consolidate_all_departments(
                department_data,
                self.config.DEPARTMENT_SHEET_HEADERS
            )
            
            if consolidated_df.empty:
                print("❌ No hay datos consolidados")
                return
            
            # Get date range
            start_date, end_date = self.get_date_range_for_report(report_type)
            
            # Filter by dates if not global
            if start_date is not None:
                filtered_df = self.filter_dataframe_by_dates(consolidated_df, start_date, end_date)
                date_range_str = f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"
                report_name = f"Reporte_{report_type.capitalize()}_{start_date.strftime('%d_%m_%Y')}"
            else:
                filtered_df = consolidated_df
                date_range_str = "Todo el período"
                report_name = f"Reporte_Global_{datetime.now().strftime('%d_%m_%Y')}"
            
            if filtered_df.empty:
                print(f"⚠️ No hay proyectos para el rango: {date_range_str}")
                return
            
            # Get root folder for storing reports
            root_folder_id = self.config.DRIVE_ROOT_FOLDER_ID
            if not root_folder_id:
                # Use the one from setup
                try:
                    root_folder_id = self.drive_mgr.get_or_create_folder(
                        self.config.DRIVE_ROOT_FOLDER_NAME
                    )
                except Exception as e:
                    logger.error(f"Could not get root folder: {e}")
                    print(f"❌ No se pudo acceder a la carpeta raíz: {e}")
                    return
            
            # Create new spreadsheet for the report
            print(f"📝 Creando Google Sheet del reporte...\n")
            try:
                report_sheet_id = self.sheets_mgr.get_or_create_spreadsheet(
                    report_name,
                    root_folder_id
                )
                logger.info(f"Created report sheet: {report_sheet_id}")
            except Exception as e:
                logger.error(f"Error creating report sheet: {e}")
                print(f"❌ Error creando el reporte en Drive: {e}")
                return
            
            # Write headers
            try:
                self.sheets_mgr.create_headers(
                    report_sheet_id,
                    report_name,
                    self.config.MASTER_SHEET_HEADERS
                )
                logger.info(f"Headers created for report sheet")
                
                # Clear any existing data from the sheet (rows A2:H onwards)
                try:
                    actual_sheet_name = self._get_first_sheet_name(report_sheet_id)
                    clear_range = self.sheets_mgr._build_range(actual_sheet_name, "A2:H")
                    self.sheets_mgr.clear_data(report_sheet_id, clear_range)
                    logger.info(f"Cleared existing data from {actual_sheet_name}")
                except Exception as e:
                    logger.info(f"No existing data to clear (first report): {str(e)}")
                    
            except Exception as e:
                logger.warning(f"Headers may already exist: {str(e)}")
            
            # Convert DataFrame to sheet format
            sheet_data = self.consolidator.dataframe_to_sheet_data(filtered_df)
            
            # Write data to sheet
            try:
                # Get actual sheet name (should match report_name after create_headers)
                actual_sheet_name = self._get_first_sheet_name(report_sheet_id)
                range_ = self.sheets_mgr._build_range(actual_sheet_name, "A1")
                self.sheets_mgr.write_data(
                    report_sheet_id,
                    range_,
                    sheet_data
                )
                logger.info(f"Wrote {len(filtered_df)} projects to report sheet")
            except Exception as e:
                logger.error(f"Error writing report data: {e}")
                print(f"❌ Error escribiendo datos: {e}")
                return
            
            # Display report summary
            print("\n" + "=" * 70)
            print(f"✅ REPORTE {report_type.upper()} CREADO EN DRIVE")
            print("=" * 70)
            print(f"📅 Rango: {date_range_str}\n")
            print(f"📋 Total de proyectos: {len(filtered_df)}\n")
            
            # Group by department
            if 'Departamento' in filtered_df.columns:
                by_dept = filtered_df.groupby('Departamento')
                
                for dept, data_dept in by_dept:
                    print(f"  📂 {dept}: {len(data_dept)} proyectos")
            
            # Summary by status
            print(f"\n📊 RESUMEN POR ESTADO:")
            if 'Estado' in filtered_df.columns:
                estado_counts = filtered_df['Estado'].value_counts()
                for estado, count in estado_counts.items():
                    print(f"  {estado}: {count} proyectos")
            
            # Generate Drive link
            drive_link = f"https://docs.google.com/spreadsheets/d/{report_sheet_id}/edit"
            print(f"\n🔗 ENLACE AL REPORTE:")
            print(f"   {drive_link}")
            
            print(f"\n✅ Reporte creado exitosamente en Google Drive\n")
            
            logger.info(f"Report successfully created: {drive_link}")
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}", exc_info=True)
            print(f"❌ Error al generar reporte: {e}")
    
    def show_report_menu(self):
        """Show interactive report menu"""
        while True:
            print("\n" + "=" * 70)
            print("📊 MENÚ DE REPORTES")
            print("=" * 70 + "\n")
            
            print("Selecciona el tipo de reporte:\n")
            print("  1. 📅 Reporte del día")
            print("  2. 📆 Reporte de la semana")
            print("  3. 📊 Reporte del mes")
            print("  4. 🌍 Reporte global (todos los proyectos)")
            print("  5. ↩️ Volver al menú principal\n")
            
            choice = input("🔹 Selecciona opción (1-5): ").strip()
            
            if choice == "1":
                self.generate_report("dia")
            elif choice == "2":
                self.generate_report("semana")
            elif choice == "3":
                self.generate_report("mes")
            elif choice == "4":
                self.generate_report("global")
            elif choice == "5":
                break
            else:
                print("❌ Opción no válida")
            
            input("\n🔹 Presiona Enter para continuar...")
    
    def run_full_cycle(self):
        """Execute the complete project scheduler cycle"""
        logger.info("")
        logger.info("╔" + "=" * 68 + "╗")
        logger.info("║" + " PROJECT SCHEDULER - FULL EXECUTION CYCLE ".center(68) + "║")
        logger.info("╚" + "=" * 68 + "╝")
        logger.info("")
        
        try:
            # Step 1: Setup folder structure
            root_folder_id = self.setup_folder_structure()
            
            # Step 2: Setup spreadsheets
            self.setup_spreadsheets(root_folder_id)
            
            # Step 3: Consolidate schedules
            consolidated_df = self.consolidate_schedules()
            
            # Step 4: Evaluate alerts
            if consolidated_df is not None:
                overdue, approaching = self.evaluate_alerts(consolidated_df)
            
            # Log execution summary
            execution_summary = {
                'Status': 'SUCCESS',
                'Root Folder': root_folder_id,
                'Departments': len(self.config.DEPARTMENTS),
                'Master Schedule': self.config.SHEET_MAESTRO_ID
            }
            self.notifier.log_execution_summary(execution_summary)
            
            logger.info("")
            logger.info("✓ Execution completed successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Execution failed: {str(e)}", exc_info=True)
            
            execution_summary = {
                'Status': 'FAILED',
                'Error': str(e)
            }
            self.notifier.log_execution_summary(execution_summary)
            
            return False


def main(token_path: str = None):
    """
    Main entry point with interactive menu
    
    Args:
        token_path: Optional path to OAuth token file (skips menu if provided)
    """
    try:
        app = ProjectSchedulerApp(token_path=token_path)
        
        # Show interactive menu if no specific action provided
        if not token_path:
            while True:
                print("\n" + "=" * 70)
                print("🚀 PROJECT SCHEDULER - MENÚ PRINCIPAL")
                print("=" * 70 + "\n")
                
                print("Opciones disponibles:\n")
                print("  1. ▶️  Ejecutar ciclo completo")
                print("  2. 📊 Generar reporte")
                print("  3. ❌ Salir\n")
                
                choice = input("🔹 Selecciona opción (1-3): ").strip()
                
                if choice == "1":
                    print("\n⏳ Ejecutando ciclo completo...\n")
                    success = app.run_full_cycle()
                    if success:
                        print("\n✓ Ciclo completado exitosamente")
                    else:
                        print("\n✗ El ciclo falló, revisa los logs")
                
                elif choice == "2":
                    app.show_report_menu()
                
                elif choice == "3":
                    print("\n👋 ¡Hasta luego!\n")
                    sys.exit(0)
                
                else:
                    print("❌ Opción no válida")
        else:
            # If token provided, just run full cycle
            print("⏳ Ejecutando ciclo completo...\n")
            success = app.run_full_cycle()
            
            if success:
                print("\n✓ Project Scheduler executed successfully")
                print(f"✓ View detailed logs at: {Config.LOG_FILE}")
                print(f"✓ View alerts at: {Config.LOG_FILE_PATH}")
                sys.exit(0)
            else:
                print("\n✗ Project Scheduler execution failed")
                print(f"✗ Check logs at: {Config.LOG_FILE}")
                sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    # Check if token path provided as command line argument
    token_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if token_path:
        print(f"📧 Using token from: {token_path}")
    else:
        print("📧 No token provided, showing account selector...")
    
    main(token_path=token_path)