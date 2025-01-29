import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data extracted from excel
data = {
    "Tip": ["A", "B", "C", "D", "E", "F", "G", "H"] * 4,
    "Run": ["50 uL - Run 1"] * 8 + ["50 uL - Run 2"] * 8 + ["20 uL - Run 1 "] * 8 + ["20 uL - Run 2 "] * 8,
    "Programmed Volume (µL)": [50] * 16 + [20] * 16,
    "Measured Volume (µL)": [
        50, 49.5, 50, 50.5, 50, 42.5, 48, 50,  # 50uL - Run 1
        52, 51.5, 51, 51.5, 51, 51.5, 51.5, 51,  # 50 uL - Run 2
        21, 21, 21, 21, 21, 21, 21, 21,  # 20 uL - Run 1
        21, 21, 21, 21, 21, 21, 21, 21  # 20 uL - Run 2
    ],
    "Error (µL)": [
        0.0, 0.5, 0.0, -0.5, 0.0, 7.5, 2.0, 0.0,  # 50uL - Run 1
        -2.0, -1.5, -1.0, -1.5, -1.0, -1.5, -1.5, -1.0,  # 50 uL - Run 2
        -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,  # 20 uL - Run 1
        -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0  # 20 uL - Run 2 
    ],
    "% Error": [
        0, 1, 0, 1, 0, 15, 4, 0,  # 50uL - Run 1
        4, 3, 2, 3, 2, 3, 3, 2,  # 50 uL - Run 2
        5, 5, 5, 5, 5, 5, 5, 5,  # 20 uL - Run 1
        5, 5, 5, 5, 5, 5, 5, 5 # 20 uL - Run 2 
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Remove the 15% error point
df = df[df["% Error"] != 15].reset_index(drop=True)

# Combine Run 1 and Run 2 for 50 µL volumes
df_combined_50ul = df[df["Programmed Volume (µL)"] == 50].copy()
df_combined_50ul["Run"] = "50 µL"  # Label combined data

# Combine Run 1 and Run 2 for 20 µL volumes
df_combined_20ul = df[df["Programmed Volume (µL)"] == 20].copy()
df_combined_20ul["Run"] = "20 µL"  # Label combined data

# Combine both datasets back into one
df_final = pd.concat([df_combined_50ul, df_combined_20ul], ignore_index=True)

# Plot: Box Plot for % Error Across Combined Runs
plt.figure(figsize=(10, 6))
sns.boxplot(x="Run", y="% Error", data=df_final, palette="Set2")
plt.title("Box Plot of % Error Across Combined Runs")
plt.xlabel("Run")
plt.ylabel("% Error")
plt.show()
