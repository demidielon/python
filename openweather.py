from interface import clear, interface

import os
import urllib.request
import urllib.parse
import gzip
import json

import sqlite3
from sqlite3 import Error

# Параметры удаленной базы данных списка городов
BASE_PATH = 'data'
LIST_NAME = 'city.list'
LIST_URL = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
SOURCE_LINK = 'http://api.openweathermap.org/data/2.5/weather'
APPID_FILE = 'app.id'


interface.selected_city = None


def url_request(url, params, method="GET"):
    if method == "POST":
        return urllib.request.urlopen(url, data=urllib.parse.urlencode(params))
    else:
        return urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params))


def appid():
    # Получение App ID из файла
    with open(APPID_FILE, encoding="utf-8") as appid:
        result = appid.read()
        return result


def init_citylist():
    # Проверка наличия рабочей директории
    if not os.path.exists(BASE_PATH):
        os.mkdir(BASE_PATH)

    # Проверка наличия списка городов
    if not os.path.isfile(os.path.join(BASE_PATH, LIST_NAME+'.json')):
        print('Список городов подготавливается...')

        # Загрузка архива
        if not os.path.isfile(os.path.join(BASE_PATH, LIST_NAME + '.json.gz')):
            print('Загрузка файла из интернета...')
            try:
                urllib.request.urlretrieve(LIST_URL, os.path.join(BASE_PATH, LIST_NAME+'.json.gz'))
            except urllib.error.URLError:
                print('Ошибка: не удалось загрузить базу данных')
            else:
                print('База городов успешно загружена')

        # Распаковка архива
        if not os.path.isdir(os.path.join(BASE_PATH, LIST_NAME+'.json.gz')):
            with gzip.open(os.path.join(BASE_PATH, LIST_NAME+'.json.gz'), 'rb') as in_file:
                s = in_file.read()
            open(os.path.join(BASE_PATH, LIST_NAME+'.json'), 'wb').write(s)
            print('База городов успешно распакована')

    # Преобразование списка городов из JSON в словарь
    with open(os.path.join(BASE_PATH, LIST_NAME+'.json'), encoding="utf-8") as file:
        city_list = json.load(file)

    return city_list


def check_inter():
    print(init_citylist())

def city_select():
    city_list = init_citylist()
    country_list = []
    for city in city_list:
        if city['country'] not in country_list and city['country'] != '':
            country_list.append(city['country'])
    country_list.sort()

    clear()
    print('Список стран:')
    for key in range(len(country_list)//20+1):
        print(str(country_list[key*20:key*20+20]))
    input_country = input('\nУкажите страну: ')

    filtred_city_list = []
    for city in city_list:
        if city['country'] == input_country:
            filtred_city_list.append(city['name'])
    filtred_city_list.sort()

    if filtred_city_list == []:
        interface.selected_city = None
        clear()
        print('Указанная страна не найдена\n')
        return

    clear()
    print('Список городов:')
    for key in range(len(filtred_city_list)//5+1):
        print(str(filtred_city_list[key*5:key*5+5]))
    input_city = input('\nУкажите город: ')

    for city in city_list:
        if city['name'] == input_city:
            interface.selected_city = city
            clear()
            print(f'Выбранный город: {interface.selected_city}\n')
            break
        else:
            interface.selected_city = None

    if interface.selected_city is None:
        interface.selected_city = None
        clear()
        print('Такого города нет в списке\n')


def print_selected_city():
    clear()
    print(f'Выбранный город: {interface.selected_city}\n')


def print_weather():
    if interface.selected_city is not None:
        params = dict(
            id=interface.selected_city['id'],
            units='metric',
            appid=appid()
        )
        try:
            data = json.load(url_request(SOURCE_LINK, params))
        except urllib.error.URLError:
            print('Ошибка соединения\n')
        else:
            print(f'Погода в городе: {interface.selected_city["name"]}\nСтрана: {interface.selected_city["country"]}')
            print(f'Основная информация: {data["weather"][0]["main"]} - {data["weather"][0]["description"]}')
            print(f'Температура: {data["main"]["temp"]} градусов по Цельсию')
            print()


clear()
tasks = {'0': (city_select, 'Выбрать город', []),
         '1': (print_selected_city, 'Вывести на экран выбранный город', []),
         '2': (print_weather, 'Какая погода в выбранном городе')}

interface(tasks)

