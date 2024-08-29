import requests

from server.server import run


if __name__ == '__main__':
    # Используем сервис ipify для получения публичного IP
    public_ip = requests.get('https://api.ipify.org').text

    run('', 8000, public_ip)
