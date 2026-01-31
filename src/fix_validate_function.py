"""
Script to fix the validate_data_quality function in data_aggr_improved.ipynb
Fixes the TypeError when dates have mixed types (datetime and strings).
"""

import json
import sys

def fix_validate_function(notebook_path):
    """Fix the validate_data_quality function in the notebook"""
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Find the cell with validate_data_quality function
    fixed_function = '''def validate_data_quality(df, file_name):
    """Validate data quality and return report"""
    report = {
        'file': file_name,
        'rows': len(df),
        'columns': len(df.columns),
        'missing_dates': 0,
        'missing_totals': 0,
        'duplicate_rows': 0,
        'date_range': None
    }
    
    # Check for date column
    date_col = None
    for col in DATE_COLUMNS:
        if col.lower() in df.columns:
            date_col = col.lower()
            break
    
    if date_col:
        report['missing_dates'] = df[date_col].isna().sum()
        valid_dates = df[date_col].dropna()
        
        if len(valid_dates) > 0:
            # Convert to datetime if needed (handle mixed types)
            try:
                # Try to convert to datetime if not already
                if not pd.api.types.is_datetime64_any_dtype(valid_dates):
                    valid_dates = pd.to_datetime(valid_dates, errors='coerce')
                
                # Only compute min/max if we have valid datetime values
                valid_datetime = valid_dates.dropna()
                if len(valid_datetime) > 0:
                    report['date_range'] = (valid_datetime.min(), valid_datetime.max())
            except Exception as e:
                # If conversion fails, skip date range
                logger.warning(f"Could not compute date range for {file_name}: {e}")
                report['date_range'] = None
    
    # Check for total column
    if 'total' in df.columns:
        report['missing_totals'] = df['total'].isna().sum()
    
    # Check for duplicates
    if date_col:
        report['duplicate_rows'] = df.duplicated(subset=[date_col]).sum()
    
    return report'''
    
    # Find and replace the function
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'def validate_data_quality' in source and 'valid_dates.min()' in source:
                # This is the problematic cell - replace it
                cell['source'] = [line + '\n' for line in fixed_function.split('\n')]
                print("✅ Found and fixed the validate_data_quality function!")
                break
    
    # Write the fixed notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Fixed notebook saved to: {notebook_path}")

if __name__ == "__main__":
    notebook_path = "data_aggr_improved.ipynb"
    try:
        fix_validate_function(notebook_path)
        print("\n✅ Fix complete! You can now run the notebook again.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
