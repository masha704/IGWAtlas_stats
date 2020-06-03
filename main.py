import datetime
import json

import tkinter
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import messagebox as mb
from tkinter import *

import requests
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import os.path

RECORDS_URL = 'https://lmnad.nntu.ru/api/v1/records/'
API_KEY = 'd837d31970deb03ee35c416c5a66be1bba9f56d3'

RECORD_TYPES = ('Карта', 'График', 'Спутниковый\nснимок', 'Запись', 'Таблица')
RECORD_TYPES_X = (0, 1, 2, 3, 4)
MONTHS = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
          'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')
MONTHS_X = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

SEASONS = ('Зима', 'Весна', 'Лето', 'Осень')
SEASONS_X = (0, 1, 2, 3)

WINTER_MONTHS = (12, 1, 2)
SPRING_MONTHS = (3, 4, 5)
SUMMER_MONTHS = (6, 7, 8)
AUTUMN_MONTHS = (9, 10, 11)

WORLD_OCEAN = "Мировой океан"

DICT_SEAS = {
    "Чёрное море": [(27.39656574188712, 42.44693293533655), (27.96659266928519, 41.76992184435287),
                    (29.14988448127809, 41.1321055522646), (31.36802268121137, 41.06619807539869),
                    (38.78970697167646, 40.58057822370173), (41.67955750321034, 41.3482642853712),
                    (41.77680975475529, 42.29000764508529), (41.10522203214715, 43.09303525828695),
                    (38.96347829129073, 44.29865789740193), (36.22998246300682, 45.15583566914309),
                    (34.50413720566613, 44.75432548476775), (32.85963980946213, 45.42940970338559),
                    (33.68498421388794, 46.0652834053808),
                    (31.49807894703399, 46.99890681045963), (30.02221442495623, 45.89034125415174),
                    (28.34360825167762, 43.62012559388068), (27.39656574188712, 42.44693293533655)],
    "Море Бофорта": [(-156.8082050918581, 70.92004854436657), (-135.1371478921001, 68.48789307510651),
                     (-92.37984185939624, 67.64054149661973), (-85.55268922303553, 67.05622529960745),
                     (-67.77413715632218, 63.01401398033172), (-49.71912320049623, 68.1760631248281),
                     (-56.34315870262373, 74.6901874364183), (-70.09647230886611, 77.728724576543),
                     (-112.1724764279607, 84.51774968056527), (-162.4554806566382, 75.42687388099688),
                     (-156.8082050918581, 70.92004854436657)],
    "Каспийское море": [(50.12008394322086, 46.74046178256775), (48.10495702908441, 45.49348961971855),
                        (47.52306117304433, 45.60135829063368), (46.73308623471945, 44.5034283419415),
                        (47.42371619377805, 43.73637897013653), (47.45747413106194, 42.87426576050428),
                        (49.74346270831642, 40.36525250680371), (49.32190813945557, 39.79741976588375),
                        (48.74417574048941, 38.85671849674659), (48.91511337987092, 37.68411933218063),
                        (49.73777721560645, 37.29275063417968), (50.13513634838132, 37.24716328228235),
                        (50.94805562317456, 36.71069633903755), (51.90079735015592, 36.51294485582746),
                        (54.09471923016694, 36.90566547940877), (54.09740774744745, 38.93094527962828),
                        (53.34462055399618, 39.46858802445155), (53.63662090046774, 39.85898424696027),
                        (52.90977408172154, 40.05744510093266), (53.01282056806994, 40.64917654427523),
                        (54.16614615969267, 40.62082068371873), (54.93180282133554, 40.99174194418462),
                        (54.25436757576998, 41.54168645466932), (53.56909595176641, 42.59669815968698),
                        (52.55986369909387, 41.69303261897809), (52.80972243915636, 42.67630701793416),
                        (50.46564157200533, 44.49304763936444), (51.18257510355737, 44.44310830189246),
                        (51.48462162983282, 44.6256717446535), (51.06744826276399, 44.89419036259675),
                        (53.06955324947703, 45.31526357650077), (53.1678067894626, 46.88125797502015),
                        (51.21540556542997, 47.05104740032717), (50.12008394322086, 46.74046178256775)],
    "Балтийское море": [(22.25901217649315, 65.67588493484378), (21.22315822994227, 65.21724221406947),
                        (21.22836284871322, 64.40715449737475), (20.5766153251724, 63.88996104205782),
                        (18.26459400990363, 62.97012906767883), (16.92520766193712, 61.72659960327649),
                        (17.06072737039893, 60.72767216040657), (18.76979801677728, 60.02710693867264),
                        (16.77425502253385, 58.60306402988777), (15.91161983335264, 56.17594163247227),
                        (14.61960388807469, 56.17903688088052), (13.94760311402141, 55.49460469400688),
                        (12.9187092478581, 55.42814333325364), (12.62668879594804, 56.16076553212327),
                        (9.267904726749336, 55.58324508396784), (10.92252390485939, 53.78545029941631),
                        (12.83351159298693, 54.49583134654759), (14.33504554635927, 53.84983360564746),
                        (16.32993358684115, 54.26105171268995), (18.2325742424391, 54.70468244854546),
                        (19.70612689585398, 54.22910226746411), (20.98411476000654, 54.99984738604052),
                        (21.25598976902504, 56.82122554999228), (22.56811669994733, 57.60904955555213),
                        (23.46003290648769, 56.95097188156642), (24.27282452911908, 57.10063319953949),
                        (24.61758211826361, 58.41163311433169), (23.71739164634543, 58.77777200691209),
                        (25.96784639460749, 59.4552122595944), (28.24369757389492, 59.44493637246238),
                        (30.41875338434282, 59.8836941699797), (28.7079510127766, 60.58541472289695),
                        (27.30998657948628, 60.55005859777292), (23.3183846861423, 60.08305445089943),
                        (19.78756137655186, 60.36365070059276), (20.93849509662242, 60.49574613002243),
                        (21.57859894110856, 61.31118106886252), (21.26630417812444, 62.49449727860543),
                        (21.22199127059472, 63.3665684167341), (22.03716059585436, 63.13835989498561),
                        (25.91655947968274, 65.40203551031283), (24.36328167533541, 65.81950634055588),
                        (22.25901217649315, 65.67588493484378)],
    "Азовское море": [(36.84871898624929, 45.41300904048946),
                      (37.3787767506072, 45.30899725349005), (37.62935944421832, 45.41202992779512),
                      (37.67777440740717, 45.64914659905271), (37.86879015239585, 45.73645431922621),
                      (38.35911832762768, 46.25050912049952), (37.82647013151912, 46.59919910705533),
                      (38.34089256115356, 46.71747593719477), (39.35607388123027, 47.03619243760995),
                      (39.18867913953804, 47.34942089941648), (38.5129980234087, 47.16769172260822),
                      (38.15429316011414, 47.10571142195102), (37.57072983577576, 47.1150286861585),
                      (37.36225332916693, 46.93342022359369),
                      (37.21479540301109, 46.96923473719016), (36.84402362575612, 46.76455288160297),
                      (36.6343669208849, 46.79597677886348), (36.2834093346257, 46.66752742573959),
                      (35.88106725990824, 46.65054986896078), (35.3247485682041, 46.37396190731037),
                      (35.19602616477761, 46.51271190115576), (35.08793708357416, 46.30501899900572),
                      (34.77291134667531, 46.18349735325281), (35.01351506791708, 45.67236606758198),
                      (35.51886817824808, 45.2497085766329), (35.85644531298639, 45.40581821300523),
                      (35.99020583946202, 45.35621562900026), (36.10078304045992, 45.42327315941058),
                      (36.5719183725349, 45.40537212356236), (36.84871898624929, 45.41300904048946)],
    "Баренцево море": [(39.18484448383339, 67.9637036598395), (44.59983878163726, 68.48091950189733),
                       (46.12475210570698, 66.46462154823108), (52.33946977955691, 68.48377608114374),
                       (52.09954921836098, 71.74515749590849), (60.62297296428441, 75.81770743323752),
                       (57.41429465099202, 80.71070182490131), (12.29187963232387, 79.81854627478695),
                       (23.83641316769636, 70.16516970600946), (39.18484448383339, 67.9637036598395)],
    "Восточно-Сибирское море": [(152.8239794461215, 70.71601094401601), (159.0219254111614, 70.77089312994239),
                                (160.8358272711353, 69.36344276502876), (170.9082952301434, 68.69052027795097),
                                (177.5483897521278, 69.47639900040755), (179.9269379703362, 71.07874982848313),
                                (185.2401327881728, 77.42333330827113), (150.5337133299597, 79.91240617569701),
                                (149.0929225226662, 75.10368220436933), (148.4971215971512, 72.03243792363207),
                                (152.8239794461215, 70.71601094401601)],
    "Карское море": [(61.88385757969615, 76.11948947243589), (52.39076859652629, 71.56643969843394),
                     (52.76055993290256, 68.52613661110924), (61.22461238674233, 68.75019326873054),
                     (68.98642378013868, 68.07041761285082), (70.38039616147769, 72.73093003846905),
                     (71.92499399777428, 63.64918791493891), (76.30938885666872, 72.13216101390742),
                     (83.21398808668789, 70.08147716399543), (88.80441027094747, 74.77515175746258),
                     (104.4382593450357, 77.04739830225016), (95.24641637948696, 80.94622193602817),
                     (58.19816924928404, 80.78206524506004), (61.88385757969615, 76.11948947243589)],
    "Море Лаптевых": [(96.29310942870754, 81.15177461172426), (107.80678130370758, 76.31545538206831),
                      (112.2013125537076, 76.39841019511276), (104.77448990610421, 72.46151948322732),
                      (118.73809674420338, 72.83080402090098), (129.76286891325293, 70.30528590728028),
                      (143.24857858230254, 70.0979116982196), (137.42579225850088, 75.55998496894006),
                      (137.77696574788072, 77.68887410421746), (96.36259938462125, 81.14525381001086),
                      (96.29310942870754, 81.15177461172426)],
    "Белое море": [(38.3745761836148, 66.1849164051753), (32.50906969457879, 66.9217650501927),
                   (34.77407944021602, 65.81952089125245), (34.48393769039718, 64.72875127158294),
                   (37.36371367447938, 63.67512673100959), (38.25769621243379, 64.02920526958414),
                   (36.65924920353086, 65.03727176569987), (40.08976440014158, 64.53549251160115),
                   (39.93188185016791, 65.58591520294563), (42.46195679443809, 66.33506024074345),
                   (44.0058146959932, 65.99772698098228), (44.36310313767387, 68.36871399614806),
                   (39.66719156176629, 67.90800130847033), (38.3745761836148, 66.1849164051753)],
    "Берингово море": [(161.4101600891809, 59.02374597703314), (162.9940536579636, 56.21368880535689),
                       (176.5399299127475, 51.7778703026908), (188.6303747489179, 52.21843708344092),
                       (204.1021308808721, 57.85120926833478), (199.0512369847101, 65.13023611862461),
                       (181.4052852836695, 66.52106341924369), (177.9558122169882, 64.52334185974577),
                       (178.7031757083008, 62.92866699606634), (170.3310517806818, 60.74478745344614),
                       (168.0021900224798, 61.2479655877653), (161.4101600891809, 59.02374597703314)],
    "Охотское море": [(155.6152243321679, 47.91846712405405), (156.6962756571617, 54.40416401015785),
                      (161.185600284414, 59.35305126628077), (165.6608482802567, 62.82245015450745),
                      (158.6081023030027, 62.45054012444308), (153.3282199904377, 59.89112059588682),
                      (146.6373734651626, 59.5510586210911), (142.7139067362349, 59.49771078452089),
                      (134.5663872801278, 54.36234940841436), (140.6301580735721, 53.26301301469023),
                      (142.1903708212585, 53.4410312814867), (141.9872982798825, 45.03140188546154),
                      (147.1294861836893, 42.59162873190419), (155.6152243321679, 47.91846712405405)],

    "Японское море": [(141.94595924590797, 53.18633171218353), (140.83634010528294, 52.88169244276794),
                      (141.29776588653297, 51.90721019117847), (140.3721677420017, 51.227681291243876),
                      (139.84345070098607, 48.5190022123508), (133.33920112823216, 43.009258647865096),
                      (130.19702545379366, 43.09505264443996), (129.24117199157445, 40.94346156565881),
                      (127.18121401046479, 39.330189720508095), (129.7547506449099, 33.58742145772456),
                      (135.8755033371325, 35.37195510705656), (140.56185624574383, 37.73015908094383),
                      (139.97477165435515, 41.6833488772955), (142.04002968047826, 45.98524750550346),
                      (142.39090553497044, 50.98387633440899), (141.72623268340797, 51.954751674449525),
                      (141.94595924590797, 53.18633171218353)],
    "Карибское море": [(-83.92828290990599, 14.75921492665484), (-83.50059919939586, 9.883242301634979),
                       (-81.57143500677417, 8.747330249649234), (-79.12792125240952, 9.542976978851655),
                       (-76.97657532309087, 7.855157722112979), (-74.70197055336649, 10.92819383002598),
                       (-72.3322159365957, 10.54936293485687), (-69.52174997720881, 11.54653608530186),
                       (-66.35807549245814, 9.564397792396088), (-61.81311011138047, 11.02186259770674),
                       (-60.77364427924863, 14.86952664442117), (-63.15915652808251, 18.07456289233691),
                       (-66.88944851119925, 18.33374199485756), (-83.84502387356456, 22.66601571628908),
                       (-88.77019016345129, 19.94871196644718), (-89.19022165453072, 15.75195883728443),
                       (-83.92828290990599, 14.75921492665484)],
    "Аравийское море": [(48.26991750441138, 30.43612876361517), (48.24882936963527, 27.9545832692156),
                        (51.71703309574644, 24.02096994362395), (57.32150535882855, 23.57348778559302),
                        (59.06753609135957, 21.81331664271385), (53.95027479198691, 16.66580410339008),
                        (50.43783312086756, 11.24502798790454), (46.21182285480418, 2.901146203314876),
                        (40.04799627522097, -2.295029326538503), (39.05183562657917, -12.0236365257905),
                        (46.27127465260395, -16.93312581227438), (67.45278512068548, -4.796303432880149),
                        (77.22748881689668, 8.756637761657126), (73.04709488435699, 21.20169597854037),
                        (67.09733859730609, 25.29990348224553), (54.34626431838399, 27.06659824259317),
                        (48.26991750441138, 30.43612876361517)],
    "Южно-Китайское море": [(105.6723300781247, 21.641361955243937), (105.80416601562469, 17.782288541109388),
                            (108.96822851562472, 14.351700030278302), (105.0461093749997, 9.08785129454797),
                            (102.77743261718719, 4.617990080389445), (106.03762548828091, -0.19476274238048574),
                            (111.35912817382776, 0.9355991625570602), (115.45016210937472, 4.97961875336819),
                            (121.2289707031247, 12.615391909831459), (120.39400976562474, 22.85834486290632),
                            (115.16451757812473, 23.224376333836062), (110.63815039062473, 21.672172737685923),
                            (105.6723300781247, 21.641361955243937)],
    "Восточно-Китайсоке море": [(125.63938219621953, 24.639457102067496), (130.39401531685934, 28.858857198388723),
                                (131.4508376595193, 32.8384480831481), (129.69516000217928, 33.31924933052073),
                                (128.73263281249916, 35.61168341678371), (120.59176367187406, 32.17701757552426),
                                (119.20223728134717, 25.736556483549094), (125.63938219621953, 24.639457102067496)],
    "Тасманово море": [(152.92714187499948, -26.917652730337558), (152.48768874999942, -31.91678792286556),
                       (146.2286289194552, -41.959462818428364), (167.74300658891096, -46.30746249994258),
                       (175.6155119278226, -40.91517638311338), (173.8451106249994, -35.04618267657168),
                       (166.55018874999942, -22.585097710524117), (152.92714187499948, -26.917652730337558)]
}

