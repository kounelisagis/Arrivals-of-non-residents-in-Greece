import pandas as pd
import sqlite3
import os
import re


month_to_id = {'ΙΑΝ': '01',
                'ΦΕΒ': '02',
                'ΜΑΡ': '03',
                'ΑΠΡ': '04',
                'ΜΑΙ': '05', 'ΜΑΙΟΣ': '05',
                'ΙΟΥΝ': '06',
                'ΙΟΥΛ': '07',
                'ΑΥΓ': '08',
                'ΣΕΠΤ': '09', 'ΣΕΠ': '09',
                'ΟΚΤ': '10',
                'ΝΟΕΜΒ': '11', 'ΝΟΕΜ': '11', 'ΝΟΕ': '11',
                'ΔΕΚ': '12', 'ΔΕΚΕΜ': '12'
            }


def save_to_db_and_csv(xls_dir = 'xls_files/', csv_dir = 'csv_files/', sql_dir = '', sql_name = 'db'):

    # create save folder if it doesn't exist
    os.makedirs(os.path.dirname(csv_dir), exist_ok=True)

    # create a new sqlite connection
    db = sqlite3.connect(os.path.join(sql_dir, sql_name + '.sqlite'))

    for name in [str(i) for i in range(2011, 2016)]:
        
        # dict of DataFrames
        dfs = pd.read_excel(os.path.join(xls_dir, name + '.xls'), sheet_name=None)

        for table, df in dfs.items():
            
            df.columns = ['id', 'ΧΩΡΑ', 'ΑΕΡΟΠΟΡΙΚΩΣ', 'ΣΙΔ/ΚΩΣ', 'ΘΑΛΑΣΣΙΩΣ', 'ΟΔΙΚΩΣ', 'ΣΥΝΟΛΟ']
            
            # filter (id collumn) -> number followed by a dot
            df = df[df.id.str.contains('^\d+\.$', na=False)]

            df = df.drop('id', 1) # 1 = dimension
            df = df.fillna(0) # replace NaN with zero

            # delete spaces after the end of the string (ex serbia)
            df['ΧΩΡΑ'] = df['ΧΩΡΑ'].replace('\s$', '', regex=True)

            # delete croatia references
            df['ΧΩΡΑ'] = df['ΧΩΡΑ'].replace(' \(\d+\)$', '', regex=True)

            # delete multiple spaces
            # df['ΧΩΡΑ'] = df['ΧΩΡΑ'].replace('\s+', ' ', regex=True)

            # keep only the first table
            df = df.drop_duplicates(subset=['ΧΩΡΑ'], keep='first')

            for collumn in ['ΑΕΡΟΠΟΡΙΚΩΣ', 'ΣΙΔ/ΚΩΣ', 'ΘΑΛΑΣΣΙΩΣ', 'ΟΔΙΚΩΣ', 'ΣΥΝΟΛΟ']:
                df[collumn] = df[collumn].round()
                df[collumn] = df[collumn].astype(int)
            # print(df)

            df.to_sql(name + '-' + month_to_id[table], db, if_exists='replace', index=False)
            df.to_csv(os.path.join(csv_dir, name + '-' + month_to_id[table] + '.csv'), index=False)
    
    print('Data are now in a safe place!')


if __name__ == '__main__':
    save_to_db_and_csv()
