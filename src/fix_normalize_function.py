"""
Script to fix the normalize_column_names function in data_aggr_improved.ipynb
Run this script to automatically fix the IndexError issue.
"""

import json
import sys

def fix_normalize_function(notebook_path):
    """Fix the normalize_column_names function in the notebook"""
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Find the cell with normalize_column_names function
    fixed_function = '''def normalize_column_names(df):
    """Normalize column names: lowercase, strip, handle duplicates"""
    df = df.copy()
    
    # Step 1: Strip and lowercase
    df.columns = df.columns.str.strip().str.lower()
    
    # Step 2: Identify duplicate column names
    counts = Counter(df.columns)
    duplicate_groups = {name: [] for name, count in counts.items() if count > 1}
    
    # Step 3: Group duplicate columns by name and get their positions
    for idx, col_name in enumerate(df.columns):
        if col_name in duplicate_groups:
            duplicate_groups[col_name].append(idx)
    
    # Step 4: Combine duplicate columns and build new dataframe
    combined_data = {}
    processed_duplicates = set()
    
    for idx, col_name in enumerate(df.columns):
        # Skip if this column is a duplicate we've already processed
        if col_name in processed_duplicates:
            continue
            
        if col_name in duplicate_groups:
            # This is a duplicate group - combine them
            duplicate_indices = duplicate_groups[col_name]
            
            # Get all duplicate columns
            duplicate_cols = df.iloc[:, duplicate_indices]
            
            # Combine using backfill (fill missing values from right to left)
            combined = duplicate_cols.bfill(axis=1).iloc[:, 0]
            
            combined_data[col_name] = combined
            
            # Mark all duplicates as processed
            processed_duplicates.add(col_name)
        else:
            # Regular column - keep as is
            combined_data[col_name] = df.iloc[:, idx]
    
    # Step 5: Create new dataframe with unique columns
    result_df = pd.DataFrame(combined_data)
    
    # Step 6: Ensure no remaining duplicates (safety check)
    result_df = result_df.loc[:, ~result_df.columns.duplicated()]
    
    return result_df'''
    
    # Find and replace the function
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'def normalize_column_names' in source and 'col_indices[1:]' in source:
                # This is the problematic cell - replace it
                cell['source'] = fixed_function.split('\n')
                # Add newline to each line to match notebook format
                cell['source'] = [line + '\n' for line in fixed_function.split('\n')]
                print("✅ Found and fixed the normalize_column_names function!")
                break
    
    # Write the fixed notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Fixed notebook saved to: {notebook_path}")

if __name__ == "__main__":
    notebook_path = "data_aggr_improved.ipynb"
    try:
        fix_normalize_function(notebook_path)
        print("\n✅ Fix complete! You can now run the notebook again.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