dates = []


def fetch_records(limit=5000):
    global dates_for_info
    try:
        # TODO optimization of loading records
        resp = requests.get(RECORDS_URL, params=dict(api_key=API_KEY, is_yandex_map=0, limit=limit))
        current_time = datetime.datetime.now()
        s = str(current_time)
        current_time = s.split('.')[0]
        dates_for_info = {'date': current_time}
    except requests.exceptions.ConnectionError:
        mb.showerror('IGWAtlas Статистика Offline', 'Нет подключения к серверу, проверьте интернет соединение')
    else:
        save_records(resp.json())


def load_records():
    with open('records.json', 'r') as f:
        recs = json.load(f)
    return recs


def load_date():
    with open('date.json', 'r') as f:
        date_for = json.load(f)
    return date_for


def save_records(result):
    if os.path.isfile('records.json'):
        os.remove('records.json')
    with open('records.json', 'w+') as f:
        json.dump(result, f)
    with open('date.json', 'w+') as p:
        json.dump(dates_for_info, p)


def is_inside_sea(p_lat, p_lon, coords):
    point = Point(p_lon, p_lat)
    poly = Polygon(coords)
    return point.within(poly)


def increment_type_to_sea(record_types, sea_types):
    """ Count record types for sea """
    for type_obj in record_types:
        sea_types[type_obj['value']] += 1


