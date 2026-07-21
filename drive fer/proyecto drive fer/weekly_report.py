#!/usr/bin/env python3
"""
Script para generar reporte semanal/rango con filtrado por fecha
Filtra proyectos por rango de Fecha_Entrega
"""

import logging
import sys
from datetime import datetime, timedelta
from menu import select_gmail_account
from modules.auth import GoogleAuth
from modules.drive_manager import DriveManager
from modules.sheets_manager import SheetsManager
from modules.consolidator import Consolidator
from config import Config
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class WeeklyReportGenerator:
    """Genera reportes semanales/por rango de fechas"""
    
    def __init__(self, token_path: str = None):
        """Inicializar el generador"""
        account = select_gmail_account()
        token_path = account.get('token_path')
        
        print(f"\n📧 Usando cuenta: {account['email']} ({account['name']})")
        print("🔐 Autenticando...\n")
        
        auth = GoogleAuth(token_path=token_path)
        self.config = Config
        self.sheets_mgr = SheetsManager(auth)
        self.consolidator = Consolidator()
    
    def get_date_input(self, prompt: str) -> datetime:
        """
        Solicitar fecha al usuario en formato DD/MM/YYYY
        
        Args:
            prompt: Mensaje a mostrar
            
        Returns:
            datetime object
        """
        while True:
            try:
                date_str = input(f"🔹 {prompt}: ").strip()
                # Formato DD/MM/YYYY
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                return date_obj
            except ValueError:
                print("❌ Formato inválido. Usa DD/MM/YYYY (ejemplo: 18/07/2026)")
    
    def get_date_range_interactive(self) -> tuple:
        """
        Obtener rango de fechas interactivamente
        
        Returns:
            Tuple de (fecha_inicio, fecha_fin)
        """
        print("\n" + "="*60)
        print("📅 SELECCIONAR RANGO DE FECHAS")
        print("="*60 + "\n")
        
        print("Opciones rápidas:")
        print("1. Esta semana (Lunes a Domingo)")
        print("2. Próxima semana")
        print("3. Este mes")
        print("4. Próximo mes")
        print("5. Personalizado (Ingresar fechas)\n")
        
        choice = input("🔹 Selecciona opción: ").strip()
        
        today = datetime.now()
        
        if choice == "1":
            # Esta semana
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            return start, end
        
        elif choice == "2":
            # Próxima semana
            start = today - timedelta(days=today.weekday()) + timedelta(days=7)
            end = start + timedelta(days=6)
            return start, end
        
        elif choice == "3":
            # Este mes
            start = today.replace(day=1)
            if today.month == 12:
                end = start.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end = start.replace(month=today.month + 1, day=1) - timedelta(days=1)
            return start, end
        
        elif choice == "4":
            # Próximo mes
            if today.month == 12:
                start = today.replace(year=today.year + 1, month=1, day=1)
                end = start.replace(month=2, day=1) - timedelta(days=1)
            else:
                start = today.replace(month=today.month + 1, day=1)
                end = start.replace(month=today.month + 2, day=1) - timedelta(days=1) if today.month < 11 else start.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            return start, end
        
        elif choice == "5":
            # Personalizado
            print()
            start = self.get_date_input("Ingresa fecha INICIO (DD/MM/YYYY)")
            end = self.get_date_input("Ingresa fecha FIN (DD/MM/YYYY)")
            
            if start > end:
                print("❌ La fecha de inicio debe ser menor que la de fin")
                return self.get_date_range_interactive()
            
            return start, end
        
        else:
            print("❌ Opción no válida")
            return self.get_date_range_interactive()
    
    def filter_by_date_range(self, df: pd.DataFrame, 
                            start_date: datetime, 
                            end_date: datetime) -> pd.DataFrame:
        """
        Filtrar DataFrame por rango de Fecha_Entrega
        
        Args:
            df: DataFrame con datos
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            DataFrame filtrado
        """
        try:
            # Convertir Fecha_Entrega a datetime
            df['Fecha_Entrega_dt'] = pd.to_datetime(
                df['Fecha_Entrega'], 
                format='%d/%m/%Y',
                errors='coerce'
            )
            
            # Filtrar
            filtered = df[
                (df['Fecha_Entrega_dt'] >= start_date) & 
                (df['Fecha_Entrega_dt'] <= end_date)
            ].copy()
            
            # Eliminar columna temporal
            filtered = filtered.drop('Fecha_Entrega_dt', axis=1)
            
            return filtered
        except Exception as e:
            logger.error(f"Error al filtrar por fecha: {e}")
            return df
    
    def read_all_departments(self) -> dict:
        """
        Leer datos de todos los departamentos
        
        Returns:
            Dictionary con datos por departamento
        """
        department_data = {}
        
        for dept_name in self.config.DEPARTMENTS_LIST:
            dept_name = dept_name.strip()
            sheet_id = self.config.DEPARTMENTS[dept_name].get('sheet_id')
            
            if not sheet_id:
                logger.warning(f"No sheet ID for {dept_name}, skipping...")
                continue
            
            try:
                # Usar el nombre de la hoja sin acentos
                sheet_name = dept_name.replace('á', 'a').replace('é', 'e')
                data = self.sheets_mgr.read_data(sheet_id, f"'{dept_name}'!A:G")
                department_data[dept_name] = data
                logger.info(f"Read {len(data)} rows from {dept_name}")
            except Exception as e:
                logger.error(f"Error reading {dept_name}: {str(e)}")
                continue
        
        return department_data
    
    def generate_filtered_report(self):
        """Generar reporte filtrado por rango de fechas"""
        
        print("\n" + "="*60)
        print("📊 GENERADOR DE REPORTE SEMANAL/RANGO")
        print("="*60 + "\n")
        
        # Obtener rango de fechas
        start_date, end_date = self.get_date_range_interactive()
        
        print(f"\n📅 Rango seleccionado:")
        print(f"   Desde: {start_date.strftime('%d/%m/%Y')}")
        print(f"   Hasta: {end_date.strftime('%d/%m/%Y')}")
        print(f"   Total: {(end_date - start_date).days + 1} días\n")
        
        print("📖 Leyendo datos de departamentos...\n")
        
        # Leer datos
        department_data = self.read_all_departments()
        
        if not department_data:
            print("❌ No data found")
            return
        
        # Consolidar
        print("🔄 Consolidando datos...\n")
        consolidated = self.consolidator.consolidate_all_departments(
            department_data,
            self.config.DEPARTMENT_SHEET_HEADERS
        )
        
        if consolidated.empty:
            print("❌ No consolidated data")
            return
        
        # Filtrar por fecha
        print("🔍 Aplicando filtro de fechas...\n")
        filtered = self.filter_by_date_range(consolidated, start_date, end_date)
        
        # Mostrar resultados
        print("="*60)
        print("✅ RESULTADOS DEL REPORTE")
        print("="*60 + "\n")
        
        if filtered.empty:
            print("⚠️ No projects found in the selected date range")
            return
        
        print(f"📋 Total de proyectos: {len(filtered)}\n")
        
        # Agrupar por departamento
        by_dept = filtered.groupby('Departamento')
        
        for dept, data in by_dept:
            print(f"\n{'='*60}")
            print(f"📂 {dept.upper()}: {len(data)} proyectos")
            print(f"{'='*60}\n")
            
            for idx, row in data.iterrows():
                print(f"🔹 {row['ID_Proyecto']} - {row['Cliente']}")
                print(f"   Descripción: {row['Descripcion']}")
                print(f"   Entrega: {row['Fecha_Entrega']} | Estado: {row['Estado']}")
                print(f"   Responsable: {row['Responsable']}\n")
        
        # Guardar en CSV
        csv_file = f"reporte_{start_date.strftime('%d%m%Y')}_a_{end_date.strftime('%d%m%Y')}.csv"
        filtered.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"✅ Reporte guardado: {csv_file}\n")
        
        # Resumen por estado
        print("\n" + "="*60)
        print("📊 RESUMEN POR ESTADO")
        print("="*60 + "\n")
        
        estado_counts = filtered['Estado'].value_counts()
        for estado, count in estado_counts.items():
            print(f"  {estado}: {count} proyectos")
        
        print("\n")


def main():
    """Punto de entrada"""
    try:
        generator = WeeklyReportGenerator()
        generator.generate_filtered_report()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
