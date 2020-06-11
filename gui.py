import downloader
import storer
import painter
import tkinter as tk


def download_set():
    links = downloader.find_links()
    downloader.download_files(links)
    label['text'] = 'Files successfully downloaded! You can now store them.'
    store_btn['state'] = 'normal'


def store_set():
    storer.save_to_db_and_csv()
    label['text'] = 'Files successfully stored! You can now plot the data.'

    paint_year_btn['state'] = 'normal'
    paint_country_btn['state'] = 'normal'
    paint_transport_btn['state'] = 'normal'
    paint_quarter_btn['state'] = 'normal'


def paint_set(option='year'):
    dfs_dict = painter.get_dataframes_dict()
    plain_dfs = [month_df for months_dict in dfs_dict.values()
                    for month_df in list(months_dict.values())]

    if option == 'year':
        painter.per_year(dfs_dict)
    elif option == 'country':
        painter.per_country(plain_dfs)
    elif option == 'transport':
        painter.per_transport(plain_dfs)
    else:
        painter.per_quarter(dfs_dict)

    label['text'] = 'Plot was successful!'


# Main Program

parent = tk.Tk()
parent.title('!The Ultimate Program of the Universe!')

button_frame = tk.Frame(master = parent, bd = 20)
button_frame.pack()

text_frame = tk.Frame(master = parent, bd = 20)
text_frame.pack(side = tk.BOTTOM)


download_btn = tk.Button(button_frame,
                text = 'DOWNLOAD',
                command = download_set,
                height = 5,
                width = 20,
                bg = '#c7cace'
                )

download_btn.pack(side = tk.LEFT)


store_btn = tk.Button(button_frame,
                text = 'STORE',
                command = store_set,
                height = 5,
                width = 20,
                bg = '#a7cace',
                state = 'disabled'
                )

store_btn.pack(side = tk.LEFT)


paint_year_btn = tk.Button(button_frame,
                text = 'PAINT per year',
                command = lambda: paint_set(option='year'),
                height = 5,
                width = 20,
                bg = '#97cace',
                state = 'disabled'
                )

paint_year_btn.pack(side = tk.LEFT)


paint_country_btn = tk.Button(button_frame,
                text = 'PAINT per country',
                command = lambda: paint_set(option='country'),
                height = 5,
                width = 20,
                bg = '#97cace',
                state = 'disabled'
                )

paint_country_btn.pack(side = tk.LEFT)


paint_transport_btn = tk.Button(button_frame,
                text = 'PAINT per transport',
                command = lambda: paint_set(option='transport'),
                height = 5,
                width = 20,
                bg = '#97cace',
                state = 'disabled'
                )

paint_transport_btn.pack(side = tk.LEFT)


paint_quarter_btn = tk.Button(button_frame,
                text = 'PAINT per quarter',
                command = lambda: paint_set(option='quarter'),
                height = 5,
                width = 20,
                bg = '#97cace',
                state = 'disabled'
                )

paint_quarter_btn.pack(side = tk.LEFT)


label = tk.Label(text_frame, text = "Hello!")
label.pack()

parent.mainloop()
