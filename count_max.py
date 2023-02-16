import pandas as pd



def count_max(files):
    result = {}
    for f in files:
        df = pd.read_csv(f)
        for index, values in df.iterrows():
            name = str(values["First Name"]) + " " + str(values["Surname"])
            quantity = values["Quantity"]
            if name in result:
                result[name] += quantity
            else:
                result[name] = quantity
    sorted_tuples = sorted(result.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_tuples}
    for ks in sorted_dict:
        print(str(ks) + ":" + str(sorted_dict[ks]))

# define list of csv files here
files = []

count_max(files)