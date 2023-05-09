import os
from typing import NamedTuple

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from django.conf import settings

path = os.path.join(settings.BASE_DIR, 'media/graphs/tmp')


class SpareRequestsData(NamedTuple):
    """Структура данных информации для графиков"""
    AD_prices: list
    EX_prices: list
    AD_dates: list
    EX_dates: list


def make_spare_fig(spare: str, data: SpareRequestsData) -> str:
    """Создание графика, возвращает путь к файлу графика"""
    matplotlib.rc('xtick', labelsize=16, labelcolor='#7f1700')
    matplotlib.rc('ytick', labelsize=16, labelcolor='#7f1700')
    fig = plt.figure(figsize=(7, 4), facecolor='#f0f5f2')
    ax = fig.add_subplot()
    ax.plot(data.AD_dates, data.AD_prices, marker='s', markerfacecolor='w')
    ax.plot(data.EX_dates, data.EX_prices)
    ax.grid()
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)

    formatter = mdates.ConciseDateFormatter(locator)
    formatter.formats = ['%y',
                         '%b',
                         '%d',
                         '%H:%M',
                         '%H:%M',
                         '%S.%f', ]
    formatter.zero_formats = [''] + formatter.formats[:-1]
    formatter.zero_formats[3] = '%b %d'
    formatter.offset_formats = [''] * 6
    ax.xaxis.set_major_formatter(formatter)

    graph_path = os.path.join(path, f'{spare}.png')
    fig.savefig(graph_path)
    return graph_path
