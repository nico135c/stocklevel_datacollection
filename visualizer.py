import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import os
import re

# -------------------------
# Prompt user to choose file
# -------------------------

data_folder = "data"

# List .xlsx files
files = [f for f in os.listdir(data_folder) if f.lower().endswith(".xlsx")]

if not files:
    print("No .xlsx files found in the 'data' folder.")
    exit()

print("Select a file to process:")
for i, f in enumerate(files):
    print(f"{i+1}. {f}")

choice = int(input("Enter the number of the file: ")) - 1

if choice < 0 or choice >= len(files):
    print("Invalid selection.")
    exit()

input_file = os.path.join(data_folder, files[choice])
print(f"\nLoading: {input_file}\n")

# -------------------------
# Prepare filenames
# -------------------------

base_name = os.path.splitext(os.path.basename(input_file))[0]
safe_name = re.sub(r'[^A-Za-z0-9_]+', '_', base_name)

output_dir = f"data/plots_{safe_name}"
os.makedirs(output_dir, exist_ok=True)

# -------------------------
# Load data
# -------------------------

df = pd.read_excel(input_file)

# Ensure correct column order (Part 0, Part 1, ...)
df = df.reindex(sorted(df.columns, key=lambda x: int(x.split()[1])), axis=1)


# ---------------------------------------------------------
# 1. Mean Sensor Reading vs. Stock Level (Line Plot)
# ---------------------------------------------------------

means = df.mean()

plt.figure(figsize=(10, 6))
plt.plot(means.index, means.values, marker='o')
plt.xlabel("Stock Level (Part Count 0–20)")
plt.ylabel("Mean Sensor Reading")
plt.title("Average Ultrasound Sensor Reading vs. Stock Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/{safe_name}_mean_vs_level.png")
plt.close()


# ---------------------------------------------------------
# 2. Boxplots for Each Stock Level
# ---------------------------------------------------------

plt.figure(figsize=(14, 6))
sns.boxplot(data=df)
plt.xlabel("Stock Level")
plt.ylabel("Sensor Reading")
plt.title("Boxplot of Sensor Readings per Stock Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/{safe_name}_boxplots.png")
plt.close()


# ---------------------------------------------------------
# 3. Scatter plot of ALL individual samples
# ---------------------------------------------------------

plt.figure(figsize=(14, 6))
for i, col in enumerate(df.columns):
    plt.scatter([i] * len(df[col]), df[col], alpha=0.4)

plt.xlabel("Stock Level Index")
plt.ylabel("Sensor Reading")
plt.title("All Sensor Samples Across All Stock Levels")
plt.xticks(range(len(df.columns)), df.columns, rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/{safe_name}_all_samples.png")
plt.close()


# ---------------------------------------------------------
# 4. Calibration Curve (Regression + Confidence Interval)
# ---------------------------------------------------------

X = np.array([int(col.split()[1]) for col in df.columns]).reshape(-1, 1)
y = means.values

model = LinearRegression()
model.fit(X, y)

x_pred = np.linspace(0, len(df.columns) - 1, 200).reshape(-1, 1)
y_pred = model.predict(x_pred)

# Confidence interval estimate
residuals = y - model.predict(X)
std_residuals = residuals.std()
ci = 1.96 * std_residuals

plt.figure(figsize=(10, 6))
plt.plot(X, y, 'o', label="Mean readings")
plt.plot(x_pred, y_pred, label="Regression", linewidth=2)

plt.fill_between(
    x_pred.flatten(),
    y_pred - ci,
    y_pred + ci,
    alpha=0.2,
    label="95% Confidence Interval"
)

plt.xlabel("Stock Level")
plt.ylabel("Mean Sensor Reading")
plt.title("Calibration Curve for Ultrasound Sensor")
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/{safe_name}_calibration_curve.png")
plt.close()


# ---------------------------------------------------------
# 5. Correlation Heatmap
# ---------------------------------------------------------

plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=False, cmap="viridis")
plt.title("Correlation Heatmap of Ultrasound Readings")
plt.tight_layout()
plt.savefig(f"{output_dir}/{safe_name}_correlation_heatmap.png")
plt.close()


print(f"All plots generated and saved in the '{output_dir}' folder.")