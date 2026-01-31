import pandas as pd

def ff_monthly_loader(path, skiprows):
    """ Loads monthly data from Ken French CSV file with multiple yearly/monthly data tables.
    It finds the first monthly observation and the end of the table, dropping everything else"""

    df = pd.read_csv(path, skiprows=skiprows)

    date_col = df.columns[0]
    # Converting to string
    s = df[date_col].astype(str)

    # Matches observation with the format
    is_month = s.str.match(r'^\d{6}$')

    # First monthly observation
    start = is_month.idxmax()

    # Keep rows from first obvs until next row breaks pattern
    end = start
    while end + 1 in is_month.index and is_month.loc[end + 1]:
        end += 1

    # Slicing df
    df = df.loc[start:end].copy()

    # Renaming date col to Date
    df = df.rename(columns={date_col: 'Date'})
    #Parsing to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m')
    # Settin index
    df = df.set_index('Date').sort_index()

    return df