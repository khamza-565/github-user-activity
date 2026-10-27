import sys
import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError




if len(sys.argv) < 2:
    print("Ошибка: не указано имя пользователя!")
elif len(sys.argv) > 2:
    print("Ошибка: передано лишнее значение!")
elif sys.argv[1].strip() == "":
    print("Ошибка: передано пустое значение")
else:
    nickname = sys.argv[1].strip()

    url = f"https://api.github.com/users/{nickname}/events"

    try:

        with urlopen(url) as response:
            text = response.read().decode("utf-8")
        data = json.loads(text)

        if not data:
            print("У пользователя нет недавних публичных событий.")
        else:
            for event in data:
                name = event['repo']['name']

                if event['type'] == 'CreateEvent':
                    if event['payload'].get('ref_type') and event['payload'].get('ref'):
                        ref_type = event['payload'].get('ref_type')
                        ref = event['payload'].get('ref')
                        print(f"Created {ref_type}: {ref} in {name}")

                elif event['type'] == 'PushEvent':
                    print(f"Pushed commits to: {name}")
                elif event['type'] == 'WatchEvent':
                    print(f"Starred a repository: {name}")
                else:
                    print(event['type'], event['repo']['name'])

    except json.decoder.JSONDecodeError:
        print('Ошибка: не удалось разобрать ответ сервера.')
    except HTTPError as error:
        print(f"Ошибка сервера: {error.code}")
    except URLError as error:
        print(f"Ошибка подключения: {error.reason}")





