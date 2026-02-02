import os
import json
import csv
from typing import List, Dict, Any, Optional
from datetime import datetime

# File operations tools 

def read_file(filepath: str) -> str:
    """
    Read and return the contents of a file.
    
    Args:
        filepath: Path to the file to read
        
    Returns:
        File contents as string
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(filepath: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        filepath: Path to the file to write
        content: Content to write to the file
        
    Returns:
        Success or error message
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def list_directory(dirpath: str) -> List[str]:
    """
    List all files and directories in a given path.
    
    Args:
        dirpath: Directory path to list
        
    Returns:
        List of file and directory names
    """
    try:
        return os.listdir(dirpath)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]


# CSV tools

def read_csv(filepath: str) -> Dict[str, Any]:
    """
    Read CSV file and return only top N rows.
    """
    try:
        limit = 10
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            rows = []
            for i, row in enumerate(reader):
                if i >= limit:
                    break
                rows.append(row)

            return {
                'headers': reader.fieldnames,
                'rows': rows,
                'row_count': len(rows),
                'note': f"Showing first {limit} rows only"
            }

    except Exception as e:
        return {'error': str(e)}
    

def write_csv(filepath: str, data: List[Dict[str, Any]], headers:List[str]) -> str:
    """
    Write data to CSV file.
    
    Args:
        filepath: Path to output CSV file
        data: List of dictionaries to write
        headers: list of headers (uses data keys if not provided)
        
    Returns:
        Success or error message
    """
    try:
        if not data:
            return "Error: No data to write"
        
        if headers is None | headers!=list(data[0].keys()):
            headers = list(data[0].keys())
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        
        return f"Successfully wrote {len(data)} rows to {filepath}"
    except Exception as e:
        return f"Error writing CSV: {str(e)}"


def analyze_csv_columns(filepath: str) -> Dict[str, Any]:
    """
    Analyze CSV columns for basic statistics.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        Dictionary with column analysis
    """
    try:
        data = read_csv(filepath)
        if 'error' in data:
            return data
        
        analysis = {}
        for header in data['headers']:
            values = [row.get(header, '') for row in data['rows']]
            non_empty = [v for v in values if v]
            
            analysis[header] = {
                'total_values': len(values),
                'non_empty_values': len(non_empty),
                'empty_values': len(values) - len(non_empty),
                'unique_values': len(set(non_empty)),
                'sample_values': non_empty[:5]
            }
        
        return analysis
    except Exception as e:
        return {'error': str(e)}


# JSON tools

def read_json(filepath: str) -> Dict[str, Any]:
    """
    Read and parse JSON file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {'error': str(e)}


def write_json(filepath: str, data: Any, indent: int ) -> str:
    """
    Write data to JSON file.
    
    Args:
        filepath: Path to output JSON file
        data: Data to write
        indent: Indentation level for pretty printing
        
    Returns:
        Success or error message
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        return f"Successfully wrote JSON to {filepath}"
    except Exception as e:
        return f"Error writing JSON: {str(e)}"

# Logging tools

def create_log_entry(log_file:str, agent_name: str, action: str, details: Dict[str, Any]) -> str:
    """
    Create a timestamped log entry for agent actions.
    
    Args:
        log_file: File to store logs
        agent_name: Name of the agent
        action: Action being performed
        details: Additional details to log
        
    Returns:
        Path to log file
    """
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        log_entry = {
            'timestamp': timestamp,
            'agent': agent_name,
            'action': action,
            'details': details
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            json.dump(log_entry, f, indent=2)
            f.write('\n')
        
        return log_file
    except Exception as e:
        return f"Error creating log: {str(e)}"


def read_logs(log_dir: str) -> List[Dict[str, Any]]:
    """
    Read recent log entries.

    Args:
        log_dir: File containing log files
        limit: Number of most recent logs to return

    Returns:
        List of latest log entries
    """
    logs = []
    limit: int = 8

    try:
        if not os.path.exists(log_dir):
            return logs

        for filename in os.listdir(log_dir):
            if filename.endswith('.log'):
                filepath = os.path.join(log_dir, filename)

                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            logs.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue  # skip bad lines

        logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        return logs[:limit]

    except Exception as e:
        return [{'error': str(e)}]
    
