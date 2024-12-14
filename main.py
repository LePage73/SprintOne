import data_download as dd
import data_plotting as dplt
import datetime as dt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    if ticker == '':
        ticker = 'NVDA'
        print("Тикер по умолчанию - NVDA (NVIDIA Corp.)")
    valid_period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    period = input(
        "Введите период для данных (например, '1mo' для одного месяца), если не укажете то предложим задать вручную:»")
    date_start = None
    date_end = None
    if not period in valid_period:
        period = 'manually_period'
        print("Период не распознан, будет задан вручную")
        date_start = input("Введите дату начала в формате ГГГГ-ММ-ДД:»")
        try:
            dt.datetime.strptime(date_start, "%Y-%m-%d")
        except ValueError:
            date_start = dt.date.today() - dt.timedelta(days=30)
            print("Дата не распознана, будет установлена дата 30 дней назад")

        date_end = input("Введите дату конца в формате ГГГГ-ММ-ДД:»")
        try:
            dt.datetime.strptime(date_end, "%Y-%m-%d")
        except ValueError:
            date_end = dt.date.today()
            print("Дата не распознана, будет установлена сегодняшняя дата")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, start_date=date_start, end_date=date_end, period=period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)

    # calculate and display average closed price
    dd.calculate_and_display_average_price(stock_data)

    # notify if strong fluctuations closed price
    dd.notify_if_strong_fluctuations(stock_data, input("Задайте порог изменения цены закрытия в процентах:»"))

    # export data to CSV file
    dd.export_data_to_csv(stock_data,
                          filename=input(
                              'Задайте имя CSV файла, если не укажете будет установлено имя файла Графика:»'))

    # get and plot RSI
    dplt.update_rsi_to_plot(dd.get_rsi(stock_data))

    # get and plot MACD
    dplt.update_macd_to_plot(dd.get_macd(stock_data))


if __name__ == "__main__":
    main()