def get_years_and_months(date_time_obj, sea_types):
    """ Count record by years and month """
    if date_time_obj.year not in sea_types['year']:
        sea_types['year'][date_time_obj.year] = 0
    sea_types['year'][date_time_obj.year] += 1

    if date_time_obj.month not in sea_types['month']:
        sea_types['month'][date_time_obj.month] = 0
    sea_types['month'][date_time_obj.month] += 1


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
    '''fig = plt.figure(constrained_layout=True, figsize=[8, 4])
    spec2 = gridspec.GridSpec(ncols=2, nrows=1, figure=fig)
    img_area_1 = fig.add_subplot(spec2[0, 0])
    img_area_2 = fig.add_subplot(spec2[0, 1])'''
    fig = Figure(figsize=(8.5, 5), dpi=100)
    img_area_1, img_area_2 = fig.subplots(ncols=2, nrows=1)

    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

    return canvas, img_area_1, img_area_2


def plot_season():
    try:
        plot_bars_season(img_area_1, ComboBox1.get())
    except KeyError:
        mb.showerror('IGWAtlas Статистика', 'В {} записей не существует'.format(ComboBox1.get()))
    max = max_value_seas
    try:
        plot_bars_season(img_area_2, ComboBox2.get())
    except KeyError:
        mb.showerror('IGWAtlas Статистика', 'В {} записей не существует'.format(ComboBox2.get()))
    if max_value_seas > max:
        max = max_value_seas
    print(max)
    img_area_1.set_ylim(0, max+1)
    img_area_2.set_ylim(0, max+1)
    canvas.draw()


