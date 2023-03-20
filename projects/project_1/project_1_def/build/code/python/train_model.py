from os import listdir, path, remove
from os.path import isfile, join
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from pickle import dump

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

# Initialize dictionary and load datasets
initial_dict = {}
path_datasets = "../../csv/datasets/"

# Get all datafiles (so both old and new models)
datafiles = [f for f in listdir(path_datasets) if isfile(join(path_datasets, f))]

for dataset in datafiles:
    # Get model names without extention (can also with os.path.splittext but no priority)
    dataset_name = dataset[:-4]
    model_name = dataset_name.replace("ds_t", "model_")
    file = f"{path_datasets}{dataset}"
    initial_dict[model_name] = {all_data: pd.read_csv(file)}


# Custom functions
# Remove files in a specific path with a specific extension
def remove_files(path_, ext):
    for f in listdir(path_):
        if ext in f:
            remove(path.join(path_, f))


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


# Fit models and save in models_dict
models_dict = lr_dict(initial_dict)

# Saving models
path_models = "../../../models/"
extension = ".pickle"

# Delete all models in directory
remove_files(path_models, extension)

# Save all new models
for mod in models_dict:
    filename = f"{path_models}{mod}{extension}"
    dump(models_dict[mod][model], open(filename, "wb"))
