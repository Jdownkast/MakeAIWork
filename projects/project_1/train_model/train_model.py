import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import statsmodels.api as sm
import pickle

# Set a naming dictionary, to easily change names
naming = {
    "m_name": "Model_",
    "all_data": "Data",
    "x_data": "Independend data",
    "y_data": "Dependend data",
    "x_train": "Independend train data",
    "y_train": "Dependend train data",
    "x_test": "Independend test data",
    "y_test": "Dependend test data",
    "y_pred": "Predicted data",
    "model": "Model",
}

# Unpack dictionary to use in script
for key, name in naming.items():
    exec(key + "=name")

# Select datasets to be modelled
datasets = [1, 3, *range(20, 29)]  # All datasets (except 0)

# Initialize dictionary and load datasets
initial_dict = {}
path_datasets = "../tform_db/csv/"

for dataset in datasets:
    model_name = m_name + str(dataset)
    file = f"{path_datasets}db_t{str(dataset)}.csv"
    initial_dict[model_name] = {all_data: pd.read_csv(file)}


# Custom functions
# Remove files in a specific path with a specific extension
def remove_files(path, ext):
    for f in os.listdir(path):
        if ext in f:
            os.remove(os.path.join(path, f))


# Defining the linear regression model
def lr_dict(initial_dict):
    # Unpack naming dictionary to use in function
    # for key, name in naming.items():
    #     exec(key + '=name')

    for mod in initial_dict:
        # Per model, split (in)dependend data
        initial_dict[mod][x_data] = initial_dict[mod][all_data].iloc[:, 1:]
        initial_dict[mod][y_data] = initial_dict[mod][all_data].iloc[:, :1]

        # Per model, split train-/test-data
        x_train_d, x_test_d, y_train_d, y_test_d = train_test_split(
            initial_dict[mod][x_data],
            initial_dict[mod][y_data],
            test_size=0.7,
            random_state=42,
        )

        initial_dict[mod][x_train] = x_train_d
        initial_dict[mod][y_train] = y_train_d
        initial_dict[mod][x_test] = x_test_d
        initial_dict[mod][y_test] = y_test_d

        # Fit model
        lr = LinearRegression()
        lr.fit(initial_dict[mod][x_train], initial_dict[mod][y_train])

        # Predict and save data
        initial_dict[mod][y_pred] = lr.predict(initial_dict[mod][x_test])
        initial_dict[mod][model] = lr

    # Return the new dictionary
    return initial_dict


# Defining the function to summarize the models
def model_summary(models_dict, level="extended"):
    # Preloading variables/summary
    var = "Variable"
    coef = "Coefficient"
    sig = "P-value"
    col_names = [var, coef, sig]

    param = "Parameters"
    metric = "Metrics"
    summary = {}

    for mod in models_dict:
        # Per model, get coefficients
        summary[mod] = mod
        df_int = pd.DataFrame(
            {var: "Intercept", coef: models_dict[mod][model].intercept_, sig: 0}
        )
        df_coef = pd.DataFrame(
            zip(
                models_dict[mod][x_test].columns,
                models_dict[mod][model].coef_[0],
                np.zeros(len(models_dict[mod][x_test])),
            ),
            columns=col_names,
        )
        summary[mod] = {}
        summary[mod][param] = pd.concat([df_int, df_coef], axis=0, ignore_index=True)

        # Per model, get p-values (inefficiently done with statsmodels, but...)
        x_train_sm = models_dict[mod][x_train].copy()
        x_train_sm.insert(0, "intercept", np.ones(len(x_train_sm)))
        modsm = sm.OLS(models_dict[mod][y_train], x_train_sm.astype(float))
        modsm = modsm.fit()
        summary[mod][param][sig] = modsm.pvalues.values.round(3)

        # Per model, get the regression metrics
        summary[mod][metric] = {}
        summary[mod][metric]["r2"] = metrics.r2_score(
            models_dict[mod][y_test], models_dict[mod][y_pred]
        )
        summary[mod][metric]["mse"] = metrics.mean_squared_error(
            models_dict[mod][y_test], models_dict[mod][y_pred]
        )
        summary[mod][metric]["rmse"] = np.sqrt(summary[mod][metric]["mse"])
        summary[mod][metric]["msle"] = metrics.mean_squared_log_error(
            models_dict[mod][y_test], models_dict[mod][y_pred]
        )
        summary[mod][metric]["mae"] = metrics.mean_absolute_error(
            models_dict[mod][y_test], models_dict[mod][y_pred]
        )

        # Per model, print the summary depending on 'extended' or 'limited' level
        if level == "extended" or level == "ext":
            # pd.set_option("display.precision", 3)
            print(mod, ":")
            print(summary[mod][param])
            print("\n")
            print(
                "R-squared: ",
                "%.4f" % round(summary[mod][metric]["r2"], 4),
                "; Mean squared error: ",
                "%.4f" % round(summary[mod][metric]["mse"], 4),
                "; Root mean squared error: ",
                "%.4f" % round(summary[mod][metric]["rmse"], 4),
                sep="",
            )
            print("___ \n")
            # pd.reset_option("display.precision")
        elif level == "limited" or level == "lim":
            print(
                mod,
                ":",
                " R-squared: ",
                "%.4f" % round(summary[mod][metric]["r2"], 4),
                "; Mean squared error: ",
                "%.4f" % round(summary[mod][metric]["mse"], 4),
                "; Root mean squared error: ",
                "%.4f" % round(summary[mod][metric]["rmse"], 4),
                sep="",
            )
        else:
            print(
                "Please use level "
                "extended"
                " ("
                "ext"
                ") or "
                "limited"
                " ("
                "lim"
                ") or omit a choice."
            )

    # Return summary to be saved if desired
    return summary


# Fit models and save in models_dict
models_dict = lr_dict(initial_dict)

# Can be turned off
if True:
    path_models = "./models/"
    extension = ".pickle"

    # Delete all models in directory
    remove_files(path_models, extension)

    # Save all new models
    for mod in models_dict:
        filename = f"{path_models}{mod}{extension}"
        pickle.dump(models_dict[mod][model], open(filename, "wb"))
