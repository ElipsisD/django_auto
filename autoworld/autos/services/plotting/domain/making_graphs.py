import locale
import os
from datetime import datetime
from typing import NamedTuple

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from django.conf import settings

path = os.path.join(settings.BASE_DIR, 'media/graphs/tmp')


class SpareRequestsData(NamedTuple):
    """Структура данных информации для графиков"""
    prices: list
    dates: list


def make_spare_fig(spare: str, data: SpareRequestsData) -> str:
    """Создание графика, возвращает путь к файлу графика"""
    # matplotlib.RcParams['axes.formatter.use_locale'] = False
    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot()
    ax.plot(data.dates, data.prices, marker='s', markerfacecolor='w')
    ax.grid()
    # locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    # print(locale.getlocale())
    # print(datetime(2023, 4, 2).strftime('%Y-%B-%d'))  # .strftime('%c'))
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    formatter.formats = ['%y',
                         '%b',
                         '%d',
                         '%H:%M',
                         '%H:%M',
                         '%S.%f', ]
    formatter.zero_formats = [''] + formatter.formats[:-1]
    formatter.zero_formats[3] = '%b %d'
    formatter.offset_formats = ['',
                                '%Y',
                                '%B %Y',
                                '%d %B %Y',
                                '%d %B %Y',
                                '%d %B %Y %H:%M', ]
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.ylabel('руб')
    plt.title(f'Динамика изменения цены')
    graph_path = os.path.join(path, f'{spare}.png')
    fig.savefig(graph_path)
    return graph_path
