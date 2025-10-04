import os


class TextAnalyzer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.filename = None
            self.lines_count = None
            self.chars_count = None
            self.empty_lines_count = None
            self.frequency_dict = None
            self.initialized = True

    def set_file(self, filename):
        self.filename = filename
        self._reset_results()

    def _reset_results(self):
        self.lines_count = None
        self.chars_count = None
        self.empty_lines_count = None
        self.frequency_dict = None

    def count_lines(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return sum(1 for _ in f)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return 0

    def count_characters(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return sum(len(line) for line in f)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return 0

    def count_empty_lines(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return sum(1 for line in f if line.strip() == "")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return 0

    def create_frequency_dict(self):
        freq_dict = {}
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    for char in line:
                        freq_dict[char] = freq_dict.get(char, 0) + 1
            return freq_dict
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return {}

    def analyze(self, options=["1", "2", "3", "4"]):
        for option in options:
            if option == "1":
                self.lines_count = self.count_lines()
            elif option == "2":
                self.chars_count = self.count_characters()
            elif option == "3":
                self.empty_lines_count = self.count_empty_lines()
            elif option == "4":
                self.frequency_dict = self.create_frequency_dict()

    def display_results(self, options=["1", "2", "3", "4"]):
        for option in options:
            if option == "1" and self.lines_count is not None:
                print(f"Количество строк: {self.lines_count}")
            elif option == "2" and self.chars_count is not None:
                print(f"Количество символов: {self.chars_count}")
            elif option == "3" and self.empty_lines_count is not None:
                print(f"Количество пустых строк: {self.empty_lines_count}")
            elif option == "4" and self.frequency_dict is not None:
                print("Частотный словарь символов:")
                for char, count in sorted(
                    self.frequency_dict.items(), key=lambda x: x[1], reverse=True
                ):
                    if char == "\n":
                        print(f"  '\\n': {count}")
                    elif char == " ":
                        print(f"  ' ': {count}")
                    elif char == "\t":
                        print(f"  '\\t': {count}")
                    else:
                        print(f"  '{char}': {count}")
        print()


class ConsoleMenu:
    def __init__(self):
        self.options = {
            "1": "Количество строк",
            "2": "Количество символов",
            "3": "Количество пустых строк",
            "4": "Частотный словарь символов",
            "5": "Все параметры",
            "0": "Выход",
        }

    def display(self):
        print("\n" + "=" * 50)
        print("АНАЛИЗАТОР ТЕКСТОВЫХ ФАЙЛОВ")
        print("=" * 50)
        print("\nВыберите параметры для анализа:")
        for key, value in self.options.items():
            print(f"  {key}. {value}")
        print()

    def get_user_choice(self):
        while True:
            choice = input(
                "Введите номер опции (или несколько через запятую): "
            ).strip()

            if choice == "0":
                return ["0"]

            if choice == "5":
                return ["1", "2", "3", "4"]

            choices = [c.strip() for c in choice.split(",")]

            if all(c in self.options and c not in ["0", "5"] for c in choices):
                return choices
            else:
                print("Ошибка: неверный ввод. Попробуйте снова.")


class FileValidator:
    @staticmethod
    def validate_file(filename):
        if not os.path.exists(filename):
            print(f"Ошибка: файл '{filename}' не найден.")
            return False

        if not os.path.isfile(filename):
            print(f"Ошибка: '{filename}' не является файлом.")
            return False

        try:
            with open(filename, "r", encoding="utf-8") as f:
                pass
            return True
        except Exception as e:
            print(f"Ошибка при открытии файла: {e}")
            return False

    @staticmethod
    def get_filename_from_user():
        while True:
            filename = input(
                "\nВведите имя файла для анализа (или 'exit' для выхода): "
            ).strip()

            if filename.lower() == "exit":
                return None

            if FileValidator.validate_file(filename):
                return filename


def run_tests():
    test_filename = "files/test_file.txt"
    test_content = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
    
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    try:
        with open(test_filename, "w", encoding="utf-8") as f:
            f.write(test_content)
        print(f"Создан тестовый файл: {test_filename}")
    except Exception as e:
        print(f"Ошибка создания тестового файла: {e}")
        return

    analyzer = TextAnalyzer()
    analyzer.set_file(test_filename)

    lines = analyzer.count_lines()
    print(f"Результат: {lines} строк")
    assert lines == 5, f"Ожидалось 5 строк, получено {lines}"
    print("Тест пройден")

    chars = analyzer.count_characters()
    print(f"Результат: {chars} символов")
    assert chars > 0, "Количество символов должно быть больше 0"
    print("Тест пройден")

    empty = analyzer.count_empty_lines()
    print(f"Результат: {empty} пустых строк")
    assert empty == 1, f"Ожидалось 1 пустая строка, получено {empty}"
    print("Тест пройден")

    freq = analyzer.create_frequency_dict()
    print(f"Результат: {len(freq)} уникальных символов")
    assert len(freq) > 0, "Частотный словарь не должен быть пустым"
    print("Тест пройден")

    analyzer.analyze()
    analyzer.display_results()
    print("Тест пройден")

    try:
        os.remove(test_filename)
        print(f"\nТестовый файл {test_filename} удален")
    except:
        pass


if __name__ == "__main__":
    run_tests()
