import requests
import time

API_KEY = 'ae1671ede85d280ad1b4363336fc7f38'
TEXT_TO_CHECK = 'Ваш текст для проверки уникальности. Проверяемый текст слишком короткий. Минимальная длина текста — 100 символов.'


def check_text_uniqueness(api_key, text):
    # URL для отправки текста на проверку
    url_submit = 'http://api.text.ru/post'

    # Параметры для отправки текста
    data_submit = {
        'text': text,
        'userkey': api_key
    }

    # Выполняем запрос на проверку текста
    response = requests.post(url_submit, data=data_submit)

    if response.status_code == 200:
        json_response = response.json()
        if 'text_uid' in json_response:
            text_uid = json_response['text_uid']
            return text_uid
        else:
            print('Error:', json_response)
            return None
    else:
        print('HTTP Error:', response.status_code)
        return None


def get_result(api_key, text_uid):
    # URL для получения результата проверки
    url_result = 'http://api.text.ru/post'

    # Параметры для получения результата
    data_result = {
        'uid': text_uid,
        'userkey': api_key,
        'jsonvisible': 'detail'
    }

    while True:
        # Выполняем запрос на получение результата
        response = requests.post(url_result, data=data_result)

        if response.status_code == 200:
            json_response = response.json()
            if 'text_unique' in json_response:
                return json_response
            elif 'error_code' in json_response:
                print('Error:', json_response['error_desc'])
                # Ожидаем 15 секунд перед повторной проверкой
                time.sleep(15)
        else:
            print('HTTP Error:', response.status_code)
            return None


def main():
    text_uid = check_text_uniqueness(API_KEY, TEXT_TO_CHECK)

    if text_uid:
        print('Text submitted successfully. UID:', text_uid)
        result = get_result(API_KEY, text_uid)

        if result:
            print('Unique:', result.get('text_unique'))
            print('Result details:', result)
        else:
            print('Failed to retrieve the result.')
    else:
        print('Failed to submit the text.')


if __name__ == "__main__":
    main()
