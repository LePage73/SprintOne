## Спринт №1

- fetch_stock_data(ticker, period): Получает исторические данные об акциях для указанного тикера и временного периода.
  Возвращает DataFrame с данными.

- add_moving_average(data, window_size):
  Добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия.

- create_and_save_plot(data, ticker, period, filename):
  Создаёт график, отображающий цены закрытия и скользящие средние.
  Предоставляет возможность сохранения графика в файл.
  Параметр filename опционален; если он не указан, имя файла генерируется автоматически.
  
- calculate_and_display_average_price(data)
  Вычисляет и выводит среднюю цену закрытия акций за заданный период.

- notify_if_strong_fluctuations(data, threshold)
  Анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.

- export_data_to_csv(data, filename) позволяет сохранять загруженные данные об акциях в CSV файл