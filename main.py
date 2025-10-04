from analyzer import TextAnalyzer, ConsoleMenu, FileValidator


def main():
    analyzer = TextAnalyzer()
    menu = ConsoleMenu()

    while True:
        filename = FileValidator.get_filename_from_user()

        if filename is None:
            print("Выход из программы.")
            break

        analyzer.set_file(filename)

        menu.display()
        choices = menu.get_user_choice()

        if "0" in choices:
            print("Выход из программы.")
            break

        analyzer.analyze(choices)
        analyzer.display_results(choices)

        continue_work = input("\nПродолжить работу? (да/нет): ").strip().lower()
        if continue_work not in ["да", "y"]:
            print("Выход из программы. До свидания!")
            break


if __name__ == "__main__":
    main()
