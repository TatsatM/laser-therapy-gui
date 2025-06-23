import pandas as pd
import json

# Load your Excel data
df = pd.read_excel(r"C:\Users\malvi\OneDrive\Desktop\project delhi\PythonProject\data_set.xlsx")

# Fill forward any missing BodyPart values (if needed)
df["BodyPart"] = df["BodyPart"].fillna(method="ffill")

data = []

for _, row in df.iterrows():
    entry = {
        "BodyPart": row["BodyPart"],
        "Condition": row["Condition"],
        "Power(%)": row["Power"],
        "Peak Power(W)": row["Peak Power"],
        "Pulse Width(Micro Sec)": row["Pulse Width"],
        "Pulse Freq(Hz)": row["Pulse Freq"],
        "Avg Power(W)": row["Avg Power"],
        "Dosage": {
            "Chronic": row["Chronic Dosage"],
            "Subacute": row["Subacute Dosage"],
            "Acute": row["Acute Dosage"]
        },
        "Area": {
            "Large": row["Large Area"],
            "Medium": row["Medium Area"],
            "Small": row["Small Area"]
        },
        "Time(min)": {
            "Chronic": row["Chronic Time"],
            "Subacute": row["Subacute Time"],
            "Acute": row["Acute Time"]
        },
        "Total Energy(J)": {
            "Chronic": row["Chronic Energy"],
            "Subacute": row["Subacute Energy"],
            "Acute": row["Acute Energy"]
        }
    }
    data.append(entry)

# Save to JSON
with open("therapy_data.json", "w") as f:
    json.dump(data, f, indent=4)
