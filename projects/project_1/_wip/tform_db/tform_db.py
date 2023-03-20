import os
import pandas as pd
import numpy as np

# Some code is added to create a 'line' of new models, see comments on top of the notebook
new = True


# Define function to clear all 'earlier' models from directory
def remove_files(path, new_, ext):
    for f in os.listdir(path):
        if len(new_) == 0:
            if ext in f and not new_ in f:
                os.remove(os.path.join(path, f))
        else:
            if ext in f and new_ in f:
                os.remove(os.path.join(path, f))


# Load csv
df = pd.read_csv("../dload_db/csv/db_mcr.csv")
# df = pd.read_csv("../dload_db/csv/static_db_mcr.csv")

# List non numerical data
list_non_num = []
for variable in df.columns:
    list_non_num = (
        list_non_num
        + df.index[~pd.to_numeric(df[variable], errors="coerce").notnull()].tolist()
    )

# Remove non numerical data
set_non_num = set(list_non_num)
df = df.loc[~df.index.isin(set_non_num)]

# Convert datatypes to numerical
for variable in df.columns:
    df[variable] = pd.to_numeric(df[variable])

# List acceptable data-range
range_var = {
    "genetic": (40, 120),
    "length": (147, 220),
    "mass": (30, 200),
    "exercise": (0, 8),
    "smoking": (0, 60),
    "alcohol": (0, 12),
    "sugar": (0, 50),
    "lifespan": (40, 120),
}

# List data outside acceptable range
list_illogical = []
for variable in df.columns:
    range_min = range_var[variable][0]
    range_max = range_var[variable][1]
    list_illogical = (
        list_illogical
        + df.index[(df[variable] < range_min) | (df[variable] > range_max)].tolist()
    )

# Remove data outside acceptable range
set_illogical = set(list_illogical)
df = df.loc[~df.index.isin(set_illogical)]

# Remove duplicates
df = df[~df.duplicated()]

# Rearrange columns to put dependent variable ('lifespan') in front
df_cols = df.columns.tolist()
df_cols = df_cols[-1:] + df_cols[:-1]
df = df[df_cols]

# Transform columns if necessary, in this case sugar only
df["sugar"] = df["sugar"] * 4

# Add new (combinations of) variables, either rational or dummy's
# BMI dummies
df["bmi"] = df["mass"] / (
    (df["length"] / 100) ** 2
)  # BMI as combined variable of mass and length
bmi_cat = (0, 18.5, 25, 30, 40)  # Healthy upper and lower bounds of BMI

df.loc[df["bmi"] <= bmi_cat[1], "bmi norm under"] = (
    df["bmi"] - bmi_cat[1]
)  # Normalised BMI for subjects under healthy levels
df.loc[df["bmi"] > bmi_cat[1], "bmi norm under"] = 0
df.loc[df["bmi"] >= bmi_cat[2], "bmi norm over"] = (
    df["bmi"] - bmi_cat[2]
)  # Normalised BMI for subjects over healthy levels
df.loc[df["bmi"] < bmi_cat[2], "bmi norm over"] = 0

df["bmi under"] = df["bmi"].between(
    bmi_cat[0], bmi_cat[1], "right"
)  # Dummy of underweight subjects
df["bmi over"] = df["bmi"].between(
    bmi_cat[1], bmi_cat[2], "right"
)  # Dummy of overweight subjects
df["bmi obese"] = df["bmi"].between(
    bmi_cat[2], bmi_cat[3], "right"
)  # Dummy of obese subjects subjects
df["bmi morbid"] = df["bmi"] > bmi_cat[3]  # Dummy of morbidly obese subjects

# Smoking dummies
smoking_cat = (0, 5, 10, 15, 20)
df["smoking few"] = df["smoking"].between(
    smoking_cat[0], smoking_cat[1], "right"
)  # Smoking few (1-5) sigarettes as dummy
df["smoking some"] = df["smoking"].between(
    smoking_cat[1], smoking_cat[2], "right"
)  # Smoking some (6-10) sigarettes as dummy
df["smoking more"] = df["smoking"].between(
    smoking_cat[2], smoking_cat[3], "right"
)  # Smoking more (11-15) sigarettes as dummy
df["smoking alot"] = df["smoking"].between(
    smoking_cat[3], smoking_cat[4], "right"
)  # Smoking alot (16-20) sigarettes as dummy
df["smoking most"] = (
    df["smoking"] > smoking_cat[4]
)  # Smoking most (20+) sigarettes as dummy

# Versions of datasets
# Var numbering 0: lifespan, 1: genetics, 2: length, 3: mass, 4: exercise,
# Var numbering 5: smoking, 6: alcohol, 7: sugar, 9 & 10: normalized bmi

# All models, old and new
df_dict = {
    0: df.iloc[:, np.r_[0:8, 9:11]],  # All variables, bmi normalized
    1: df.iloc[:, np.r_[0:2, 3:8]],  # Without length & bmi
    2: df.iloc[:, np.r_[0:3, 4:8]],  # Without mass & bmi
    3: df.iloc[:, np.r_[0:2, 4:8]],  # Without length, mass & bmi
    4: df.iloc[:, np.r_[0:4, 5:8, 9:11]],  # Without exercise
    5: df.iloc[:, np.r_[0:5, 6:8, 9:11]],  # Without smoking
    6: df.iloc[:, np.r_[0:6, 7:8, 9:11]],  # Without alcohol
    7: df.iloc[:, np.r_[0:7, 9:11]],  # Without sugar
    8: df.iloc[:, np.r_[0:4, 6:8, 9:11]],  # Without exercise and smoking
    9: df.iloc[:, np.r_[0:4, 5:6, 7:8, 9:11]],  # Without exercise and alcohol
    10: df.iloc[:, np.r_[0:4, 5:7, 9:11]],  # Without exercise and sugar
    11: df.iloc[:, np.r_[0:5, 7:8, 9:11]],  # Without smoking and alcohol
    12: df.iloc[:, np.r_[0:5, 6:7, 9:11]],  # Without smoking and sugar
    13: df.iloc[:, np.r_[0:6, 9:11]],  # Without alcohol and sugar
    14: df.iloc[:, np.r_[0:4, 7:8, 9:11]],  # Without exercise, smoking and alcohol
    15: df.iloc[:, np.r_[0:4, 6:7, 9:11]],  # Without exercise, smoking and sugar
    16: df.iloc[:, np.r_[0:4, 9:11]],  # Without exercise, smoking, alcohol and sugar
}
# For the new models: 'lifespan' is substituted by 'lifespan - genetics', 'genetics' is omitted
if new:
    for dataset in df_dict:
        df = df_dict[dataset]
        # Substitute
        df.columns = ["dif_lifespan", *df.columns[1:]]
        df.iloc[:, 0] = df.iloc[:, 0] - df.iloc[:, 1]
        # Remove
        df_dict[dataset] = df.iloc[:, np.r_[0, 2 : len(df.columns)]]


# Remove old and save new versions of datasets
path_dataset = "./csv/"
new_ = "new_" if new else ""
extension = ".csv"

# Do you want to remove the old models in this directory?
if True:
    remove_files(path_dataset, new_, extension)

# Save datasets
for dataset in df_dict:
    df_dict[dataset].to_csv(
        f"{path_dataset}{new_}db_t{str(dataset)}{extension}", index=False
    )