def plot_bars_season(img_area, cb_sea_name):
    global max_value_seas
    max_value_seas = 0
    winter_count, spring_count, summer_count, autumn_count = 0, 0, 0, 0
    for month, value in sea_stats[cb_sea_name]['month'].items():
        if month in WINTER_MONTHS:
            winter_count += value
        elif month in SPRING_MONTHS:
            spring_count += value
        elif month in SUMMER_MONTHS:
            summer_count += value
        elif month in AUTUMN_MONTHS:
            autumn_count += value
    max_value_seas = max(winter_count, spring_count, summer_count, autumn_count)

    img_area.cla()
    img_area.bar(SEASONS_X, [winter_count, spring_count, summer_count, autumn_count], tick_label=SEASONS)
    img_area.set_xlabel('Сезоны')
    img_area.set_ylabel('Количество наблюдений')
    img_area.set_title(cb_sea_name, fontsize=16)


def plot_month():
    try:
        plot_bars_month(img_area_1, ComboBox1.get())
    except KeyError:
        mb.showerror('IGWAtlas Статистика', 'В {} записей не существует'.format(ComboBox1.get()))
    max = max_value_month
    try:
        plot_bars_month(img_area_2, ComboBox2.get())
    except KeyError:
        mb.showerror('IGWAtlas Статистика', 'В {} записей не существует'.format(ComboBox2.get()))
    if max_value_month > max:
        max = max_value_month
    img_area_1.set_ylim(0, max + 1)
    img_area_2.set_ylim(0, max + 1)
    canvas.draw()


