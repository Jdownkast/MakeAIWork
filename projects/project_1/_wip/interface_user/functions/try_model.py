def try_model(all_models, param):
    """To find which model suits"""
    model = ""
    # First get parameters and check if they have a value
    parameters = [int(item) for item in list(param.values())]
    has_value = [len(parameter) > 0 for parameter in parameters]

    # Then, based on value of parameters choose approprate model
    # "New models" are identified the same, but with "new_" in front of model
    new_ = "" if has_value[0] else "new_"

    # Models without bmi, need all other parameters to do prediction
    if not has_value[1] or not has_value[2]:
        if has_value[3] and has_value[4] and has_value[5] and has_value[6]:
            # If they have all other values, choose model
            if not has_value[1] and not has_value[2]:
                model = all_models[f"{new_}model_3"]
            elif not has_value[1]:
                model = all_models[f"{new_}model_1"]
            elif not has_value[2]:
                model = all_models[f"{new_}model_2"]
    else:
        # Models with bmi, can differ on lifestyle
        if has_value[3] and has_value[4] and has_value[5] and has_value[6]:
            # If they have all values
            model = all_models[f"{new_}model_0"]
        # If one or more lifestyle value is missing
        elif (
            not has_value[3] or not has_value[4] or not has_value[5] or not has_value[6]
        ):
            # If only exercise missing
            if not has_value[3] and has_value[4] and has_value[5] and has_value[6]:
                model = all_models[f"{new_}model_4"]
            # If only smoking missing
            elif has_value[3] and not has_value[4] and has_value[5] and has_value[6]:
                model = all_models[f"{new_}model_5"]
            # If only alcohol missing
            elif has_value[3] and has_value[4] and not has_value[5] and has_value[6]:
                model = all_models[f"{new_}model_6"]
            # If only sugar missing
            elif has_value[3] and has_value[4] and has_value[5] and not has_value[6]:
                model = all_models[f"{new_}model_7"]
            # If exercise and smoking missing
            elif (
                not has_value[3] and not has_value[4] and has_value[5] and has_value[6]
            ):
                model = all_models[f"{new_}model_8"]
            # If exercise and alcohol missing
            elif (
                not has_value[3] and has_value[4] and not has_value[5] and has_value[6]
            ):
                model = all_models[f"{new_}model_9"]
            # If exercise and sugar missing
            elif (
                not has_value[3] and has_value[4] and has_value[5] and not has_value[6]
            ):
                model = all_models[f"{new_}model_10"]
            # If smoking and alcohol missing
            elif (
                has_value[3] and not has_value[4] and not has_value[5] and has_value[6]
            ):
                model = all_models[f"{new_}model_11"]
            # If smoking and sugar missing
            elif (
                has_value[3] and not has_value[4] and has_value[5] and not has_value[6]
            ):
                model = all_models[f"{new_}model_12"]
            # If alcohol and sugar missing
            elif (
                has_value[3] and has_value[4] and not has_value[5] and not has_value[6]
            ):
                model = all_models[f"{new_}model_13"]
            # If exercise, smoking and alcohol missing
            elif (
                not has_value[3]
                and not has_value[4]
                and not has_value[5]
                and has_value[6]
            ):
                model = all_models[f"{new_}model_14"]
            # If exercise, smoking and sugar missing
            elif (
                not has_value[3]
                and not has_value[4]
                and has_value[5]
                and not has_value[6]
            ):
                model = all_models[f"{new_}model_15"]
            # If exercise, alcohol and sugar missing
            elif (
                not has_value[3]
                and has_value[4]
                and not has_value[5]
                and not has_value[6]
            ):
                model = all_models[f"{new_}model_16"]
            # If smoking, alcohol and sugar missing
            elif has_value[3] and has_value[4] and has_value[5] and not has_value[6]:
                model = all_models[f"{new_}model_17"]
            # If exercise, smoking, alcohol and sugar missing
            elif (
                not has_value[3]
                and not has_value[4]
                and not has_value[5]
                and not has_value[6]
            ):
                model = all_models[f"{new_}model_18"]

    model_fit = True if len(model) > 0 else False
    return model_fit, model
