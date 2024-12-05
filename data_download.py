import yfinance as yf

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
    min = data.Close.min()
    max = data.Close.max()
    fluct = (max - min) / min * 100
    if fluct > float(threshold):
        print(f"Цена закрытия менялась на {max - min:.2f}$ или {fluct:.2f}%")
    return
