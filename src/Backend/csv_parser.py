"""CSV Parser for financial data."""

import csv
from pathlib import Path
from typing import List, Dict, Any, Optional


class FinancialRecord:
    """Represents a single financial record from CSV."""
    
    def __init__(self, data: Dict[str, Any]):
        """Initialize a financial record.
        
        Args:
            data: Dictionary of field names to values
        """
        self.data = data
    
    def __getitem__(self, key: str) -> Any:
        """Access field value by key."""
        return self.data.get(key)
    
    def __repr__(self) -> str:
        """String representation of record."""
        return f"FinancialRecord({self.data})"
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get field value with optional default."""
        return self.data.get(key, default)


class CSVParser:
    """Parses CSV files and stores data in organized classes."""
    
    def __init__(self, file_path: str):
        """Initialize CSV parser.
        
        Args:
            file_path: Path to CSV file to parse
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If file is not a valid CSV
        """
        self.file_path = Path(file_path)
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        if self.file_path.suffix.lower() != '.csv':
            raise ValueError(f"File must be a CSV file, got: {self.file_path.suffix}")
        
        self.headers: List[str] = []
        self.records: List[FinancialRecord] = []
        self._parse()
    
    def _parse(self) -> None:
        """Parse the CSV file into records."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                if reader.fieldnames is None:
                    raise ValueError("CSV file is empty or has no headers")
                
                self.headers = list(reader.fieldnames)
                
                for row in reader:
                    # Convert numeric strings to appropriate types
                    converted_row = self._convert_types(row)
                    record = FinancialRecord(converted_row)
                    self.records.append(record)
            
        except csv.Error as e:
            raise ValueError(f"Error parsing CSV: {e}")
    
    def _convert_types(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Convert string values to appropriate types.
        
        Args:
            row: Dictionary of string values from CSV
            
        Returns:
            Dictionary with converted types
        """
        converted = {}
        
        for key, value in row.items():
            if value is None or value == '':
                converted[key] = None
                continue
            
            # Try to convert to float
            try:
                if '.' in str(value):
                    converted[key] = float(value)
                else:
                    converted[key] = int(value)
            except (ValueError, TypeError):
                # Keep as string if conversion fails
                converted[key] = value
        
        return converted
    
    def get_record(self, index: int) -> Optional[FinancialRecord]:
        """Get a specific record by index.
        
        Args:
            index: Row index (0-based)
            
        Returns:
            FinancialRecord or None if index out of range
        """
        if 0 <= index < len(self.records):
            return self.records[index]
        return None
    
    def get_all_records(self) -> List[FinancialRecord]:
        """Get all records.
        
        Returns:
            List of all FinancialRecord objects
        """
        return self.records
    
    def get_column(self, column_name: str) -> List[Any]:
        """Get all values from a specific column.
        
        Args:
            column_name: Name of the column
            
        Returns:
            List of values from that column
            
        Raises:
            KeyError: If column doesn't exist
        """
        if column_name not in self.headers:
            raise KeyError(f"Column '{column_name}' not found. Available: {self.headers}")
        
        return [record[column_name] for record in self.records]
    
    def filter_records(self, field: str, value: Any) -> List[FinancialRecord]:
        """Filter records by field value.
        
        Args:
            field: Field name to filter on
            value: Value to match
            
        Returns:
            List of matching records
        """
        return [record for record in self.records if record[field] == value]
    
    def __len__(self) -> int:
        """Return number of records."""
        return len(self.records)
    
    def __iter__(self):
        """Iterate over records."""
        return iter(self.records)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"CSVParser(file='{self.file_path.name}', records={len(self.records)})"