def plot_bars_month(img_area, cb_sea_name):
    global max_value_month
    sea_month_y = [count for record_type, count in sorted(sea_stats[cb_sea_name]['month'].items())]
    max_value_month = max(sea_month_y)
    img_area.cla()
    img_area.bar(MONTHS_X, sea_month_y, tick_label=MONTHS)
    img_area.tick_params(axis="x", labelrotation=50)
    img_area.set_xlabel('Месяца')
    img_area.set_ylabel('Количество наблюдений')
    img_area.set_title(cb_sea_name, fontsize=16)


def plot_bars_year():
    try:
        plot_bars_year1(img_area_1, ComboBox1.get())
    except KeyError:
        mb.showerror('IGWAtlas Статистика', 'В {} записей не существует'.format(ComboBox1.get()))
    max = max_value_year
    try:
        plot_bars_year1(img_area_2, ComboBox2.get())
    except KeyError:
        mb.showerror('IGWAtlas Статистика', 'В {} записей не существует'.format(ComboBox2.get()))
    if max_value_year > max:
        max = max_value_year
    img_area_1.set_ylim(0, max + 1)
    img_area_2.set_ylim(0, max + 1)
    canvas.draw()


def plot_bars_year1(img_area, cb_sea_name):
    global max_value_year
    # generate dict with zero values
    init_range_year = {year: 0 for year in range(sea_stats['min_year'].year, sea_stats['max_year'].year)}

    # join year for sea with init range
    sea_years = {**init_range_year, **sea_stats[cb_sea_name]['year']}

    sea_years_y = [year for year, value in sorted(sea_years.items())]
    sea_years_x = [value for year, value in sorted(sea_years.items())]
    max_value_year = max(sea_years_x)

    img_area.cla()
    img_area.bar(sea_years_y, sea_years_x)
    img_area.set_xlabel('Года')
    img_area.set_ylabel('Количество наблюдений')
    img_area.set_title(cb_sea_name, fontsize=16)


