import requests
import json
import tkinter
from tkinter import Menu
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter.ttk import Combobox
import datetime
from matplotlib.ticker import FixedLocator, FixedFormatter
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
import numpy as np
from collections import Counter

RECORDS_URL = 'https://lmnad.nntu.ru/api/v1/records/'
API_KEY = 'd837d31970deb03ee35c416c5a66be1bba9f56d3'
x_label = ['Карта', 'График', 'Спутниковый снимок', 'Запись', 'Таблица']
labels = [1, 2, 3, 4, 5]
label = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
         'Декабрь']
x_label_season = ['Зима', 'Весна', 'Лето', 'Осень']


def fetch_records(limit=3000):
    resp = requests.get(RECORDS_URL, params=dict(api_key=API_KEY, is_yandex_map=0, limit=3000))
    records = resp.json()
    save_records(records)


def load_records():
    with open('records.json', 'r') as f:
        recs = json.load(f)
    return recs


def save_records(result):
    with open('records.json', 'w+') as f:
        json.dump(result, f)


def is_inside_sea(p_lat, p_lon, lon, lon1, lat, lat1):
    return lon <= p_lon <= lon1 and lat <= p_lat <= lat1


def increment_type_to_sea(def_sea_records, sea_types):
    for type_str in def_sea_records:
        value = type_str['value']
        if value not in sea_types:
            sea_types[value] = 0
        sea_types[value] += 1


def _quit():
    window.quit()
    window.destroy()


def init_menu_bar():
    menu = Menu(window)
    # Add button 'Exit'
    new_item = Menu(menu, tearoff=0)
    new_item.add_command(label='Exit', command=_quit)

    menu.add_cascade(label='File', menu=new_item)

    window.config(menu=menu)


def init_plot_bar():
    fig = Figure(figsize=(5, 4), dpi=100)
    img_area_1, img_area_2 = fig.subplots(1, 2, sharey=True)

    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

    return canvas, img_area_1, img_area_2


def plot_season():
    plot_bars_season(img_area_1, ComboBox1.get())
    plot_bars_season(img_area_2, ComboBox2.get())

    canvas.draw()


def plot_bars_season(img_area, combobox):
    img_area.cla()
    sea_name_def = combobox
    sea_season_x = [0, 1, 2, 3]
    sea_season_winter = []
    sea_season_spring = []
    sea_season_summer = []
    sea_season_autumn = []
    for i in sea_dic[sea_name_def]['month']:
        if sea_name_def in sea_dic:
            if i == 12 or i == 1 or i == 2:
                sea_season_winter.append(1)
            if i == 3 or i == 4 or i == 5:
                sea_season_spring.append(1)
            if i == 6 or i == 7 or i == 8:
                sea_season_summer.append(1)
            if i == 9 or i == 10 or i == 11:
                sea_season_autumn.append(1)
    sea_season_y = [len(sea_season_winter), len(sea_season_spring), len(sea_season_summer), len(sea_season_autumn)]
    img_area.bar(sea_season_x, sea_season_y, tick_label=x_label_season)
    img_area.set_xlabel('Сезоны')
    img_area.set_ylabel('Количество наблюдений')
    img_area.set_title(sea_name_def, fontsize=16)


def plot_month():
    plot_bars_month(img_area_1, ComboBox1.get())
    plot_bars_month(img_area_2, ComboBox2.get())

    canvas.draw()


def plot_bars_month(img_area, combobox):
    img_area.cla()
    sea_name_def = combobox
    sea_month_y = []
    sea_month_x = []
    month_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for i in month_x:
        y = 0
        if sea_name_def in sea_dic:
            if i in sea_dic[sea_name_def]['month']:
                y = sea_dic[sea_name_def]['month'][i]
        sea_month_y.append(y)
        sea_month_x.append(i)
    img_area.bar(sea_month_x, sea_month_y, tick_label=label)
    img_area.tick_params(axis="x", labelrotation=50)
    img_area.set_xlabel('Месяца')
    img_area.set_ylabel('Количество наблюдений')
    img_area.set_title(sea_name_def, fontsize=16)


