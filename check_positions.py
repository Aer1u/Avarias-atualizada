import pandas as pd
file_path = r"c:\Users\Pichau\Downloads\Avaria\Drive atualizado.xlsx"
try:
    df = pd.read_excel(file_path)
    # Find position column
    pos_col = next(col for col in df.columns if 'posi' in str(col).lower())
    unique_pos = df[pos_col].dropna().unique().tolist()
    print("Sample unique positions (first 20):")
    for pos in unique_pos[:20]:
        print(pos)
except Exception as e:
    print(f"Error: {e}")