def plot_bars():
    try:
        plot_bars_type(img_area_1, ComboBox1.get())
    except KeyError:
        mb.showerror('IGWAtlas Статистика', 'В {} записей не существует'.format(ComboBox1.get()))
    max = max_value_type
    try:
        plot_bars_type(img_area_2, ComboBox2.get())
    except KeyError:
        mb.showerror('IGWAtlas Статистика', 'В {} записей не существует'.format(ComboBox2.get()))
    if max_value_type > max:
        max = max_value_type
    img_area_1.set_ylim(0, max + 1)
    img_area_2.set_ylim(0, max + 1)
    canvas.draw()


def plot_bars_type(img_area, cb_sea_name):
    global max_value_type
    sea_type_y = [count for record_type, count in sorted(sea_stats[cb_sea_name]['types'].items())]
    max_value_type = max(sea_type_y)

    img_area.cla()
    img_area.bar(RECORD_TYPES_X, sea_type_y, tick_label=RECORD_TYPES)
    img_area.tick_params(labelsize=7)
    img_area.set_xlabel('Типы наблюдений')
    img_area.set_ylabel('Количество наблюдений')
    img_area.set_title(cb_sea_name, fontsize=16)


def get_sea_name(point_get):
    """ Get sea name by coordinates """
    for sea_name, coords in DICT_SEAS.items():
        if is_inside_sea(point_get['lat'], point_get['lon'], coords):
            return sea_name

    return WORLD_OCEAN


