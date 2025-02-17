from telethon import TelegramClient, events
import asyncio
import requests
import os
import random
import re

api_id = '22033302'
api_hash = '522596c0b5c29485d238e531ed87ec83'

# Используем None вместо имени файла для временной сессии
client = TelegramClient(None, api_id, api_hash)

allowed_user_id = None
stop_spam_event = asyncio.Event()
stop_rassil_event = asyncio.Event()

os.makedirs('session1', exist_ok=True)

jokes = [
    "Почему программисты не любят природу? Потому что там слишком много багов.",
    "Какой язык программирования самый оптимистичный? Java, потому что у него всегда есть 'try'.",
    "Почему Python не может взобраться на гору? Потому что у него нет 'climb' метода.",
    """— Мама, что такое черный юмор?
— Сынок, видишь вон там мужчину без рук? Вели ему похлопать в ладоши.
— Мама! Я же слепой!
— Вот именно."""
]

async def delete_user_message(event):
    try:
        await event.delete()
    except Exception as e:
        await event.respond(f"Ошибка при удалении сообщения: {e}")

async def is_user_allowed(event):
    return event.sender_id == allowed_user_id

async def spam_messages(event, message, duration):
    end_time = asyncio.get_event_loop().time() + duration
    while asyncio.get_event_loop().time() < end_time:
        if stop_spam_event.is_set():
            break
        try:
            await event.respond(message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
        await asyncio.sleep(0.01)

@client.on(events.NewMessage(pattern=r'\.spam (.+) (\d+)'))
async def spam(event):
    if not await is_user_allowed(event):
        await delete_user_message(event)
        return

    message = event.pattern_match.group(1)
    duration = int(event.pattern_match.group(2)) * 60
    stop_spam_event.clear()
    await spam_messages(event, message, duration)
    await delete_user_message(event)

@client.on(events.NewMessage(pattern=r'\.stop'))
async def stop(event):
    if not await is_user_allowed(event):
        await delete_user_message(event)
        return
        
    stop_spam_event.set()
    stop_rassil_event.set()
    await delete_user_message(event)

@client.on(events.NewMessage(pattern=r'\.rassil (.+) (\S+) (\S+)'))
async def rassil(event):
    if not await is_user_allowed(event):
        await delete_user_message(event)
        return

    message = event.pattern_match.group(1)
    delay_input = event.pattern_match.group(2)  # Задержка между сообщениями
    duration_input = event.pattern_match.group(3)  # Общее время

    # Функция для преобразования времени
    def parse_duration(duration_str):
        time_units = {
            's': 1,    # секунды
            'm': 60,   # минуты
            'h': 3600, # часы
            'd': 86400, # дни
            'w': 604800, # недели
            'y': 31536000 # годы
        }

        if duration_str[-1] in time_units:  # если последний символ указывает на единицу времени
            unit = duration_str[-1]
            value = int(duration_str[:-1])
            return value * time_units[unit]
        else:  # если число без буквы, рассматриваем как секунды
            return int(duration_str)

    try:
        delay = parse_duration(delay_input)  # преобразуем задержку
        duration = parse_duration(duration_input)  # преобразуем общее время
    except ValueError:
        await event.respond("Неверный формат времени. Пожалуйста, используйте числа с единицами времени (s, m, h, d, w, y) или просто числа для секунд.")
        return

    await delete_user_message(event)  # Удаляем сообщение с командой сразу
    end_time = asyncio.get_event_loop().time() + duration
    stop_rassil_event.clear()

    while asyncio.get_event_loop().time() < end_time:
        if stop_rassil_event.is_set():
            break
        try:
            await event.respond(message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
        await asyncio.sleep(delay)  # задержка между сообщениями

@client.on(events.NewMessage(pattern=r'\.ip (.+)'))
async def ip_info(event):
    ip = event.pattern_match.group(1)
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        if data['status'] == 'fail':
            await event.respond("Информация по IP не найдена.")
        else:
            location_link = f"https://www.google.com/maps/search/?api=1&query={data['lat']},{data['lon']}"
            info = (f"Информация по IP {ip}:\n"
                    f"Страна: {data['country']}\n"
                    f"Регион: {data['regionName']}\n"
                    f"Город: {data['city']}\n"
                    f"Широта: {data['lat']}\n"
                    f"Долгота: {data['lon']}\n"
                    f"ISP: {data['isp']}\n"
                    f"Почтовый индекс: {data['zip']}\n"
                    f"Часовой пояс: {data['timezone']}\n"
                    f"Статус: {data['status']}\n"
                    f"Региональный код: {data['region']}\n"
                    f"Примерное местоположение: [Ссылка на Google Maps]({location_link})\n")
            await event.respond(info)
        await delete_user_message(event)
    except Exception as e:
        await event.respond(f"Ошибка при получении информации: {e}")
        await delete_user_message(event)

@client.on(events.NewMessage(pattern=r'\.init'))
async def init(event):
    if not await is_user_allowed(event):
        await delete_user_message(event)
        return

    participants = await client.get_participants(event.chat_id)
    phone_numbers = []

    for user in participants:
        if user.phone:
            name = user.first_name if user.first_name else "Без имени"
            phone_numbers.append(f"{name} | {user.phone}")

    if phone_numbers:
        with open('phone_numbers.txt', 'w') as f:
            for entry in phone_numbers:
                f.write(f"{entry}\n")

        await client.send_file('me', 'phone_numbers.txt')
    else:
        await event.respond("Нет открытых номеров в группе.")
    await delete_user_message(event)

@client.on(events.NewMessage(pattern=r'\.start'))
async def start(event):
    if not await is_user_allowed(event):
        await delete_user_message(event)
        return

    await event.respond("Привет! Я юзербот. Как я могу помочь? Напишите .help для того чтобы увидеть доступные команды")
    await delete_user_message(event)

@client.on(events.NewMessage(pattern=r'\.help'))
async def help(event):
    if not await is_user_allowed(event):
        await delete_user_message(event)
        return

    help_text = ("Доступные команды:\n"
                 ".start - Приветственное сообщение\n"
                 ".help - Список команд\n"
                 ".spam <сообщение> <время> - Запустить спам\n"
                 ".stop - Остановить спам и рассылку\n"
                 ".ip <IP-адрес> - Получить информацию по IP\n"
                 ".init - Получить все открытые номера в группе и отправить файл в избранное\n"
                 ".addsession - Добавить файл сессии\n"
                 ".joke - Получить случайную шутку\n"
                 ".number <номер> - Получить информацию по номеру\n"
                 ".snos <ссылка на сообщение> <комментарий> <количество> - Отправить жалобы на сообщение\n"
                 ".rassil <сообщение> <задержка> <время> - Рассылка сообщений с задержкой")
    await event.respond(help_text)
    await delete_user_message(event)

@client.on(events.NewMessage(pattern=r'\.addsession'))
async def add_session(event):
    if event.sender_id not in [7451036519, 6321157988]:
        await delete_user_message(event)
        return

    await event.respond("Пожалуйста, отправьте файл сессии (с расширением .session).")

    @client.on(events.NewMessage(from_users=event.sender_id))
    async def handle_session_file(msg):
        if msg.file and msg.file.name.endswith('.session'):
            file_path = f'session1/{msg.file.name}'
            await msg.download_media(file=file_path)
            await event.respond(f"Файл сессии '{msg.file.name}' успешно добавлен!")
            await client.remove_event_handler(handle_session_file)
        else:
            await msg.respond("Пожалуйста, отправьте файл с расширением .session.")

    await delete_user_message(event)

@client.on(events.NewMessage(pattern=r'\.number (.+)'))
async def number_info(event):
    number = event.pattern_match.group(1)

    if re.match(r'^\+?\d{10,15}$', number):
        info = f"Номер: {number}\n"
        info += "------------------------------\n"

        try:
            response = requests.get(f'https://htmlweb.ru/geo/api.php?phone={number}')
            response.raise_for_status()

            data = response.json()

            if data:
                country = data.get('country', 'Неизвестно')
                region = data.get('region', 'Неизвестно')
                city = data.get('city', 'Неизвестно')
                provider = data.get('provider', 'Неизвестно')

                info += f"Страна: {country}\n"
                info += f"Регион: {region}\n"
                info += f"Город: {city}\n"
                info += f"Провайдер: {provider}\n"
            else:
                info += "Информация не найдена.\n"

        except requests.exceptions.HTTPError:
            info += "Ошибка: Информация не найдена \n"
        except Exception as e:
            info += f"Ошибка при получении информации: {e}\n"

        info += "------------------------------\n"
        
        await event.respond(info)
        await delete_user_message(event)
    else:
        await event.respond("Неверный формат номера. Пожалуйста, проверьте и попробуйте снова.")
        await delete_user_message(event)

@client.on(events.NewMessage(pattern=r'\.snos (.+) (.+) (\d+)'))
async def snos(event):
    if not await is_user_allowed(event):
        await delete_user_message(event)
        return

    comment = event.pattern_match.group(1)
    count = int(event.pattern_match.group(2))

    session_dir = 'session1'
    session_files = [f for f in os.listdir(session_dir) if f.endswith('.session')]

    if not session_files:
        await event.respond("Нет доступных сессий для отправки жалоб.")
        await delete_user_message(event)
        return

    successful_reports = 0
    failed_reports = 0

    for session_file in session_files:
        session_file_path = os.path.join(session_dir, session_file)

        async with TelegramClient(session_file_path, api_id, api_hash) as active_session:
            for _ in range(count):
                try:
                    await active_session.send_message('me', f'Жалоба на сообщение: {session_file}\nКомментарий: {comment}')
                    successful_reports += 1
                except Exception as e:
                    failed_reports += 1
                    print(f"Ошибка при отправке сессии {session_file}: {e}")

    await event.respond(f"Отправлено {successful_reports} успешных жалоб(ы) и {failed_reports} неуспешных.")
    await delete_user_message(event)

async def check_active_sessions():
    session_dir = 'session1'
    if os.path.exists(session_dir):
        sessions = os.listdir(session_dir)
        if sessions:
            print("Активные сессии:", sessions)
        else:
            print("Нет активных сессий.")
    else:
        print("Директория сессий не найдена.")

async def main():
    retries = 5
    for attempt in range(retries):
        try:
            await client.start()
            break
        except Exception as e:
            if "database is locked" in str(e):
                print(f"Попытка {attempt + 1} из {retries}: база данных заблокирована, повторная попытка...")
                await asyncio.sleep(1)
            else:
                print(f"Неожиданная ошибка: {e}")
                break

    global allowed_user_id
    me = await client.get_me()
    allowed_user_id = me.id
    await check_active_sessions()
    await client.run_until_disconnected()

client.loop.run_until_complete(main())