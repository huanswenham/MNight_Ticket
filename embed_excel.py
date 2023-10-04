import pandas as pd


# paths is a dictionary
def embed_excel(ordernum, path, file):

    df = pd.read_csv(file)

    df.loc[df['Order No'] == int(ordernum), 'PDF'] = path
    
    df.to_csv(file, index=False)