def get_stats(points):
    """ Prepare statistics """
    stats = {}
    for point in points:
        sea_name = get_sea_name(point)
        if sea_name not in stats:
            stats[sea_name] = {}
            stats[sea_name]['year'] = {}
            stats[sea_name]['types'] = {i: 0 for i in RECORD_TYPES_X}
            stats[sea_name]['month'] = {i: 0 for i in MONTHS_X}

        increment_type_to_sea(point['new_types'], stats[sea_name]['types'])

        if point['date']:
            date_time_obj = datetime.datetime.strptime(point['date'], '%Y-%m-%dT%H:%M:%SZ')
            get_years_and_months(date_time_obj, stats[sea_name])
            dates.append(date_time_obj)

    stats['min_year'] = min(dates)
    stats['max_year'] = max(dates)

    return stats


def create_info():
    global root
    root = Tk()
    date_for_info = load_date()
    l1 = Label(text='Total records: {}'.format(records['count']), font="Arial 14", master=root, justify=LEFT)
    l2 = Label(text='Дата последнего обновления:\n{}'.format(date_for_info['date']), font="Arial 14", master=root)
    l3 = Label(text='Для отзывов и предложений:\nmanikina704@gmail.com', font="Arial 14", master=root)
    l4 = Label(text='Версия приложения:\n1.2.1', master=root, font="Arial 14")
    l1.pack()
    l2.pack()
    l3.pack()
    l4.pack()
    root.wm_title("IGWAtlas Статистика")
    root.mainloop()
    root.quit()


def create_dataset():
    if os.path.isfile('records.json'):
        os.remove('records.json')
    fetch_records()
    wait_load.destroy()


def create_start_dowload():
    global wait_load
    wait_load = tkinter.Tk()
    text_of_informatio = Label(master=wait_load, text='Нажмите на кнопку\nи ожидайте закрытия окна')
    text_of_informatio.pack()
    button_start = tkinter.Button(master=wait_load, text='Загрузить', command=create_dataset)
    button_start.pack(side=tkinter.BOTTOM)
    wait_load.wm_title("IGWAtlas Статистика")
    wait_load.mainloop()
    wait_load.quit()


def on_closing():
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        window.quit()


if __name__ == '__main__':
    window = Tk()
    window.wm_title("IGWAtlas Статистика")

    canvas, img_area_1, img_area_2 = init_plot_bar()

    button_type = tkinter.Button(master=window, text='По типам наблюдений', command=plot_bars)
    button_type.pack(side=tkinter.LEFT)
    button_year = tkinter.Button(master=window, text='По годам', command=plot_bars_year)
    button_year.pack(side=tkinter.LEFT)
    button_season = tkinter.Button(master=window, text='По сезонам', command=plot_season)
    button_season.pack(side=tkinter.LEFT)
    button_month = tkinter.Button(master=window, text='По месяцам', command=plot_month)
    button_month.pack(side=tkinter.LEFT)

    ComboBox2 = Combobox(master=window, state="readonly")
    ComboBox2['values'] = list(DICT_SEAS.keys()) + [WORLD_OCEAN]
    ComboBox2.current(0)
    ComboBox2.pack(side=tkinter.RIGHT)

    ComboBox1 = Combobox(master=window, state="readonly")
    ComboBox1['values'] = list(DICT_SEAS.keys()) + [WORLD_OCEAN]
    ComboBox1.current(0)
    ComboBox1.pack()

    # load saved records from json
    records = {}
    for i in range(3):
        try:
            records = load_records()
        except FileNotFoundError:
            # fetch records from server and save locally
            fetch_records()

        if records:
            break

    if records:
        print('Total records: {}'.format(records['count']))
        sea_stats = get_stats(records['results'])
        print('IGWAtlas Statistic ready for work')
    else:
        mb.showerror('IGWAtlas Статистика Offline', 'Ошибка при загрузке данных')
    menu = Menu(window)
    submenu = Menu(window)
    window.config(menu=menu)
    submenu.add_command(label="info", command=create_info)
    submenu.add_command(label="Обновить данные", command=create_start_dowload)
    menu.add_cascade(label="about", menu=submenu)

    window.protocol("WM_DELETE_WINDOW", on_closing)
    tkinter.mainloop()
