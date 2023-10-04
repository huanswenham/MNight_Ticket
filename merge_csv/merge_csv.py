import os
import pandas as pd


def merge_to_old_csv():
    """Merge new_file csv into old_file csv such that new rows will have no 
    values in PDF column.
    """
    
    old_file = os.getenv("OLD_CSV_FILE_PATH", default=None)
    new_file = os.getenv("NEW_CSV_FILE_PATH", default=None)
    left_df, right_df = pd.read_csv(new_file), pd.read_csv(old_file)

    orderNums = set()

    for index, values in left_df.iterrows():
        orNum = values["Order No"]
        if orNum in orderNums:
            left_df.loc[int(index), 'Order No'] = int(str(orNum) + '11')
        orderNums.add(orNum)
    

    left_df = pd.merge(left_df, right_df[["Order No", "PDF"]], on="Order No", how="left")

    left_df.to_csv(old_file, index=False)