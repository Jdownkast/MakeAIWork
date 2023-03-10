import pandas as pd

# Load csv
# df = pd.read_csv("../dload_db/csv/db_mcr.csv")
df = pd.read_csv("../dload_db/csv/static_db_mcr.csv")

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
    smoking_cat[0], smoking_cat[1], "right"
)  # Smoking some (6-10) sigarettes as dummy
df["smoking more"] = df["smoking"].between(
    smoking_cat[1], smoking_cat[2], "right"
)  # Smoking more (11-15) sigarettes as dummy
df["smoking alot"] = df["smoking"].between(
    smoking_cat[2], smoking_cat[3], "right"
)  # Smoking alot (16-20) sigarettes as dummy
df["smoking most"] = (
    df["smoking"] > smoking_cat[3]
)  # Smoking most (20+) sigarettes as dummy

# Save different sets of data for modeling
path_db_t = "csv/db_t1.csv"

df_t1 = df.iloc[:, :9]
df_t1.to_csv(path_db_t, index=False)
