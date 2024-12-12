# -*- coding: utf-8 -*-
import requests
import webbrowser

class WikipediaSearch:
    def __init__(self):
        self.results = []  # Список для хранения результатов поиска

    # Выполняет запрос к API википедии и получает результаты поиска
    def fetch_results(self, query):
        url = "https://ru.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "format": "json",
            "utf8": "",
            "srsearch": query,
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if "query" in data and "search" in data["query"]:
                self.results = data["query"]["search"]
                return True
        return False

    # Отображает результаты поиска с номерами для выбора
    def display_results(self, query):
        if not self.results:
            print(f"По запросу '{query}' ничего не найдено.")
            return

        print(f"Результаты поиска по запросу '{query}':\n")
        for idx, result in enumerate(self.results, start=1):
            print(f"{idx}. {result['title']}")

    # Открывает статью по индексу в браузере
    def open_article(self, index):
        page_id = self.results[index - 1]["pageid"]
        result_url = f"https://ru.wikipedia.org/?curid={page_id}"
        webbrowser.open(result_url)

def main():
    search_engine = WikipediaSearch()

    while True:
        # Запросить строку поиска у пользователя
        query = input("Введите строку для поиска по Википедии (или '-1' для завершения): ").strip()

        if query.lower() == '-1':
            print("Выход из программы...")
            break

        # Выполнение поиска
        if search_engine.fetch_results(query):
            search_engine.display_results(query)

            # Запросить у пользователя номер статьи для открытия
            try:
                article_number = int(input("Введите номер статьи для открытия (или 0 для нового поиска): ").strip())
                if article_number == 0:
                    continue
                elif 1 <= article_number <= len(search_engine.results):
                    search_engine.open_article(article_number)
                else:
                    print("Некорректный номер статьи.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")
        else:
            print("Произошла ошибка при выполнении запроса. Попробуйте снова...")

if __name__ == "__main__":
    main()

