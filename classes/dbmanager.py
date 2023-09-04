import colorama
import psycopg2


class DBManager:

    def __init__(self, params):
        self.connection = psycopg2.connect(**params)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        self.cursor.execute("SELECT company, COUNT(vacancy_name) FROM vacancies "
                            "JOIN companies USING (company_id) "
                            "GROUP BY company")
        result = self.cursor.fetchall()
        for item in result:
            print(colorama.Fore.BLUE + "Компания: " + colorama.Fore.RESET + f"{item[0]}, \t\t" + colorama.Fore.CYAN +
                  "Вакансий: " + colorama.Fore.RESET + f"{item[1]}")

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        self.cursor.execute("SELECT company, vacancy_name, salary_from, salary_to, url FROM vacancies "
                            "JOIN companies USING(company_id)")
        result = self.cursor.fetchall()
        for item in result:
            print(colorama.Fore.BLUE + "Компания: " + colorama.Fore.RESET + f"{item[0]}, " + colorama.Fore.CYAN +
                  "Вакансий: " + colorama.Fore.RESET + f"{item[1]}" +
                  f"{self.format_salary(item)}, "
                  f"Ссылка на вакансию: {item[4]}")

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        self.cursor.execute("SELECT AVG(salary_from) as средняя_зарплата_от, "
                            "AVG(salary_to) as средняя_зарплата_до FROM vacancies")
        result = self.cursor.fetchall()
        for item in result:
            print("Средняя зарплата от: " + colorama.Fore.LIGHTGREEN_EX + f"{int(item[0])} руб., " + colorama.Fore.RESET +
                  "Средняя зарплата до: " + colorama.Fore.GREEN + f"{int(item[1])} руб." + colorama.Fore.RESET)

    def get_vacancies_with_highest_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        self.cursor.execute("SELECT * FROM vacancies "
                            "WHERE salary_from > (SELECT AVG(salary_from+salary_to) FROM vacancies) "
                            "OR salary_to > (SELECT AVG(salary_from+salary_to) FROM vacancies)")
        result = self.cursor.fetchall()
        for item in result:
            print("ID_компании: " + colorama.Fore.YELLOW + f"{item[0]}" + colorama.Fore.RESET +
                  ", Вакансия: " + colorama.Fore.GREEN + f"{item[1]}" + colorama.Fore.RESET + ", " +
                  f"{self.format_salary(item)}, " + colorama.Fore.LIGHTMAGENTA_EX +
                  f"Ссылка на вакансию: {item[4]}" + colorama.Fore.RESET)

    def get_vacancies_with_keyword(self, query):
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например “python”.
        """
        for word in query.split():
            self.cursor.execute(f"SELECT * FROM vacancies "
                                f"WHERE vacancy_name LIKE '%{word.capitalize()}%'")
            result = self.cursor.fetchall()
            if result:
                print(f'Результаты по ключевому слову "{word}":')
            for item in result:
                print(f"ID_компании: {item[0]}, " + colorama.Fore.GREEN + "Вакансия: {item[1]}, "+colorama.Fore.RESET +
                      f"{self.format_salary(item)}, "
                      f"Ссылка на вакансию: {item[4]}")

    @staticmethod
    def format_salary(item):
        if item[2] is None:
            return f"Зарплата до {item[3]} руб."
        if item[3] is None:
            return f"Зарплата от {item[2]} руб."
        return f"Зарплата от {item[2]} до {item[3]} руб."

    def close(self):
        self.cursor.close()
        self.connection.close()