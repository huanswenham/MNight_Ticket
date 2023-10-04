import pandas as pd


def put_pdf_path_to_csv(ordernum, path, file):
    df = pd.read_csv(file)

    df.loc[df['Order No'] == int(ordernum), 'PDF'] = path
    
    df.to_csv(file, index=False)