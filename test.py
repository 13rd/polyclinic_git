import requests


def main():
    data = {
        "role_name": "pacient"
    }

    # URL вашего API
    url = 'http://localhost:5000/create_doctor'

    # Отправка запроса
    response = requests.post(url, json=data)

    # Проверка статуса ответа и вывод результата
    if response.status_code == 201:
        print("Роль создана успешно.")
    else:
        print(f"{response.text}")


if __name__ == '__main__':
    main()
