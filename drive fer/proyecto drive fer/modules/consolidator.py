"""
Consolidator Module
Handles consolidation of data from multiple department sheets into master schedule
"""

import logging
from typing import Dict, List, Tuple
import pandas as pd

logger = logging.getLogger(__name__)


class Consolidator:
    """Consolidates data from multiple department sheets"""
    
    def __init__(self):
        """Initialize Consolidator"""
        logger.info("Consolidator initialized")
    
    def prepare_department_data(self, 
                               sheet_data: List[List],
                               department_name: str,
                               headers: List[str]) -> pd.DataFrame:
        """
        Prepare data from a single department sheet
        Automatically detects and maps Excel column format if needed
        
        Args:
            sheet_data: Raw data from Google Sheet (list of lists)
            department_name: Name of the department
            headers: Column headers (used if data is already in expected format)
        
        Returns:
            DataFrame with department data in standard format
        """
        try:
            if not sheet_data or len(sheet_data) <= 1:
                # No data except headers
                logger.warning(f"No data found for {department_name}")
                return pd.DataFrame(columns=headers + ['Departamento'])
            
            # Get actual headers from first row
            actual_headers = sheet_data[0]
            data_rows = sheet_data[1:]
            
            logger.info(f"[{department_name}] Row count: {len(data_rows)}, Column count: {len(actual_headers)}")
            logger.info(f"[{department_name}] Actual headers from sheet: {actual_headers}")
            
            # Create DataFrame with actual headers
            df = pd.DataFrame(data_rows, columns=actual_headers)
            
            logger.info(f"[{department_name}] DataFrame shape before mapping: {df.shape}")
            logger.info(f"[{department_name}] DataFrame columns: {df.columns.tolist()}")
            
            # Check if we need to map Excel columns
            # Excel format has 11 columns or has specific Excel header names
            needs_mapping = (
                len(actual_headers) >= 10 or  # 10+ columns suggests Excel format
                'COTIZACIÓN' in actual_headers or 
                'Rubro de Cotización' in actual_headers or
                'Fecha de pedido' in actual_headers
            )
            
            if needs_mapping:
                logger.info(f"[{department_name}] Detected Excel format ({len(actual_headers)} columns), applying mapping...")
                df = self.map_excel_columns(df)
                logger.info(f"[{department_name}] DataFrame columns after mapping: {df.columns.tolist()}")
            else:
                logger.info(f"[{department_name}] Using standard format ({len(actual_headers)} columns)")
            
            # Add department column if not already present
            if 'Departamento' not in df.columns:
                df['Departamento'] = department_name
            
            # Remove empty rows
            df = df.dropna(how='all')
            
            # Remove rows where ID_Proyecto is empty
            if 'ID_Proyecto' in df.columns:
                df = df[df['ID_Proyecto'].astype(str).str.strip() != '']
            
            logger.info(f"Prepared {len(df)} rows from {department_name}")
            return df
        except Exception as e:
            logger.error(f"Error preparing data for {department_name}: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return pd.DataFrame(columns=headers + ['Departamento'])
    
    def consolidate_all_departments(self,
                                   department_data: Dict[str, List[List]],
                                   headers: List[str]) -> pd.DataFrame:
        """
        Consolidate data from all departments
        
        Args:
            department_data: Dictionary of {department_name: sheet_data}
            headers: Column headers for the sheets
        
        Returns:
            Consolidated DataFrame
        """
        try:
            dataframes = []
            
            for dept_name, sheet_data in department_data.items():
                df = self.prepare_department_data(sheet_data, dept_name, headers)
                if not df.empty:
                    dataframes.append(df)
            
            if not dataframes:
                logger.warning("No data to consolidate from any department")
                return pd.DataFrame(columns=headers + ['Departamento'])
            
            # Concatenate all dataframes
            consolidated = pd.concat(dataframes, ignore_index=True)
            
            # Reorder columns to put Departamento last
            cols = [col for col in consolidated.columns if col != 'Departamento'] + ['Departamento']
            consolidated = consolidated[cols]
            
            logger.info(f"Consolidated {len(consolidated)} total projects from all departments")
            return consolidated
        except Exception as e:
            logger.error(f"Error consolidating departments: {str(e)}")
            return pd.DataFrame(columns=headers + ['Departamento'])
    
    def dataframe_to_sheet_data(self, df: pd.DataFrame) -> List[List]:
        """
        Convert DataFrame to format suitable for Google Sheets
        Handles datetime conversion to DD/MM/YYYY format and NaN/inf replacement
        
        Args:
            df: DataFrame to convert
        
        Returns:
            List of lists suitable for Google Sheets
        """
        try:
            import numpy as np
            
            # Create a copy to avoid modifying original
            df_copy = df.copy()
            
            # FIRST: Convert datetime columns to DD/MM/YYYY format BEFORE any other conversions
            for col in df_copy.columns:
                # Check if it's already datetime type
                if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                    df_copy[col] = df_copy[col].dt.strftime('%d/%m/%Y')
                # Try to parse as datetime if it's object type (string)
                elif df_copy[col].dtype == 'object':
                    try:
                        # Try to convert to datetime
                        temp = pd.to_datetime(df_copy[col], errors='coerce')
                        # If most values parsed successfully, convert
                        non_na_count = temp.notna().sum()
                        total_count = len(temp)
                        
                        if non_na_count > 0 and non_na_count / total_count > 0.5:  # At least 50% parsed
                            df_copy[col] = temp.dt.strftime('%d/%m/%Y')
                            # Replace 'NaT' strings with empty string
                            df_copy[col] = df_copy[col].replace('NaT', '')
                    except:
                        pass  # Leave as-is if conversion fails
            
            # SECOND: Replace all remaining numpy NaN and inf with empty strings
            df_copy = df_copy.replace([np.inf, -np.inf], np.nan)
            df_copy = df_copy.where(pd.notna(df_copy), '')
            
            # Add header row
            header = [df_copy.columns.tolist()]
            
            # Convert all data to strings, handling special cases
            data = []
            for row in df_copy.values:
                converted_row = []
                for val in row:
                    # Handle None
                    if val is None:
                        converted_row.append('')
                    # Handle numpy NaN (though should be replaced already)
                    elif isinstance(val, float) and np.isnan(val):
                        converted_row.append('')
                    # Handle pandas NA
                    elif pd.isna(val):
                        converted_row.append('')
                    # Handle empty string
                    elif val == '':
                        converted_row.append('')
                    # Convert everything else to string, strip whitespace
                    else:
                        converted_row.append(str(val).strip())
                data.append(converted_row)
            
            logger.info(f"Converted {len(data)} rows to sheet format")
            return header + data
        except Exception as e:
            logger.error(f"Error converting DataFrame to sheet data: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def get_department_summary(self, df: pd.DataFrame, department: str) -> Dict:
        """
        Get summary statistics for a specific department
        
        Args:
            df: Consolidated DataFrame
            department: Department name
        
        Returns:
            Summary dictionary
        """
        try:
            dept_data = df[df['Departamento'] == department]
            
            summary = {
                'departamento': department,
                'total_proyectos': len(dept_data),
                'pendiente': len(dept_data[dept_data['Estado'] == 'Pendiente']),
                'en_progreso': len(dept_data[dept_data['Estado'] == 'En progreso']),
                'completado': len(dept_data[dept_data['Estado'] == 'Completado']),
                'retrasado': len(dept_data[dept_data['Estado'] == 'Retrasado'])
            }
            
            return summary
        except Exception as e:
            logger.error(f"Error getting summary for {department}: {str(e)}")
            return {}
    
    def get_all_summaries(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Get summary for all departments
        
        Args:
            df: Consolidated DataFrame
        
        Returns:
            Dictionary of summaries by department
        """
        try:
            summaries = {}
            
            for department in df['Departamento'].unique():
                summary = self.get_department_summary(df, department)
                if summary:
                    summaries[department] = summary
            
            logger.info(f"Generated summaries for {len(summaries)} departments")
            return summaries
        except Exception as e:
            logger.error(f"Error getting all summaries: {str(e)}")
            return {}
    
    def export_to_csv(self, df: pd.DataFrame, filepath: str) -> bool:
        """
        Export consolidated data to CSV
        
        Args:
            df: DataFrame to export
            filepath: Path to save CSV
        
        Returns:
            True if successful, False otherwise
        """
        try:
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"Exported consolidated data to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return False
    
    def map_excel_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Map Excel columns (11 columns) to expected format (8 columns)
        
        Excel structure (11 columns):
        A: COTIZACIÓN → ID_Proyecto
        B: Última Rev. → (skip)
        C: Cliente → Cliente
        D: Rubro de Cotización → (skip, handled by department)
        E: Vendedor → Responsable
        F: Fecha de pedido → Fecha_Inicio
        G: Fecha primer envío → Fecha_Entrega
        H: Fecha último estado → Fecha último estado
        I: Diferencia de días → (skip)
        J: Estado → Estado
        K: Descripción → Descripcion
        
        Args:
            df: DataFrame with Excel data (11 columns)
        
        Returns:
            DataFrame with mapped columns (8 required columns)
        """
        try:
            logger.info(f"Starting Excel column mapping for {len(df)} rows")
            logger.info(f"Input columns: {df.columns.tolist()}")
            
            # Expected column order in Excel
            expected_cols = [
                'COTIZACIÓN', 'Última Rev.', 'Cliente', 'Rubro de Cotización', 
                'Vendedor', 'Fecha de pedido', 'Fecha primer envío', 
                'Fecha último estado', 'Diferencia de días', 'Estado', 'Descripción'
            ]
            
            # Check if we have the expected structure
            actual_cols = df.columns.tolist()
            
            # Build mapped dataframe using column position if names don't match
            if len(actual_cols) >= 11 or len(actual_cols) == 11:
                # Map by position (columns A-K)
                mapped_data = {}
                
                # Column A (index 0): ID_Proyecto
                if len(actual_cols) > 0:
                    mapped_data['ID_Proyecto'] = df.iloc[:, 0]
                
                # Column C (index 2): Cliente
                if len(actual_cols) > 2:
                    mapped_data['Cliente'] = df.iloc[:, 2]
                
                # Column E (index 4): Responsable
                if len(actual_cols) > 4:
                    mapped_data['Responsable'] = df.iloc[:, 4]
                
                # Column F (index 5): Fecha_Inicio
                if len(actual_cols) > 5:
                    mapped_data['Fecha_Inicio'] = df.iloc[:, 5]
                
                # Column G (index 6): Fecha_Entrega
                if len(actual_cols) > 6:
                    mapped_data['Fecha_Entrega'] = df.iloc[:, 6]
                
                # Column H (index 7): Fecha último estado (optional, for validation)
                if len(actual_cols) > 7:
                    mapped_data['Fecha último estado'] = df.iloc[:, 7]
                
                # Column J (index 9): Estado
                if len(actual_cols) > 9:
                    mapped_data['Estado'] = df.iloc[:, 9]
                
                # Column K (index 10): Descripcion
                if len(actual_cols) > 10:
                    mapped_data['Descripcion'] = df.iloc[:, 10]
                
                df_mapped = pd.DataFrame(mapped_data)
                logger.info(f"Mapped columns by position: {df_mapped.columns.tolist()}")
            
            # Ensure all required columns exist
            required_cols = [
                'ID_Proyecto', 'Cliente', 'Descripcion',
                'Fecha_Inicio', 'Fecha_Entrega', 'Estado', 'Responsable'
            ]
            
            for col in required_cols:
                if col not in df_mapped.columns:
                    logger.warning(f"Missing column: {col}, adding empty column")
                    df_mapped[col] = ''
            
            # Reorder to standard format
            df_result = df_mapped[required_cols].copy()
            
            logger.info(f"Mapped {len(df_result)} rows from Excel format to standard format")
            logger.info(f"Output columns: {df_result.columns.tolist()}")
            return df_result
            
        except Exception as e:
            logger.error(f"Error mapping Excel columns: {str(e)}")
            logger.error(f"Input shape: {df.shape}, columns: {df.columns.tolist()}")
            return df
    
    def validate_data_integrity(self, df: pd.DataFrame, headers: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate data integrity of consolidated DataFrame
        
        Args:
            df: DataFrame to validate
            headers: Required headers
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        from typing import Tuple
        
        errors = []
        
        # Check headers
        expected_headers = headers + ['Departamento']
        actual_headers = list(df.columns)
        
        for header in expected_headers:
            if header not in actual_headers:
                errors.append(f"Missing header: {header}")
        
        # Check for empty critical fields
        critical_fields = ['ID_Proyecto', 'Cliente', 'Departamento']
        for field in critical_fields:
            if field in df.columns:
                empty_count = df[field].isna().sum() + (df[field] == '').sum()
                if empty_count > 0:
                    errors.append(f"Found {empty_count} empty values in {field}")
        
        # Check valid states
        if 'Estado' in df.columns:
            valid_states = ['Pendiente', 'En progreso', 'Completado', 'Retrasado']
            invalid_states = df[~df['Estado'].isin(valid_states)]['Estado'].unique()
            if len(invalid_states) > 0:
                errors.append(f"Invalid states found: {', '.join(invalid_states)}")
        
        is_valid = len(errors) == 0
        logger.info(f"Data validation: {'PASSED' if is_valid else 'FAILED'} ({len(errors)} errors)")
        
        return is_valid, errors
