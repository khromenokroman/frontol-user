#!/usr/bin/env python3
from random import randint
import json
import os
from time import sleep

#константы
JSON_FILE = 'info_user.json'
PATH_KASSA1 = '/home/raipo/share/kassa1/'
PATH_KASSA2 = '/home/raipo/share/kassa2/'

#методы
def create_users(users = {}):

    repeat = 'д'

    while repeat == 'д':
        info_user = {}
        pin_card = 0
        password = 0
        #получаем инфу по сотруднику
        name = input('Введите имя сотрудника: ')
        password = randint(1,1000000)
        pin_card = input('Введите номер карты сотрудника: ')
        if pin_card == '':
            pin_card = randint(1,10000000)
        role = input('Введите полномочия сотрудника:\n\t1-кассир\n\t2-старший кассир\n')
        print('\n')
        try:
            if int(role) == 1:
                print(f'Добавлен сотрудник {name.title()}\n\tПрава: кассир\n\tНомер карты: {pin_card}\n\tПароль: {password}')
            elif int(role) == 2:
                print(f'Добавлен сотрудник {name.title()}\n\tПрава: старший кассир\n\tНомер карты: {pin_card}\n\tПароль: {password}')
            else:
                print('Вы должны указать целое число 1 или 2\nПробуйте еще...')
                continue
            print('\n')
        except:
            print('Вы должны указать целое число 1 или 2\nПробуйте еще...')
            continue

        #добавим в словарь
        try:
            info_user['password'] = int(password)
            info_user['pin_card'] = int(pin_card)
            info_user['role'] = int(role)
            users[name] = info_user
        except:
            print('Введены не корректные данные, пробуйте еще...')
            continue
        #узнаем еще надо создавть или нет
        repeat = input('Добавить еще одного сотрудника? [д\н]')

    #print(users)
    #пишем в json
    with open(JSON_FILE, 'w') as f:
        json.dump(users, f, sort_keys=True, indent=4, ensure_ascii=False)

def load_info():
    #читаем из json
    try:
        with open(JSON_FILE) as f:
            info_users = json.load(f)
        print(json.dumps(info_users,sort_keys=True, indent=4, ensure_ascii=False))
        return info_users
    except:
        info_users = {}
        return info_users

def download_kassa(path, f_name, fl_name):

    directory = path + fl_name
    #создадим файл флаг
    with open(directory, 'w') as f:
        f.write('')

    directory = path + f_name
    #создадим главный файл
    users = load_info()
    text_in_file = f'##@@&&\n#\n$$$DELETEALLUSERS\n$$$ADDUSERS\n1;Системный администратор;Системный администратор;1;147896325;;;\n'
    count = 2
    for name, info in users.items():
        if info.get('role') == 1: #кассир
            personal_string = f'{count};{name};{name};{4};{info.get("password")};;;\n' 
        elif info.get('role') == 2: #старший кассир
            personal_string = f'{count};{name};{name};{3};{info.get("password")};{info.get("pin_card")};;\n' 
        count += 1
        text_in_file += personal_string
    
    with open(directory, 'w', encoding='cp1251') as f:
        f.write(text_in_file)
     

if __name__ == '__main__':
    
    answer = 0

    while True:
        
        os.system('clear')
        print('Что хотите сделать:\n\n\t1-просмотреть сотрудников\n\t2-добавить сотрудников\n\t3-удалить сотрудникa\n\t4-Выгрузить сотрудников на кассы\n\t5-выход')
        answer = input('Ответ: ')
        try:
            int(answer)
        except:
            print('Необходимо вводить целые числа от 1 до 5...')
            sleep(5)
            os.system('clear')
            continue
        if int(answer) == 1:
            load_info()
            input('Для продолжения нажмите Enter...')
        elif int(answer) == 2:
            users = load_info()
            create_users(users)
        elif int(answer) == 3:
            users = load_info()
            user = input('Введите имя удаляемого сотрудника: ')
            del users[user]
            with open(JSON_FILE, 'w') as f:
                json.dump(users, f, sort_keys=True, indent=4, ensure_ascii=False)
        elif int(answer) == 4:
            download_kassa(PATH_KASSA1,'Pos01.spr', 'Pos01.flz')
            download_kassa(PATH_KASSA2,'Pos02.spr', 'Pos02.flz')
            #print('Касса1 загружена...')
            print('='*20)
            input('Выгрузка сотрудников на кассы произведена\nДля продолжения нажмите Enter...')
        elif int(answer) == 5:
            print('Всего доброго!')
            break
        else:
            print('Необходимо вводить целые числа от 1 до 5...')
            sleep(5)
