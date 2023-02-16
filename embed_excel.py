import pandas as pd


# paths is a dictionary
def embed_excel(ordernum, path, file):

    df = pd.read_csv(file)

    df.loc[df['Order No'] == int(ordernum), 'PDF'] = path
    
    df.to_csv(file, index=False)


# For testing:
# data_file = 'ticket-qr.csv'
# def main():
#     embed_excel({100122: "p1", 100123: "p2", 100124: "p3", 100125: "p4"}, data_file)

# if __name__ == "__main__":
#     main()