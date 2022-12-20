import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs

URL_ = "https://cbr.ru/"
respons_ = requests.get(URL_)
path_ = 'data.txt'


def extract_data_from_cbr(aisles=1000, delay=120):
    if respons_.status_code == 200:
        number_of_passes = 0
        print(f"Начало парсинга. Запланировано {aisles} проходов с задержкой в {delay} секунд")
        while aisles:
            try:
                soup = bs(respons_.text, "html.parser")
                vacancies_names = soup.find('main', class_='home-content').find_all(class_='main-indicator_value')
                text_list = ["Цель по инфляции", "Инфляция", "Ключевая ставка", "Ставка RUONIA"]
                counter = 0

                with open(path_, 'a') as file_dt:
                    file_dt.write(f" *************** {datetime.now()} *************** \n")

                for sort_data in vacancies_names:
                    split_data = sort_data.text.split('%')
                    with open(path_, 'a') as file_:
                        file_.write(f"{text_list[counter]} - {split_data[0]}\n")
                    counter += 1

                number_of_passes += 1
                print(f"Проход - {number_of_passes}")
                time.sleep(delay)

            except KeyboardInterrupt:
                print("Выполнение остановлено пользователем!")
                break


if __name__ == '__main__':
    extract_data_from_cbr()
