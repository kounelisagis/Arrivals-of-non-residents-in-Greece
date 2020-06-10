import pandas as pd
import matplotlib.pyplot as plt
import os
import re



def get_dataframes_dict(csv_dir = 'csv_files/'):
    directory = os.fsencode(csv_dir)

    dfs = {}  # dictionary of dictionaries of dataframes

    for file in sorted(os.listdir(csv_dir)):
        filename = os.fsdecode(file)

        year_month = re.sub('\.csv$', '', filename)
        year, month = year_month.split('-')

        filepath = os.path.join(csv_dir, filename)
        df = pd.read_csv(filepath)

        year = int(year)
        month = int(month)
        if year not in dfs:
            dfs[year] = {}
        dfs[year][month] = df

    return dfs



def per_year(dfs, charts_dir='charts/', picture_name='per_year'):
    
    years = []

    for year, months in dfs.items():
        df = pd.concat([months[month] for month in range(1,13)], ignore_index=True)
        df = df.sum()
        years.append((year, df['ΣΥΝΟΛΟ']))

    x, y = zip(*years)
    
    plt.figure(figsize=(20,10))
    plt.bar(x, y)
    plt.title('Αφίξεις ανά Χρόνο')
    plt.ylabel('Αφίξεις')


    os.makedirs(os.path.dirname(charts_dir), exist_ok=True)
    plt.savefig(os.path.join(charts_dir, picture_name), bbox_inches='tight', dpi=100)
    plt.show()



def per_quarter(dfs, charts_dir='charts/', picture_name='per_quarter'):
    
    quarters = []

    for year, months in dfs.items():
        for quarter in range(1,5):
            df = pd.concat([months[month] for month in range(3*quarter - 2, 3*quarter + 1)], ignore_index=True)
            df = df.sum()
            quarters.append(('{}-Q{}'.format(year, quarter), df['ΣΥΝΟΛΟ']))

    x, y = zip(*quarters)
    
    plt.figure(figsize=(20,10))
    plt.bar(x, y)
    plt.title('Αφίξεις ανά Τρίμηνο')
    plt.ylabel('Αφίξεις')


    os.makedirs(os.path.dirname(charts_dir), exist_ok=True)
    plt.savefig(os.path.join(charts_dir, picture_name), bbox_inches='tight', dpi=100)
    plt.show()




def per_transport(dfs, charts_dir='charts/', picture_name='per_transport'):
    df = pd.concat(dfs, ignore_index=True)
    df = df.drop('ΧΩΡΑ', 1) # 1 = dimension
    df = df.drop('ΣΥΝΟΛΟ', 1) # 1 = dimension
    df = df.sum()

    plt.figure(figsize=(20,10))
    df.plot.bar()

    ax = plt.gca()
    ax.set_yscale('log')


    os.makedirs(os.path.dirname(charts_dir), exist_ok=True)
    plt.savefig(os.path.join(charts_dir, picture_name), bbox_inches='tight', dpi=100)
    plt.show()



def per_country(dfs, top_n=10, charts_dir='charts/', picture_name='per_country'):
    # to one df
    df = pd.concat(dfs, ignore_index=True)

    # group by country and sum the other columns
    df = df.groupby(['ΧΩΡΑ'], as_index=False)[['ΑΕΡΟΠΟΡΙΚΩΣ', 'ΣΙΔ/ΚΩΣ', 'ΘΑΛΑΣΣΙΩΣ', 'ΟΔΙΚΩΣ', 'ΣΥΝΟΛΟ']].sum()
    df = df.sort_values('ΣΥΝΟΛΟ', ascending=False).head(10)

    x = df['ΧΩΡΑ']
    y = df['ΣΥΝΟΛΟ']
    plt.figure(figsize=(20,10))
    plt.bar(x, y)
    plt.title('Χώρες με το μεγαλύτερο Μερίδιο Αφίξεων')
    plt.ylabel('Αφίξεις')


    os.makedirs(os.path.dirname(charts_dir), exist_ok=True)
    plt.savefig(os.path.join(charts_dir, picture_name), bbox_inches='tight', dpi=100)
    plt.show()


if __name__ == '__main__':

    dfs_dict = get_dataframes_dict()
    plain_dfs = [month_df for months_dict in dfs_dict.values() for month_df in list(months_dict.values())]

    per_year(dfs_dict)
    per_country(plain_dfs)
    per_transport(plain_dfs)
    per_quarter(dfs_dict)
