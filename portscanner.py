import socket

def scan_ports(url, ports_to_scan=None):
    if ports_to_scan is None:
        ports_to_scan = [80, 443, 22, 21, 25, 110, 143, 993, 995]  # Стандартные порты для сканирования

    open_ports = []

    try:
        ip = socket.gethostbyname(url)
        print(f"Сканирование {url} ({ip})...")

        for port in ports_to_scan:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Таймаут в 1 секунду

            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)

            sock.close()

    except socket.gaierror:
        print("Не удалось получить IP-адрес. Проверьте URL.")
        return []

    print(f"Открытые порты: {open_ports}")
    return open_ports

if __name__ == "__main__":
    url = input("Введите URL для сканирования открытых портов: ")
    scan_ports(url)