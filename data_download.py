import pandas as pd
import yfinance as yf
import glob
import os
import pandas


def fetch_stock_data(ticker, period='1mo'):
    """
    Получает исторические данные об акциях для указанного тикера и временного периода.
    :param ticker:
    :param period:
    :return DataFrame:
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    """
    Добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия.

    :param data:
    :param window_size:
    :return DataFrame:
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """"
    вычисляет среднюю цену закрытия акций за заданный период и выводит её в консоль
    """
    data_average = data['Close'].mean()
    print(f'Средняя цена закрытия: {data_average:.2f}$')
    return


def notify_if_strong_fluctuations(data, threshold):
    """
    анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период
    :param data:
    :param threshold:
    :return:
    """
    if threshold == None or threshold == '':
        threshold = 0
    min = data.Close.min()
    max = data.Close.max()
    fluct = (max - min) / min * 100
    if fluct > float(threshold):
        print(f"Цена закрытия менялась на {max - min:.2f}$ или {fluct:.2f}%")
    return


def export_data_to_csv(data, filename=None):
    """
    позволяет сохранять загруженные данные об акциях в CSV файл.
    :param data:
    :param filename:
    :return:
    """
    # если имя файла не указано берем имя файла сохраненного предыдущей функцией - create_and_save_plot()
    if filename == None or filename == '':
        current_directory = os.getcwd()
        list_files = glob.glob(current_directory + '\\*.png')
        filename = max(list_files, key=os.path.getmtime)
    filename = filename.split('.')[0] + '.csv'
    data.to_csv(filename, sep=';', encoding='utf-8', index=True)
    print(f'Загруженные данные сохранены в файл: {filename}')
    return


def get_rsi(df, periods=14, ema=True):
    """
       Возвращает DataFrame c датой (индексом) и значением RSI.
    """
    close_delta = df['Close'].diff()

    # Сделаем два ряда: для верхних и нижних закрытий
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema == True:
        # используем экспонентую среднюю скользящую
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    else:
        # используем простую среднюю скользящую
        ma_up = up.rolling(window=periods, adjust=False).mean()
        ma_down = down.rolling(window=periods, adjust=False).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))

    return pd.DataFrame({'Date': rsi.index, 'RSI': rsi.values})


def get_macd(df):
    """
    Возвращает DataFrame с основной и сигнальной линией MACD и разницу между ними
    :param df:
    :return:
    """
    exp1 = df.Close.ewm(span=12, adjust=False).mean()
    exp2 = df.Close.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()
    bc = macd - exp3
    df['MACD'] = macd
    df['SignalLine'] = exp3
    df['BC'] = bc
    df['BC_COLOR'] = bc.map(lambda x: 'red' if x < 0 else 'green')
    return df
