import os
import pandas as pd
import numpy as np


# Define function to clear all 'earlier' models from directory
def remove_files(path, ext):
    for f in os.listdir(path):
        if ext in f:
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

# This piece of code is added to create a 'line' of new models, see comments on top of the notebook 
new = True
if new:
    # Create and rename new variable 'dif_lifespan' as difference between genetic and lifespan 
    df['lifespan'] = df['genetic'] - df['lifespan']
    df.columns = ['dif_lifespan', *df.columns[1:]]
    # Drop genetic as it is no longer used
    df.drop(columns='genetic')
        

# Versions of datasets
# Models that are not used already filtered
df_dict = {
    0: df,  # Complete dataset
    1: df.iloc[:, np.r_[:9]],  # All continuous/ratio ('main') variables
    2: df.iloc[:, np.r_[0:2, 4:9]],  # All main variables except length & mass
    3: df.iloc[:, np.r_[0:8, 9:11]],  # M1, but bmi normalized
    4: df.iloc[:, np.r_[0:8, 11:15]],  # M1, but bmi categorized
    5: df.iloc[:, np.r_[0:5, 6:9, 15:20]],  # M1, but smoking categorized
    6: df.iloc[:, np.r_[0:5, 6:8, 9:11, 15:20]],  # M3, but smoking categorized
    7: df.iloc[:, np.r_[0:5, 6:8, 11:15, 15:20]],  # M4, but smoking categorized
    8: df.iloc[:, np.r_[0:2, 4:8, 9:11]],  # M2, but bmi normalized
    9: df.iloc[:, np.r_[0:2, 4:8, 11:15]],  # M2, but bmi categorized
    10: df.iloc[:, np.r_[0:2, 4, 6:9, 15:20]],  # M2, but smoking categorized
    11: df.iloc[:, np.r_[0:2, 4, 6:8, 9:11, 15:20]],  # M8, but smoking categorized
    12: df.iloc[:, np.r_[0:2, 4, 6:8, 11:15, 15:20]],  # M9, but smoking categorized
    13: df.iloc[:, np.r_[0:1, 2:9]],  # All main variables except genetics
    14: df.iloc[:, np.r_[0:1, 4:9]],  # All main variables except gen., length & mass
    15: df.iloc[:, np.r_[0:1, 2:8, 9:11]],  # M13, but bmi normalized
    16: df.iloc[:, np.r_[0:1, 2:8, 11:15]],  # M13, but bmi categorized
    17: df.iloc[:, np.r_[0:1, 3:5, 6:9, 15:20]],  # M13, but smoking categorized
    18: df.iloc[:, np.r_[0:1, 3:5, 6:8, 9:11, 15:20]],  # M14, but smoking categorized
    19: df.iloc[:, np.r_[0:1, 3:5, 6:8, 11:15, 15:20]],  # M15, but smoking categorized
    20: df.iloc[:, np.r_[0:1, 2:8, 9:11]],  # M3, but without genetics
    21: df.iloc[:, np.r_[0:2, 4:8]],  # M1, but without length, mass & bmi
    22: df.iloc[:, np.r_[0:4, 5:8, 9:11]],  # M3, but without exercise
    23: df.iloc[:, np.r_[0:5, 6:8, 9:11]],  # M3, but without smoking
    24: df.iloc[:, np.r_[0:6, 7:8, 9:11]],  # M3, but without alcohol
    25: df.iloc[:, np.r_[0:7, 9:11]],  # M3, but without sugar
    26: df.iloc[:, np.r_[0:5, 7, 9:11]],  # M3, but without smoking & alcohol
    27: df.iloc[:, np.r_[0:5, 9:11]],  # M3, but without smoking, alcohol & sugar
    28: df.iloc[
        :, np.r_[0:4, 9:11]
    ],  # M3, but without exercise, smoking alcohol & sugar
}

# Remove old and save new versions of datasets
path_dataset = "./csv/"
extension = ".csv"

remove_files(path_dataset, extension)

# Change save_dict for specific datasets,
# otherwise [*range(len(df_dict))] to save all
save_dict = [*range(len(df_dict))]
for i in save_dict:
    df_dict[i].to_csv(f"{path_dataset}db_t{str(i)}{extension}", index=False)