def plot_bars_year():
    plot_bars_year1(img_area_1, ComboBox1.get())
    plot_bars_year1(img_area_2, ComboBox2.get())

    canvas.draw()


def plot_bars_year1(img_area, combobox):
    img_area.cla()
    sea_name_def = combobox
    sea_years_y = []
    sea_years_x = []
    range_x = range(min_year, max_year, 1)
    for i in range_x:
        y = 0
        if sea_name_def in sea_dic:
            if i in sea_dic[sea_name_def]['year']:
                y = sea_dic[sea_name_def]['year'][i]
        sea_years_y.append(y)
        sea_years_x.append(i)
    img_area.bar(sea_years_x, sea_years_y, tick_label=sea_years_x)
    img_area.xaxis.set_major_locator(MaxNLocator(max_year - min_year + 1))
    img_area.tick_params(axis="x", labelrotation=90, labelsize=6.5)
    img_area.set_xlabel('Года')
    img_area.set_ylabel('Количество наблюдений')
    img_area.set_title(sea_name_def, fontsize=16)


def plot_bars():
    print("Plot or update bar!")

    plot_bars_type(img_area_1, ComboBox1.get())
    plot_bars_type(img_area_2, ComboBox2.get())

    canvas.draw()


def plot_bars_type(img_area, combobox):
    img_area.cla()
    sea_name_def = combobox
    sea_type_y = []
    sea_type_x = [0, 1, 2, 3, 4]
    for e in sea_type_x:
        os_y = 0
        if sea_name_def in sea_dic:
            if e in sea_dic[sea_name_def]['new_types']:
                os_y = sea_dic[sea_name_def]['new_types'][e]
        sea_type_y.append(os_y)
    img_area.bar(sea_type_x, sea_type_y, tick_label=x_label)
    img_area.tick_params(labelsize=7)
    img_area.set_xlabel('Типы наблюдений')
    img_area.set_ylabel('Количество наблюдений')
    img_area.set_title(sea_name_def, fontsize=16)


def get_sea_name(point_get):
    if is_inside_sea(point_get['lat'], point_get['lon'], 27.166665, 41.895011, 41.196970, 48.015644):
        return black_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 47.706201, 54.112157, 35.831338, 46.817235):
        return kasp_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 11.033512, 22.344357, 53.925258, 60.364091):
        return balt_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 34.689990, 38.185911, 45.225182, 47.007205):
        return azov_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 27.082836, 67.464416, 71.276162, 79.814267):
        return barenz_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 143.306583, 179.883581, 66.459554, 76.588341):
        return ist_sib_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 55.108884, 95.543544, 68.865791, 81.424224):
        return kar_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 102.730621, 138.622760, 72.848152, 79.230808):
        return sea_lapt_name
    if is_inside_sea(point_get['lat'], point_get['lon'], -179.929840, -161.653438, 66.645032, 71.446011):
        return chuk_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 33.518473, 40.385833, 63.654762, 66.678821):
        return white_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 156.640431, -156.888830, 50.764496, 66.304490):
        return bering_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 135.007656, 156.231867, 51.571616, 61.230127):
        return okhotsk_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 127.344542, 142.468475, 33.217811, 51.962581):
        return japan_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], -89.078428, -66.502074, 5.203730, 23.157922):
        return karib_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 45.734804, 76.933129, 0.989934, 25.688408):
        return arav_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 107.235153, 121.277466, 2.012984, 22.613627):
        return south_kit_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 120.021048, 129.481133, 25.781484, 33.172170):
        return ist_kit_sea_name
    if is_inside_sea(point_get['lat'], point_get['lon'], 151.004796, 173.163069, -47.869489, -34.236905):
        return tas_sea_name
    return mir_okean_name


if __name__ == '__main__':
    # fetch_records()
    records = load_records()



