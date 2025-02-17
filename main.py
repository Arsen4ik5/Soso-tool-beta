import subprocess

def main_menu():
    valid_passwords = {"Mrcod", "1005", "100513", "10051310"}

    password = input("Введите пароль для доступа: ")

    if password not in valid_passwords:
        print("ДЫШИ МНЕ В ХУЙ ПИДОР КОТОРОМУ СЛИЛИ ТУЛ БЕЗ ПАРОЛЯ АХХААХАХАХ")
        return

    while True:
        print(r'''/$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$        /$$$$$$$$ /$$$$$$   /$$$$$$  /$$      
 /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$      |__  $$__//$$__  $$ /$$__  $$| $$      
| $$  \__/| $$  \ $$| $$  \__/| $$  \ $$         | $$  | $$  \ $$| $$  \ $$| $$      
|  $$$$$$ | $$  | $$|  $$$$$$ | $$  | $$         | $$  | $$  | $$| $$  | $$| $$      
 \____  $$| $$  | $$ \____  $$| $$  | $$         | $$  | $$  | $$| $$  | $$| $$      
 /$$  \ $$| $$  | $$ /$$  \ $$| $$  | $$         | $$  | $$  | $$| $$  | $$| $$      
|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$/         | $$  |  $$$$$$/|  $$$$$$/| $$$$$$$$
 \______/  \______/  \______/  \______/          |__/   \______/  \______/ |________/
''')
        print("\nВыберите номер, чтобы открыть нужный файл:")
        print("0 - Выход")
        print("1 - ddos")
        print("2 - Port scanner")
        print("3 - Arsusbot - юзербот")
        print("4 - Пробив по IP")

        choice = input("Введите номер: ")

        if choice == "0":
            print("Выход из программы.")
            break
        elif choice == "1":
            run_script("ddos.py")
        elif choice == "2":
            run_script("portscanner.py")
        elif choice == "3":
            run_script("usbot2.py")
        elif choice == "4":
            run_script("ip.py")
        else:
            print("Неверный ввод, попробуйте снова.")

def run_script(filename):
    try:
        subprocess.run(['python', filename], check=True)
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении файла {filename}: {e}")

if __name__ == "__main__":
    main_menu()