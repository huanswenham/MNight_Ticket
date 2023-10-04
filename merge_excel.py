import pandas as pd

def merge_excel(old_file, new_file):
    left_df = pd.read_csv(new_file)     # New file
    right_df = pd.read_csv(old_file)    # Old file

    orderNums = []

    for index, values in left_df.iterrows():
        orNum = values["Order No"]
        if orNum in orderNums:
            left_df.loc[int(index), 'Order No'] = int(str(orNum) + '11')
        else:
            orderNums.append(orNum)
    

    left_df = pd.merge(left_df, right_df[["Order No", "PDF"]], on="Order No", how="left")

    left_df.to_csv(old_file, index=False)