if __name__ == '__main__':
    black_sea_name = "Чёрное море"
    kasp_sea_name = "Каспийское море"
    balt_sea_name = "Балтийское море"
    azov_sea_name = "Азовское море"
    barenz_sea_name = "Баренцево море"
    ist_sib_sea_name = "Восточно-Сибирское море"
    kar_sea_name = "Карское море"
    sea_lapt_name = "Море Лаптевых"
    chuk_sea_name = "Чукотское море"
    white_sea_name = "Белое море"
    bering_sea_name = "Берингово море"
    okhotsk_sea_name = "Охотское море"
    japan_sea_name = "Японское море"
    karib_sea_name = "Карибское море"
    arav_sea_name = "Аравийское море"
    south_kit_sea_name = "Южно-Китайское море"
    ist_kit_sea_name = "Восточно-Китайсоке море"
    tas_sea_name = "Тасманово море"
    mir_okean_name = "Мировой океан"

    window = tkinter.Tk()
    window.wm_title("IGWAtlas_статистика")

    count_records = records['count']
    
    results_records = records['results']

    sea_dic = dict()
    max_year = -1
    min_year = 5000
    for point in results_records:
        sea_name = get_sea_name(point)
        if sea_name is not None:
            if sea_name not in sea_dic:
                sea_dic[sea_name] = dict()
                sea_dic[sea_name]['year'] = dict()
                sea_dic[sea_name]['new_types'] = dict()
                sea_dic[sea_name]['month'] = dict()
                sea_dic[sea_name]['season'] = dict()

            increment_type_to_sea(point['new_types'], sea_dic[sea_name]['new_types'])

            if point['date'] is not None:
                date_time_obj = datetime.datetime.strptime(point['date'], '%Y-%m-%dT%H:%M:%SZ')
                if date_time_obj.year not in sea_dic[sea_name]['year']:
                    sea_dic[sea_name]['year'][date_time_obj.year] = 0
                sea_dic[sea_name]['year'][date_time_obj.year] += 1
                max_year = max(date_time_obj.year, max_year)
                min_year = min(date_time_obj.year, min_year)
                if date_time_obj.month not in sea_dic[sea_name]['month']:
                    sea_dic[sea_name]['month'][date_time_obj.month] = 0
                sea_dic[sea_name]['month'][date_time_obj.month] += 1

    canvas, img_area_1, img_area_2 = init_plot_bar()

    button_type = tkinter.Button(master=window, text='По типам наблюдений', command=plot_bars)
    button_type.pack(side=tkinter.LEFT)
    button_year = tkinter.Button(master=window, text='По годам', command=plot_bars_year)
    button_year.pack(side=tkinter.LEFT)
    button_season = tkinter.Button(master=window, text='По сезонам', command=plot_season)
    button_season.pack(side=tkinter.LEFT)
    button_month = tkinter.Button(master=window, text='По месяцам', command=plot_month)
    button_month.pack(side=tkinter.LEFT)
    ComboBox2 = Combobox(master=window)
    ComboBox2['values'] = (
        black_sea_name, kasp_sea_name, balt_sea_name, barenz_sea_name, kar_sea_name,
        sea_lapt_name, bering_sea_name, okhotsk_sea_name, japan_sea_name, karib_sea_name, arav_sea_name,
        south_kit_sea_name, ist_kit_sea_name, tas_sea_name, mir_okean_name)
    ComboBox2.current(0)  
    ComboBox2.pack(side=tkinter.RIGHT)
    ComboBox1 = Combobox(master=window)
    ComboBox1['values'] = (
        black_sea_name, kasp_sea_name, balt_sea_name, barenz_sea_name, kar_sea_name,
        sea_lapt_name, bering_sea_name, okhotsk_sea_name, japan_sea_name, karib_sea_name, arav_sea_name,
        south_kit_sea_name, ist_kit_sea_name, tas_sea_name, mir_okean_name)
    ComboBox1.current(0)  
    ComboBox1.pack()
    tkinter.mainloop()

print(map_types)
