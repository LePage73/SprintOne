import matplotlib.pyplot as plt
import pandas as pd
import os
import glob


def create_and_save_plot(data, ticker, period, filename=None):
    """
    Создаёт график, отображающий цены закрытия и скользящие средние.
    Предоставляет возможность сохранения графика в файл.
    Параметр filename опционален; если он не указан, имя файла генерируется автоматически.
    :param data:
    :param ticker:
    :param period:
    :param filename:
    :return:
    """
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")


def update_rsi_to_plot(rsi):
    """
    Дополняет предыдущий график добавляя к нему график RSI и сохраняет в файл
    :param rsi:
    :return:
    """
    # запоминаем старую легенду
    line1, label1 = plt.gca().get_legend_handles_labels()
    plt.legend().set_visible(False)
    # строим график поверх старого в другом масштабе
    ax = plt.twinx()
    ax.plot(rsi['Date'], rsi['RSI'], 'g', label='RSI')
    ax.set_ylabel('RSI', color='g')
    ax.grid()
    # берем новую легенду
    line2, label2 = plt.gca().get_legend_handles_labels()
    # объединяем новую и старую легенды
    line = line1 + line2
    label = label1 + label2
    plt.legend(line, label)
    # находим имя файла
    current_directory = os.getcwd()
    list_files = glob.glob(current_directory + '\\*.png')
    filename = max(list_files, key=os.path.getmtime)
    filename = filename.split('.')[0] + '_with_RSI.png'
    plt.savefig(filename)
    print(f'Дополненый RSI график сохранен в файл: {filename}')


def update_macd_to_plot(df):
    """
    Добавляет к предыдущему холсту график MACD и сохраняет в файл
    :param df:
    :return:
    """
    # получаем текущую фигуру
    fig = plt.gcf()
    # берем список графиков на ней
    ax_list = fig.axes
    # все графики помещаем в верхнюю ячейку
    _ = [ax.set_subplotspec(fig.add_gridspec(2, 1)[0]) for ax in ax_list]
    # выбираем нижнюю ячейку и строим в ней график MACD
    plt.subplot(212)
    plt.plot(df.index, df['MACD'], 'y', label='MACD')
    plt.plot(df.index, df['SignalLine'], 'r', label='SignalLine')
    plt.bar(df.index, df['BC'], color=df['BC_COLOR'], label='BC')
    plt.tight_layout()
    plt.legend()
    # находим имя файла
    current_directory = os.getcwd()
    list_files = glob.glob(current_directory + '\\*.png')
    filename = max(list_files, key=os.path.getmtime)
    filename = filename.split('.')[0] + '_and_MACD.png'
    plt.savefig(filename)
    plt.show()
    print(f'Дополненый MACD график сохранен в файл: {filename}')
