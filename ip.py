import os
import requests

def get_ip_info(ip_address):
    try:
        response = requests.get(f"http://ipinfo.io/{ip_address}/json")
        response.raise_for_status()  # Проверка на успешность запроса
        data = response.json()
        
        location = data.get("loc")
        google_maps_url = f"https://www.google.com/maps?q={location}" if location else "Координаты отсутствуют"

        return {
            "IP": data.get("ip"),
            "Hostname": data.get("hostname"),
            "City": data.get("city"),
            "Region": data.get("region"),
            "Country": data.get("country"),
            "Location": location,
            "Google Maps": google_maps_url,
            "Organization": data.get("org"),
            "Postal": data.get("postal"),
            "Timezone": data.get("timezone")
        }
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении информации: {e}")
        return None

def display_ip_info(info):
    if info is None:
        print("Информация недоступна.")
    else:
        for key, value in info.items():
            print(f"{key}: {value}")

def clear_console():
    # Очистка консоли в зависимости от операционной системы
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    ip_to_check = input("Введите IP-адрес для пробива: ")
    ip_info = get_ip_info(ip_to_check)
    display_ip_info(ip_info)
    
    input("\nНажмите Enter, чтобы вернуться в меню")
    clear_console()