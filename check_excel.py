import pandas as pd
file_path = r"c:\Users\Pichau\Downloads\Avaria\Drive atualizado.xlsx"
try:
    df = pd.read_excel(file_path)
    print("Columns found:")
    print(df.columns.tolist())
    print("\nFirst row sample:")
    print(df.iloc[0].to_dict())
except Exception as e:
    print(f"Error: {e}")
