import pandas as pd

def load_excel_text(path):
    df = pd.read_excel(path, sheet_name=None)
    combined = ""
    for name, sheet in df.items():
        combined += f"### Sheet: {name}\n\n"
        combined += sheet.astype(str).to_string(index=False)
        combined += "\n\n"
    return combined
