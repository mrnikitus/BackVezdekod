import shutil
from datetime import datetime
import json
import requests

try:
    import config
except ImportError:
    shutil.copy(r'config.example.py', r'config.py')
    import srv

token = config.token
set_header = 'Token ' + token

s = requests.Session()
s.headers.update({'Authorization': set_header})

def show_all():
    req = s.get(f'{config.host}/api/memes')
    if req.status_code != 200:
        print('\nПри запросе возникла проблема!\nКод ошибки: ', req.status_code, ', сообщение: "',json.loads(req.content)['detail'],'"',sep='')
    else:
        resp = json.loads(req.content)
        print('\nСписок мемов в порядке их добавления в систему (от новых до старых):\n')
        for i in range(len(resp)):
            print(f'{i+1}) ID: {resp[i]["id"]}\nКартинка: {resp[i]["photo"]}\nАвтор: {resp[i]["author"]}\nДата добавления: {datetime.strptime(resp[i]["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")}\nКоличество лайков: {resp[i]["likes"]}\n')

def meme_feed():
    while(True):
        req = s.get(f'{config.host}/api/feed')
        if req.status_code != 200:
            if req.status_code == 204:
                print('\nМемов пока еще нет в базе(')
                return
            print('\nПри запросе возникла проблема!\nКод ошибки: ', req.status_code, ', сообщение: "',
                  json.loads(req.content)['detail'], '"', sep='')
            break
        else:
            resp = json.loads(req.content)
            print(f'\nID: {resp["id"]}\nКартинка: {resp["photo"]}\nАвтор: {resp["author"]}\nДата добавления: {datetime.strptime(resp["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")}\nКоличество лайков: {resp["likes"]}\n')
            print(' [1] Лайк, [2] Пропустить, [0] Выйти из меню')
            choice = int(input(' Ваш выбор: '))
            if choice == 1:
                req = s.post(f'{config.host}/api/like/{resp["id"]}')
                if req.status_code != 200:
                    print('\nПри запросе возникла проблема!\nКод ошибки: ', req.status_code, ', сообщение: "',
                          json.loads(req.content)['detail'], '"', sep='')
                    break
                else:
                    print(json.loads(req.content)['detail'])
            elif choice == 2:
                req = s.delete(f'{config.host}/api/like/{resp["id"]}')
                if req.status_code != 200:
                    print('\nПри запросе возникла проблема!\nКод ошибки: ', req.status_code, ', сообщение: "',
                          json.loads(req.content)['detail'], '"', sep='')
                    break
                else:
                    print(json.loads(req.content)['detail'])
            elif choice == 0:
                break
            else:
                print('Вы ввели неправильную команду...')

def meme_feed_new():
    while (True):
        req = s.get(f'{config.host}/api/feed_new')
        if req.status_code != 200:
            if req.status_code == 204:
                print('\nМемов пока еще нет в базе(')
                return
            print('\nПри запросе возникла проблема!\nКод ошибки: ', req.status_code, ', сообщение: "',
                  json.loads(req.content)['detail'], '"', sep='')
            break
        else:
            resp = json.loads(req.content)
            print(
                f'\nID: {resp["id"]}\nКартинка: {resp["photo"]}\nАвтор: {resp["author"]}\nДата добавления: {datetime.strptime(resp["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")}\nКоличество лайков: {resp["likes"]}\n')
            print(' [1] Лайк, [2] Пропустить, [0] Выйти из меню')
            choice = int(input(' Ваш выбор: '))
            if choice == 1:
                req = s.post(f'{config.host}/api/like/{resp["id"]}')
                if req.status_code != 200:
                    print('\nПри запросе возникла проблема!\nКод ошибки: ', req.status_code, ', сообщение: "',
                          json.loads(req.content)['detail'], '"', sep='')
                    break
                else:
                    print(json.loads(req.content)['detail'])
            elif choice == 2:
                req = s.delete(f'{config.host}/api/like/{resp["id"]}')
                if req.status_code != 200:
                    print('\nПри запросе возникла проблема!\nКод ошибки: ', req.status_code, ', сообщение: "',
                          json.loads(req.content)['detail'], '"', sep='')
                    break
                else:
                    print(json.loads(req.content)['detail'])
            elif choice == 0:
                break
            else:
                print('Вы ввели неправильную команду...')

def show_stats():
    req = s.get(f'{config.host}/api/top')
    if req.status_code != 200:
        if req.status_code == 403:
            print('\nВам запрещен доступ сюда(')
            return
        print('\nПри запросе возникла проблема!\nКод ошибки: ', req.status_code, ', сообщение: "',
              json.loads(req.content)['detail'], '"', sep='')
    else:
        resp = json.loads(req.content)
        print(f'\nТоп-30 мемов по популярности:\nПоследнее обновление: {datetime.strptime(resp["last_updated"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")}\n')
        for i in range(len(resp['data'])):
            print(f'{i+1}) ID: {resp["data"][i]["id"]}\nКартинка: {resp["data"][i]["photo"]}\nАвтор: {resp["data"][i]["author"]}\nДата добавления: {datetime.strptime(resp["data"][i]["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")}\nКоличество лайков: {resp["data"][i]["likes"]}\n')

if __name__ == '__main__':
    print("Данный файл позволяет работать с backend сервиса в удобном виде.")
    print("Выберите одно из действий:")
    while(True):
        print('\n 1) Посмотреть все мемы (на 10 баллов)\n 2) Показать подборку мемов с сортировкой по дате (на 20 баллов)\n 3) Показать подборку мемов с определенным приоритетом (на 30 баллов)\n 4) Показать статистику (на 50 баллов)\n 0) Выйти из программы')
        task = int(input('Выберите действие: '))
        if task == 1:
            show_all()
        elif task == 2:
            meme_feed()
        elif task == 3:
            meme_feed_new()
        elif task == 4:
            show_stats()
        elif task == 0:
            print("До свидания!")
            exit(0)
        else:
            print('Повторите ввод!')