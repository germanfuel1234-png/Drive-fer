#!/usr/bin/env python3
"""
Script para leer Excel locales, mapear columnas y generar reporte semanal
Convierte la estructura de Cotizaciones a formato de Cronograma
"""

import logging
import sys
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from modules.consolidator import Consolidator
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class ExcelImporter:
    """Lee Excel locales y mapea a formato de cronograma"""
    
    def __init__(self, excel_folder: str = "./logs/excel"):
        """
        Inicializar importador
        
        Args:
            excel_folder: Carpeta con los Excel locales
        """
        self.excel_folder = Path(excel_folder)
        self.consolidator = Consolidator()
        self.config = Config
        
        if not self.excel_folder.exists():
            raise FileNotFoundError(f"Carpeta {excel_folder} no encontrada")
        
        logger.info(f"ExcelImporter inicializado: {self.excel_folder}")
    
    def read_excel_files(self) -> dict:
        """
        Leer todos los Excel de la carpeta
        
        Returns:
            Dictionary {nombre_archivo: DataFrame}
        """
        data = {}
        
        for excel_file in self.excel_folder.glob("*.xlsx"):
            try:
                logger.info(f"Leyendo: {excel_file.name}")
                df = pd.read_excel(excel_file, sheet_name=0)
                data[excel_file.stem] = df
                logger.info(f"  → {len(df)} filas leídas")
            except Exception as e:
                logger.error(f"Error leyendo {excel_file.name}: {e}")
                continue
        
        return data
    
    def process_all_excels(self) -> pd.DataFrame:
        """
        Leer todos los Excel, mapear columnas y consolidar
        
        Returns:
            DataFrame consolidado
        """
        # Leer todos los Excel
        all_data = self.read_excel_files()
        
        if not all_data:
            logger.warning("No Excel files found")
            return pd.DataFrame()
        
        # Mapear cada Excel
        dataframes = []
        for filename, df in all_data.items():
            logger.info(f"Mapeando columnas: {filename}")
            df_mapped = self.consolidator.map_excel_columns(df)
            
            if not df_mapped.empty:
                dataframes.append(df_mapped)
        
        if not dataframes:
            logger.warning("No data after mapping")
            return pd.DataFrame()
        
        # Consolidar todos
        consolidated = pd.concat(dataframes, ignore_index=True)
        logger.info(f"Total consolidado: {len(consolidated)} proyectos")
        
        return consolidated
    
    def filter_by_date_range(self, df: pd.DataFrame, 
                            start_date: datetime, 
                            end_date: datetime) -> pd.DataFrame:
        """
        Filtrar por rango de Fecha_Entrega
        
        Args:
            df: DataFrame con datos
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            DataFrame filtrado
        """
        try:
            # Convertir a datetime
            df['Fecha_Entrega_dt'] = pd.to_datetime(
                df['Fecha_Entrega'], 
                format='%Y-%m-%d',
                errors='coerce'
            )
            
            # Si el formato no funciona, intentar con el otro
            mask = df['Fecha_Entrega_dt'].isna()
            if mask.any():
                df.loc[mask, 'Fecha_Entrega_dt'] = pd.to_datetime(
                    df.loc[mask, 'Fecha_Entrega'],
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
            
            logger.info(f"Filtrados: {len(filtered)} proyectos en rango {start_date.date()} a {end_date.date()}")
            return filtered
            
        except Exception as e:
            logger.error(f"Error al filtrar por fecha: {e}")
            return df
    
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
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            return start, end
        
        elif choice == "2":
            start = today - timedelta(days=today.weekday()) + timedelta(days=7)
            end = start + timedelta(days=6)
            return start, end
        
        elif choice == "3":
            start = today.replace(day=1)
            if today.month == 12:
                end = start.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end = start.replace(month=today.month + 1, day=1) - timedelta(days=1)
            return start, end
        
        elif choice == "4":
            if today.month == 12:
                start = today.replace(year=today.year + 1, month=1, day=1)
                end = start.replace(month=2, day=1) - timedelta(days=1)
            else:
                start = today.replace(month=today.month + 1, day=1)
                if today.month < 11:
                    end = start.replace(month=today.month + 2, day=1) - timedelta(days=1)
                else:
                    end = start.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            return start, end
        
        else:
            print("❌ Opción no válida")
            return self.get_date_range_interactive()
    
    def generate_report(self, filter_dates: bool = True):
        """
        Generar reporte de Excel locales
        
        Args:
            filter_dates: Si True, pide rango de fechas
        """
        print("\n" + "="*60)
        print("📊 REPORTE SEMANAL - LECTURA DE EXCEL LOCALES")
        print("="*60 + "\n")
        
        # Procesar Excel
        print("🔍 Leyendo y procesando Excel...\n")
        consolidated = self.process_all_excels()
        
        if consolidated.empty:
            print("❌ No hay datos para procesar")
            return
        
        # Filtrar por fechas
        if filter_dates:
            start_date, end_date = self.get_date_range_interactive()
            print(f"\n📅 Rango seleccionado:")
            print(f"   Desde: {start_date.strftime('%d/%m/%Y')}")
            print(f"   Hasta: {end_date.strftime('%d/%m/%Y')}")
            print(f"   Total: {(end_date - start_date).days + 1} días\n")
            
            filtered = self.filter_by_date_range(consolidated, start_date, end_date)
        else:
            filtered = consolidated
        
        if filtered.empty:
            print("⚠️ No hay proyectos en el rango seleccionado")
            return
        
        # Mostrar resultados
        print("="*60)
        print("✅ RESULTADOS DEL REPORTE")
        print("="*60 + "\n")
        
        print(f"📋 Total de proyectos: {len(filtered)}\n")
        
        # Agrupar por departamento
        by_dept = filtered.groupby('Departamento')
        
        for dept, data in by_dept:
            print(f"\n{'='*60}")
            print(f"📂 {dept.upper()}: {len(data)} proyectos")
            print(f"{'='*60}\n")
            
            for idx, row in data.iterrows():
                id_proj = str(row.get('ID_Proyecto', 'N/A'))[:10]
                cliente = str(row.get('Cliente', 'N/A'))[:30]
                fecha = str(row.get('Fecha_Entrega', 'N/A'))
                estado = str(row.get('Estado', 'N/A'))
                resp = str(row.get('Responsable', 'N/A'))[:20]
                
                print(f"🔹 {id_proj} - {cliente}")
                print(f"   Entrega: {fecha} | Estado: {estado}")
                print(f"   Responsable: {resp}\n")
        
        # Guardar en CSV
        if filter_dates:
            csv_file = f"reporte_{start_date.strftime('%d%m%Y')}_a_{end_date.strftime('%d%m%Y')}.csv"
        else:
            csv_file = f"reporte_completo_{datetime.now().strftime('%d%m%Y_%H%M%S')}.csv"
        
        filtered.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"✅ Reporte guardado: {csv_file}\n")
        
        # Resumen por estado
        print("\n" + "="*60)
        print("📊 RESUMEN POR ESTADO")
        print("="*60 + "\n")
        
        if 'Estado' in filtered.columns:
            estado_counts = filtered['Estado'].value_counts()
            for estado, count in estado_counts.items():
                print(f"  {estado}: {count} proyectos")
        
        print("\n")


def main():
    """Punto de entrada"""
    try:
        importer = ExcelImporter(excel_folder="./logs/excel")
        importer.generate_report(filter_dates=True)
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error en main: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
