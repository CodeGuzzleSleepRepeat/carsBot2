import requests
import time
import urllib3
import pandas as pd
import json
import datetime
import asyncio
from threading import Thread




#TOKEN = '5127651114:AAGKbGTvpZlcZWEyhNPiJ-r4adPV0svrIV4'
URL = 'https://api.telegram.org/bot'
TOKEN = '5177823817:AAHM-d-I065pue_oLXvrsMNnVQTH0jJ9puw'



data = []


admin_name = [['fcknmaggot', '-1']]

supervisors = pd.DataFrame()
managers = pd.DataFrame()

chats = []
chat_ids = []
complaints = []

banned = set()

flag = {}
flag_data = {}
flag_car = {}
flag_admin = {}
flag_user = {}
flag_visor = {}
flag_mes = {}
flag_complaint = {}
counter = {}
num_of_photos = {}
gl_clas = {}
cur_manager = {}
cur_message = {}
cur_salon = {}
it2 = {}
it3 = {}
gl_flag = {}


start_pos = 20

def parse_data(date):
	global data
	global start_pos
	url_poster = 'https://api.maxposter.ru/partners-api/vehicles/active'
	headers = {'Content-type' : 'application/json', 'Authorization' : 'Basic Y2hlc3RhdnRvQG1heHBvc3Rlci5ydTpuNWsxZzdxRA'}
	fields = json.dumps({"filters" : [{"fields": "acquisitionDate","type": "greaterOrEqual","value": date}], "offset": "0","orders": ["-acquisitionDate"]})
	res = requests.post(f'{url_poster}', headers=headers, data=fields)
	pool = json.loads(res.text)['data']['vehicles']
	i = len(data)
	for car in pool:
		if str(car).find('price') > -1:
			price = str(car['price'])
		else:
			price = "Не указана"
		if str(car).find('generation') > -1:
			gen = str(car['generation']['name'])
		else:
			gen = "Не указано"
		if str(car).find('mileage') > -1:
			miles = str(car['mileage'])
		else:
			miles = "Не указан"
		if str(car).find('car_condition') > -1:
			if car['car_condition'] == 'excelent':
				cond = 'Отличное'
			else:
				cond = 'Среднее'
		else:
			cond = "Не указано"
		if str(car).find('modification') > -1:
			mod = str(car['modification']['name'])
		else:
			mod = "Не указана"
		if str(car).find('engineVolume') > -1:
			vol = str(car['engineVolume'])
		else:
			vol = "Не указан"
		if str(car).find('engineType') > -1:
			if str(car['engineType']) == 'petrol':
				eng_type = 'бензин'
			elif str(car['engineType']) == 'diesel':
				eng_type = 'дизель'
			else:
				eng_type = 'электро'
		else:
			eng_type = "Не указан"
		if str(car).find('gearboxType') > -1:
			if str(car['gearboxType']) == 'automatic':
				gear = 'автомат'
			else:
				gear = 'механика'
		else:
			gear = "Не указана"
		if str(car).find('driveType') > -1:
			if str(car['driveType']) == 'rear':
				driveType = 'задний'
			elif str(car['driveType']) == 'full_4wd':
				driveType = 'полный'
			else:
				driveType = 'передний'
		else:
			driveType = "Не указан"
		if str(car).find('complectation') > -1:
			if str(car['complectation']) == 'None':
				compl = "Не указана"
			else:
				compl = str(car['complectation']['name'])
		else:
			compl = "Не указана"
		if str(car).find('bodyConfiguration') > -1:
			body = str(car['bodyConfiguration']['name'])
		else:
			body = "Не указана"
		if str(car).find('steeringWheel') > -1:
			if str(car['steeringWheel']) == 'left':
				wheel = 'левый'
			else:
				wheel = 'правый'
		else:
			wheel = "Не указан"
		if str(car).find('uin') > -1:
			uin = str(car['uin'])
		else:
			uin = "Не указан"
		if str(car).find('bodyColor') > -1:
			color = str(car['bodyColor'])
		else:
			color = "Не указан"
		#if car.find('bodyConfiguration') > -1:
		#	 = str(car['bodyConfiguration']['name'])
		#else:
		#	body = "Не указана"



		ddd = ['id: ' + str(i), 'Марка и модель: ' + car['brand']['name']  + ' ' + car['model']['name'], 'Салон: ' + car['address'], 'Год выпуска: ' + str(car['year']),
		'Поколение: ' + gen, 'Пробег: ', miles + ' км', 'Модификация: ' + mod,
		 'Объем двигателя: ' + vol, 'Тип двигателя: ' + eng_type, 'Коробка передач: ' + gear, 'Привод: ' + driveType, 'Комплектация: ' + compl, 
		 'Тип кузова: ' + body, 'Цвет: ' + color, 'Руль: ' + wheel, 'VIN или номер кузова: ' + uin, 'Цена: ' + price] 

		start_pos = len(ddd)

		j = 0
		
		for photo in car['photos']:
			#pic = requests.get(photo['url']).content
			#file = open('car' + str(i) + '_photo' + str(j) + '.jpg', "wb")
			#file.write(pic)
			ddd.append('car' + str(i) + '_photo' + str(j) + '.jpg')
			j += 1

		print("Downloading photos: " + str(i) + " done")
		i += 1
		data.append(ddd)
	


def get_managers():
	file = open('managers.txt', "r")
	res = file.read()
	i = 0
	arr = res.split('\n')
	for line in arr:
		if line == '':
			continue
		pos1 = line.find(' ')
		pos2 = line.rfind(' ')
		managers[i] = (line[:pos1], line[pos1 + 1: pos2], line[pos2 + 1:])
		i += 1

def get_svisors():
	file = open('svisors.txt', "r")
	res = file.read()
	i = 0
	arr = res.split('\n')
	for line in arr:
		if line == '':
			continue
		pos1 = line.find(' ')
		pos2 = line.rfind(' ')
		supervisors[i] = (line[:pos1], line[pos1 + 1: pos2], line[pos2 + 1:])
		i += 1


def get_admins():
	file = open('admins.txt', "r")
	res = file.read()
	arr = res.split('\n')
	for line in arr:
		if line == '':
			break
		pos1 = line.find(' ')
		admin_name.append([line[:pos1], line[pos1 + 1:]])








def get_updates(offset=0):
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    return result['result']

def editMessage(mes_id, chat_id, text):
	requests.get(f'{URL}{TOKEN}/editMessage?chat_id={chat_id}&message_id={mes_id}&text={text}')



def sendMedia1(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia2(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia3(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia4(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia5(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia6(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia7(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-7"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb") 
	    , "random-name-7": open(data[int(text)][start_num + 6], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia8(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-7"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-8"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb") 
	    , "random-name-7": open(data[int(text)][start_num + 6], "rb") 
	    , "random-name-8": open(data[int(text)][start_num + 7], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia9(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-7"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-8"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-9"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb") 
	    , "random-name-7": open(data[int(text)][start_num + 6], "rb") 
	    , "random-name-8": open(data[int(text)][start_num + 7], "rb") 
	    , "random-name-9": open(data[int(text)][start_num + 8], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia10(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-7"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-8"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-9"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-10"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb") 
	    , "random-name-7": open(data[int(text)][start_num + 6], "rb") 
	    , "random-name-8": open(data[int(text)][start_num + 7], "rb") 
	    , "random-name-9": open(data[int(text)][start_num + 8], "rb") 
	    , "random-name-10": open(data[int(text)][start_num + 9], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)


def sendMedia(chat_id, ind, start_num):
	length = len(data[int(ind)]) - start_num
	if length == 1:
		sendMedia1(chat_id, ind, start_num)
	elif length == 2:
		sendMedia2(chat_id, ind, start_num)
	elif length == 3:
		sendMedia3(chat_id, ind, start_num)
	elif length == 4:
		sendMedia4(chat_id, ind, start_num)
	elif length == 5:
		sendMedia5(chat_id, ind, start_num)
	elif length == 6:
		sendMedia6(chat_id, ind, start_num)
	elif length == 7:
		sendMedia7(chat_id, ind, start_num)
	elif length == 8:
		sendMedia8(chat_id, ind, start_num)
	elif length == 9:
		sendMedia9(chat_id, ind, start_num)
	elif length == 10:
		sendMedia10(chat_id, ind, start_num)
	else:
		sendMedia10(chat_id, ind, start_num)
		sendMedia(chat_id, ind, start_num + 10)




def editMessageCaption(mes_id, chat_id, text, cur, photo_num, salon):
	caption = '\n'.join(data[int(text)][1:17])
	price = ''
	l = len(data[int(text)][17])
	f = True
	
	for i in range(l):
		price += data[int(text)][17][l - i - 1]
		if i % 3 == 2 and f:
			price += ' '
		if data[int(text)][17][l - i - 1] == ':':
			f = False
	p = price.rfind(' ')
	price = price[:p] + price[p + 1:]
	caption += '\n' + ''.join(reversed(price))
	reply_markup = {'inline_keyboard': [[{'text' : 'Связаться с менеджером', 'callback_data' : 'manager' + str(text) + '_' + str(salon)}]]}
	sendMedia(chat_id, text, 18)

	requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&reply_markup={json.dumps(reply_markup)}&text={caption}')
	


def editReplyMarkup(chat_id, clas, text):
	reply_markup = { "keyboard": [['Все авто'], ["Эконом (до 1 млн)"], ["Комфорт (от 1 до 3 млн)"], ["Премиум (от 3 до 10 млн)"], ["Элит (больше 10 млн)"], ["Выставить свою машину"]], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)



def reply_keyboard(chat_id, text):
	reply_markup = { "keyboard": [['Все авто'], ["Эконом (до 1 млн)"], ["Комфорт (от 1 до 3 млн)"], ["Премиум (от 3 до 10 млн)"], ["Элит (больше 10 млн)"], ["Выставить свою машину"], ['Оставить жалобу на менеджера']], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)		


def reply_admin_keyboard(chat_id, text):
	reply_markup = { "keyboard": [["Добавить админа"], ["Назначить менеджера"], ["Удалить менеджера"], ['Показать менеджеров'], ['Показать переписки'], ['Просмотреть жалобы']], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text' : text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

def reply_manager_keyboard(chat_id, text):
	reply_markup = { "keyboard": [["Удалить авто"], ['Забанить пользователя'], ['Разбанить пользователя']], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text' : text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

def reply_admin_manager_keyboard(chat_id, text):
	reply_markup = { "keyboard": [["Добавить админа"], ["Назначить менеджера"], ["Удалить менеджера"], ['Показать менеджеров'], ['Показать переписки'], ['Просмотреть жалобы'], ["Удалить авто"], ['Забанить пользователя'], ['Разбанить пользователя']], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text' : text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

def reply_keyboard_old_manager(chat_id, text, man):
	reply_markup = { "keyboard": [['Все авто'], ["Эконом (до 1 млн)"], ["Комфорт (от 1 до 3 млн)"], ["Премиум (от 3 до 10 млн)"], ["Элит (больше 10 млн)"], ["Выставить свою машину"], ['Вернуться к диалогу с ' + man], ['Оставить жалобу на менеджера']], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

def reply_svisor_keyboard(chat_id, text):
	reply_markup = { "keyboard": [['Показать переписки'], ['Переписка за день'], ['Переписка с пользователем']], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text' : text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)


def send_photo_url(chat_id, img_url):
    requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_url}&caption=hi')

def send_photo_file(chat_id, img, caption):
	file = {'photo' : open(img, 'rb'), 'caption' : caption}
	requests.post(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}', data=file)

def send_photo_file_id(chat_id, img, caption):
	return requests.post(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={img}&caption={caption}')

def send_message(chat_id, text):
	return json.loads(requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}').text)




def inline_keyboard(chat_id, ddd):
	for d in ddd:
		d += '\n'
	text = '\n'.join(ddd[1:5])
	l = len(ddd[17])
	price = ''
	f = True
	
	for i in range(l):
		price += ddd[17][l - i - 1]
		if i % 3 == 2 and f:
			price += ' '
		if ddd[17][l - i - 1] == ':':
			f = False
	
	p = price.rfind(' ')
	price = price[:p] + price[p + 1:]
	text += '\n' + ''.join(reversed(price))
	file =  {'photo' : open(ddd[18], 'rb')}
	salon = ddd[2][7:]
	reply_markup = {'inline_keyboard': [[{'text': 'Подробнее', 'callback_data' : 'show' + ddd[0] + '_' + salon}, {'text' : 'Связаться с менеджером', 'callback_data' : 'manager' + ddd[0] + '_' + salon}]]}
	data = {'chat_id': chat_id, 'caption': text, 'reply_markup': json.dumps(reply_markup)}
	return requests.post(f'{URL}{TOKEN}/sendPhoto', files=file, data = data)

def inline_keyboard_visor(chat_id, text):
	reply_markup = {'inline_keyboard': [[{'text' : 'id пользователя', 'callback_data' : 'id'}, {'text' : 'Ник пользователя', 'callback_data' : 'username'}, {'text' : 'Дата', 'callback_data' : 'date'}]]}
	data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
	return requests.get(f'{URL}{TOKEN}/sendMessage', data = data)

def inline_keyboard_compl(chat_id, text, i):
	reply_markup = {'inline_keyboard': [[{'text' : 'Просмотреть', 'callback_data' : 'compl' + str(i)}]]}
	data = {'chat_id': chat_id, 'text': 'Жалоба ' + str(i), 'reply_markup': json.dumps(reply_markup)}
	return requests.get(f'{URL}{TOKEN}/sendMessage', data = data)

def f_write(text, manager, client_id, client_name, time):
	file = open('messages.txt', "a+")
	file.write(text + ';;' + manager + ';;' + time.strftime('%m-%d-%y %H:%M:%S') + ';;' + str(client_id) + ';;' + client_name + '\n')	
	file.close()

def f_read():
	file = open('messages.txt', "r")
	res = file.read()
	arr = res.split('\n')
	file.close()	
	return arr

def get_mes(manager, chat_id):
	arr = f_read()
	i = 0
	for a in arr:
		if a == '':
			continue
		words = a.split(';;')
		if words[1] == manager:
			send_message(chat_id, str(words[2]) + ': ' + str(words[0]))
			i += 1
	if i == 0:
		send_message(chat_id, 'Таких переписок не найдено')

def get_mes_by_client(manager, client, chat_id):
	arr = f_read()
	i = 0
	for a in arr:
		if a == '':
			continue
		words = a.split(';;')
		if words[1].lower() == manager.lower() and words[3] == client:
			send_message(chat_id, str(words[2]) + ': ' + str(words[0]))
			i += 1
	if i == 0:
		send_message(chat_id, 'Таких переписок не найдено')

def get_mes_by_client_name(manager, client_name, chat_id):
	arr = f_read()
	i = 0
	for a in arr:
		if a == '':
			continue
		words = a.split(';;')
		if words[1].lower() == manager.lower() and words[4] == client_name[1:]:
			send_message(chat_id, str(words[2]) + ': ' + str(words[0]))
			i += 1
	if i == 0:
		send_message(chat_id, 'Таких переписок не найдено')

def get_mes_by_time(manager, day, chat_id):
	arr = f_read()
	mes = {}
	for a in arr:
		if a == '':
			continue
		words = a.split(';;')
		if words[1].lower() == manager.lower() and words[2][:8] == day:
			try:
				mes[words[2]] += str(words[2]) + ': ' + str(words[0] + '\n')
			except:
				mes[words[2]] = str(words[2]) + ': ' + str(words[0] + '\n')
	for m in mes:
		send_message(chat_id, m)

	if len(mes) == 0:
		send_message(chat_id, 'Таких переписок не найдено')

def get_mes_by_client_date(manager, date, client_id, chat_id):
	arr = f_read()
	i = 0
	for a in arr:
		if a == '':
			continue
		words = a.split(';;')
		print(words[1].lower(), manager.lower(), words[3], client_id, words[2][:8], date)
		if words[1].lower() == manager.lower() and words[3] == client_id and words[2][:8] == date:
			send_message(chat_id, str(words[2]) + ': ' + str(words[0]))
			i += 1
	if i == 0:
		send_message(chat_id, 'Таких переписок не найдено')


def add_admin(str):
	global admin_name
	file = open('admins.txt', "a+")
	if (str[0] != '@'):
		return 'Неверный ник'
	admin_name.append([str[1:], '-1'])
	file.write(str[1:])
	file.write(' ')
	file.write('-1')
	file.write('\n')
	it2[str[1:]] = 1
	return 'Админ успешно добавлен'

def add_manager(str):
	global managers
	file = open('managers.txt', "a+")
	pos = str.find(' ')
	if pos == -1 or pos == len(str) - 1:
		return 'Не указан салон (или слово Менеджер для менеджера по приему авто)'
	name = str[:pos]
	salon = str[pos + 1:]
	if (name[0] != '@'):
		return 'Неверный ник'
	name = name[1:]

	length_managers = len(managers.columns)
	managers[length_managers] = (name, salon, '-1')
	if length_managers > 0:
		file.write('\n')
	file.write(name)
	file.write(' ')
	file.write(salon)
	file.write(' ')
	file.write('-1')
	it2[name] = 1
	return 'Менеджер успешно добавлен, чтобы начать работу, менеджер должен отправить любое сообщение в бота'


def add_svisor(str):
	global supervisors
	file = open('svisors.txt', "a+")
	pos = str.find(' ')
	if pos == -1 or pos == len(str) - 1:
		return 'Не указан салон (или слово Супервизор для супервизора по приему авто)'
	name = str[:pos]
	salon = str[pos + 1:]
	if (name[0] != '@'):
		return 'Неверный ник'
	name = name[1:]

	length_managers = len(supervisors.columns)
	supervisors[length_managers] = (name, salon, '-1')
	if length_managers > 0:
		file.write('\n')
	file.write(name)
	file.write(' ')
	file.write(salon)
	file.write(' ')
	file.write('-1')
	it3[name] = 1
	return 'Супервизор успешно добавлен, чтобы начать работу, супервизор должен отправить любое сообщение в бота'

def delete_manager(name):
	global managers
	length = len(managers.columns)
	f = False
	file = open('managers.txt', "w")
	for i in range(length):
		try:
			if f:
				managers[i - 1] = managers[i]
			if (str(managers[i][0]) == str(name[1:])):
				#managers = managers.drop(columns = i)
				f = True
		except:
			break
	if f:
		managers = managers.drop(columns = length - 1)
	
	
	length = len(managers.columns)
	for i in range(length):
		try:
			file.write(managers[i][0])
			file.write(' ')
			file.write(managers[i][1])
			file.write(' ')
			file.write(str(managers[i][2]))
			file.write('\n')
		except:
			break

	it2[name[1:]] = 1

	if f:
		return 'Менеджер успешно удален'
	return 'Такого менеджера нет'


def delete_svisor(name):
	global supervisors
	length = len(supervisors.columns)
	f = False
	file = open('svisors.txt', "w")
	for i in range(length):
		try:
			if f:
				supervisors[i - 1] = supervisors[i]
			if (str(supervisors[i][0]) == str(name[1:])):
				f = True
		except:
			break
	if f:
		supervisors = supervisors.drop(columns = length - 1)
	
	
	length = len(supervisors.columns)
	for i in range(length):
		try:
			file.write(supervisors[i][0])
			file.write(' ')
			file.write(supervisors[i][1])
			file.write(' ')
			file.write(str(supervisors[i][2]))
			file.write('\n')
		except:
			break

	it3[name[1:]] = 1

	if f:
		return 'Супервизор успешно удален'
	return 'Такого супервизора нет'




def shpw_one_clas(message, clas, num, count):
	global last_clas
	global gl_flag
	
	price1 = 0
	price2 = 0
	j = 0
	if (clas.find('Эконом') == 0):
		
		price1 = 1000000
		price2 = 0
	elif (clas.find('Комфорт') == 0):
		price1 = 3000000
		price2 = 1000000
	elif (clas.find('Премиум') == 0):
		price2 = 3000000
		price1 = 10000000
	elif (clas.find('Элит') == 0):
		price2 = 10000000
		price1 = 100000000
	elif (clas.find('Все авто') == 0):
		price2 = 0
		price1 = 100000000
	else:
		return False

	cc = 0
	length = len(data)
	gl_flag[message['message']['chat']['id']] = 1
	for i in range(length):
		if int(data[i][17][6:]) < price1 and int(data[i][17][6:]) >= price2:
			if j >= count:
				inline_keyboard(message['message']['chat']['id'], data[i])
				cc += 1
			j += 1 
			if (j == num + count):
				break

	if count + 1 <= cc + count:
		editReplyMarkup(message['message']['chat']['id'], clas, 'Авто ' + str(count + 1) + '-' + str(cc + count)) 
	gl_clas[message['message']['chat']['id']] = clas
	if i == length - 1:
		send_message(message['message']['chat']['id'], 'Больше нет объявлений в этой категории')
	gl_flag[message['message']['chat']['id']] = 0
	return True

def send_file(message):
	global num_of_photos
	man = ""
	length = len(managers.columns)
	for i in range(length):
		try:
			if (managers[i][1].lower() == 'Менеджер'.lower()):
				man = managers[i][2]
				break
		except:
			break
	else:
		send_message(message['message']['chat']['id'], 'Менеджер еще не пользуется ботом')
		return -1

	if str(message).find('caption') > -1:
		cur_message[message['message']['chat']['id']] += 'Цена: ' + message['message']['caption']
	send_message(man, 'Новая машина от ' + message['message']['chat']['first_name'] + ' ' + str(message['message']['chat']['id'])[5:] + '. Чтобы написать пользователю - ответьте на его сообщение')
	username = ' '
	if str(message).find('username') > -1:
		username = message['message']['chat']['username']
	f_write('Новая машина от пользователя ' +  str(message['message']['chat']['id'])[5:] + '. Чтобы написать пользователю - ответьте на его сообщение', 'Менеджер', message['message']['chat']['id'], username, datetime.datetime.now())

	mes = message['message']['photo'][0]['file_id']
	return requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={man}&photo={mes}')

def send_car_data(message):
	length = len(managers.columns)
	man_id = -1
	for i in range(length):
		try:
			if (managers[i][1].lower() == 'Менеджер'.lower()):
				man_id = managers[i][2]
				break
		except:
			break

	username = str(message['message']['chat']['first_name'])
	try:
		send_message(man_id, 'Сообщение от пользователя ' + username + ' id ' + str(message['message']['chat']['id'])[5:] + ':\n' + str(cur_message[message['message']['chat']['id']]))
		username = ' '
		if str(message).find('username') > -1:
			username = message['message']['chat']['username']
		f_write('Сообщение от пользователя id ' + str(message['message']['chat']['id'])[5:] + ':\n' + str(cur_message[message['message']['chat']['id']]), 'Менеджер', message['message']['chat']['id'], username, datetime.datetime.now())
	except:
		send_message(message['message']['chat']['id'], 'Что-то пошло не так, пожалуйста, отправьте сообщение повторно')
	flag_car[message['message']['chat']['id']] = 0

def send_sticker(message):
	man = ""
	length = len(managers.columns)
	for i in range(length):
		try:
			if (managers[i][1].lower() == 'Менеджер'.lower()):
				man = managers[i][2]
				break
		except:
			break
	else:
		send_message(message['message']['chat']['id'], 'Менеджер еще не пользуется ботом')
		return -1

	if str(message).find('caption') > -1:
		cur_message[message['message']['chat']['id']] += 'Цена: ' + message['message']['caption']
	send_message(man, 'Новая машина от пользователя ' + str(message['message']['chat']['id'])[5:] + '. Чтобы написать пользователю - ответьте на его сообщение')
	mes = message['message']['sticker'][0]['file_id']
	return requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={man}&photo={mes}')




def check_message(message):
	if str(message).find('data') > -1:
		return 1



	global data
	global flag_data
	global flag
	global flag_car
	global flag_user
	global gl_flag
	global banned

	chat_id_cur = message['message']['chat']['id']

	if str(message).find('file') > -1 and flag_car[chat_id_cur] == 7:
		rrr = send_file(message).json()
		if rrr == -1:
			return 1

		chats.append([rrr['result']['message_id'], chat_id_cur])
		return 1
	

	if flag_car[chat_id_cur] == 7:
		cur_message[message['message']['chat']['id']] += 'Цена: ' + message['message']['text']
		send_car_data(message)
		

	if message['message']['text'] == 'Оставить жалобу на менеджера':
		send_message(message['message']['chat']['id'], 'Введите нзвание салона и дату диалога в формате mm-dd-yy')
		flag_complaint[chat_id_cur] = 1
		return 1

	if flag_complaint[chat_id_cur] == 1:
		if message['message']['text'].find('-') == -1 or message['message']['text'].find('-') == message['message']['text'].rfind('-'):
			send_message(name[1], 'Неправильно введена дата')
			flag_complaint[chat_id_cur] = 0
			return 1
		complaints.append(message['message']['text'] + ' ' + str(message['message']['chat']['id']))
		print(complaints)
		for name in admin_name:
			if name[1] != -1:
				send_message(name[1], 'Новая жалоба')
		return 1

	
	if str(message).find('reply_to_message') > -1:
		length = len(managers.columns)
		for j in range(length):
			if str(message['message']['chat']['id']) == str(managers[j][2]):
				for i in range (len(chats)):
					if message['message']['reply_to_message']['message_id'] == chats[i][0]:
						while gl_flag[chats[i][1]] == 1:
							time.sleep(1)
						if cur_manager[chats[i][1]][0] != managers[j][2] and cur_manager[chats[i][1]][0] != -1:
							reply_keyboard_old_manager(chats[i][1], 'Новое сообщение от менеджера ' + managers[j][1] + ', чтобы вернуться к диалогу с ним нажмите клавишу вернуться к диалогу', managers[j][1])
							flag_car[chats[i][1]] = 0
						if str(message['message']).find('photo') > -1:
							caption = ''
							if str(message).find('caption') > -1:
								caption = message['message']['caption']
							chats.append([send_photo_file_id(chats[i][1], message['message']['photo'][0]['file_id'], managers[j][1] + ': ' + caption)['result']['message_id'], message['message']['chat']['id']])
							username = ' '
							if str(message).find('username') > -1:
								username = message['message']['chat']['username']
							f_write(managers[j][1] + ': photo ' + message['message']['photo'][0]['file_id'], managers[j][1], chats[i][1], username, datetime.datetime.now())

						try:
							chats.append([send_message(chats[i][1], managers[j][1] + ': ' + message['message']['text'])['result']['message_id'], message['message']['chat']['id']])
							username = ' '
							if str(message).find('username') > -1:
								username = message['message']['chat']['username']
							f_write(managers[j][1] + ': ' + message['message']['text'], managers[j][1], chats[i][1], username, datetime.datetime.now())
						except:
							break
				return 1


	if str(message).find('file') > -1:
		return 1

	if str(message['message']['text']).find('Вернуться к диалогу') > - 1:
		man = message['message']['text'][len('Вернуться к диалогу с '):]
		try:
			for i in range(len(managers.columns)):
				if man == managers[i][1]:
					res = managers[i][2]
		except:
			send_message(message['message']['chat']['id'], 'Не удалось вернуться к диалогу, возможно менеджер был удален')
			return 1
		cur_manager[message['message']['chat']['id']][0] = res
		send_message(message['message']['chat']['id'], 'Вы вернулись к диалогу с ' + man)
		return 1

	
	if message['message']['text'] == 'Выставить свою машину':
		leng = len(managers.columns)
		for i in range(leng):
			try:
				if managers[i][1].lower() == 'Менеджер'.lower() and int(managers[i][2]) > -1:
					cur_manager[chat_id_cur][0] = managers[i][2]
					cur_manager[chat_id_cur][1] = managers[i][1]
					send_message(message['message']['chat']['id'], '1. Введите ваш город')
					break
			except:
				break
		else:
			cur_manager[chat_id_cur][0] = -1
			send_message(message['message']['chat']['id'], 'К сожалению, менеджер еще не пользуется ботом')
			return
		flag_car[chat_id_cur] = 1
		return
				
	
	

	for name in admin_name:
		username = ""
		if str(message['message']['chat']).find('username') > -1:
			username = str(message['message']['chat']['username'])
		if username == name[0] and message['message']['text'] == 'Показать менеджеров':
			length_m = len(managers.columns)
			for i in range(length_m):
				try:
					send_message(message['message']['chat']['id'], managers[i][0] + ' ' + managers[i][1])
				except:
					break
		if username == name[0] and message['message']['text'] == 'Показать супервизоров':
			length_m = len(supervisors.columns)
			for i in range(length_m):
				try:
					send_message(message['message']['chat']['id'], supervisors[i][0] + ' ' + supervisors[i][1])
				except:
					break
		if username == str(name[0]) and name[1] == -1:
			name[1] = message['message']['chat']['id']
		if username == str(name[0]) and message['message']['text'] == 'Назначить менеджера':
			send_message(name[1], "Введите ник менеджера и название салона (например, Мкад, 51-й километр) через пробел (для назначения менеджера по приему объявлений напишите просто Менеджер)")
			flag[chat_id_cur] = 1
			return 1
		if username == str(name[0]) and message['message']['text'] == 'Показать переписки':
			send_message(name[1], "Введите салон")
			flag_visor[chat_id_cur] = 1
			return 1
		if username == str(name[0]) and flag_visor[chat_id_cur] == 1:
			print(inline_keyboard_visor(chat_id_cur, 'Выберите критерий выбора переписки'))
			cur_salon[chat_id_cur] = message['message']['text']
			flag_visor[chat_id_cur] = 2
		if username == str(name[0]) and message['message']['text'] == 'Добавить админа':
			send_message(name[1], "Введите ник админа")
			flag_admin[chat_id_cur] = 1
			return 1
		if username == str(name[0]) and message['message']['text'] == 'Просмотреть жалобы':
			i = 0
			for compl in complaints:
				compl_arr = compl.split(' ')
				inline_keyboard_compl(name[1], compl_arr[len(compl_arr) - 2], i)
				i += 1
			return 1
		if username == str(name[0]) and message['message']['text'] == 'Удалить менеджера':
			send_message(name[1], "Введите ник менеджера")
			flag[chat_id_cur] = -1
			return 1
		if username == str(name[0]) and message['message']['text'] == 'Назначить супервизора':
			send_message(name[1], "Введите ник супервизора и название салона (например, Мкад, 51-й километр) через пробел (для назначения супервизора по приему объявлений напишите просто Супервизор)")
			flag_visor[chat_id_cur] = 1
			return 1
		if username == str(name[0]) and message['message']['text'] == 'Удалить супервизора':
			send_message(name[1], "Введите ник супервизора")
			flag_visor[chat_id_cur] = -1
			return 1

	
	length = len(managers.columns)
	length_data = len(data)
	length_visors = len(supervisors.columns)
	
	for i in range(length):
		try:
			if int(message['message']['chat']['id']) == int(managers[i][2]) and message['message']['text'] == 'Удалить авто':
				send_message(managers[i][2], "Введите id авто")
				flag_data[chat_id_cur] = 1
				return 1
			if int(message['message']['chat']['id']) == int(managers[i][2]) and message['message']['text'] == 'Забанить пользователя':
				send_message(managers[i][2], "Введите id пользователя")
				flag_user[chat_id_cur] = 1
				return 1
			if int(message['message']['chat']['id']) == int(managers[i][2]) and message['message']['text'] == 'Разбанить пользователя':
				send_message(managers[i][2], "Введите id пользователя")
				flag_user[chat_id_cur] = -1
				return 1
		except:
			break
	
	for i in range(length):
		try:
			if int(message['message']['chat']['id']) == int(managers[i][2]) and flag_data[chat_id_cur] == 1:
				for j in range(length_data):
					if data[j][0][4:] == message['message']['text']:
						data = data.pop(i)
						send_message(managers[i][2], "Авто успешно удалено")
						break
				else:
					send_message(managers[i][2], 'Авто с таким id не найдено')
				flag_data[chat_id_cur] = 0
				return 1
			if int(message['message']['chat']['id']) == int(managers[i][2]) and flag_user[chat_id_cur] == 1:
				banned.add(message['message']['text'])
				flag_user[chat_id_cur] = 0
				return 1
			if int(message['message']['chat']['id']) == int(managers[i][2]) and flag_user[chat_id_cur] == -1:
				banned.discard(message['message']['text'])
				flag_user[chat_id_cur] = 0
				return 1
		except:
			break




	for i in range(length_visors):
		try:
			if int(message['message']['chat']['id']) == int(supervisors[i][2]) and message['message']['text'] == 'Вся переписка':
				get_mes(supervisors[i][1], supervisors[i][2])
				return 1
			if int(message['message']['chat']['id']) == int(supervisors[i][2]) and message['message']['text'] == 'Переписка за день':
				send_message(supervisors[i][2], "Введите дату в формате mm-dd-yy")
				flag_mes[chat_id_cur] = 1
				return 1
			if int(message['message']['chat']['id']) == int(supervisors[i][2]) and message['message']['text'] == 'Переписка с пользователем':
				send_message(supervisors[i][2], "Введите id клиента")
				flag_mes[chat_id_cur] = -1
				return 1
		except:
			break

	for name in admin_name:
		try:
			if int(message['message']['chat']['id']) == int(name[1]) and flag_mes[chat_id_cur] == 2:
				get_mes_by_time(cur_salon[chat_id_cur], message['message']['text'], name[1])
				flag_mes[chat_id_cur] = 0
				return 1
			if int(message['message']['chat']['id']) == int(name[1]) and flag_mes[chat_id_cur] == -2:
				get_mes_by_client(cur_salon[chat_id_cur], message['message']['text'], name[1])
				flag_mes[chat_id_cur] = 0
				return 1
			if int(message['message']['chat']['id']) == int(name[1]) and flag_mes[chat_id_cur] == -3:
				get_mes_by_client_name(cur_salon[chat_id_cur], message['message']['text'], name[1])
				flag_mes[chat_id_cur] = 0
				return 1
		except:
			break

	
	
	for name in admin_name:
		username = ""
		if str(message['message']['chat']).find('username') > -1:
			username = str(message['message']['chat']['username'])
		if username == str(name[0]) and flag_admin[chat_id_cur] == 1:
			send_message(name[1], add_admin(message['message']['text']))
			flag_admin[chat_id_cur] = 0
			return 1
		if username == str(name[0]) and flag[chat_id_cur] == 1:
			send_message(name[1], add_manager(message['message']['text']))
			flag[chat_id_cur] = 0
			return 1

		if username == str(name[0]) and flag[chat_id_cur] == -1:
			send_message(name[1], delete_manager(message['message']['text']))
			flag[chat_id_cur] = 0
			return 1

		if username == str(name[0]) and flag_visor[chat_id_cur] == 1:
			send_message(name[1], add_svisor(message['message']['text']))
			flag_visor[chat_id_cur] = 0
			return 1

		if username == str(name[0]) and flag_visor[chat_id_cur] == -1:
			send_message(name[1], delete_svisor(message['message']['text']))
			flag_visor[chat_id_cur] = 0
			return 1



	num = length_data																				#Число авто за раз
	global counter
	print("HEllo")
	if shpw_one_clas(message, message['message']['text'], num, 0):
		counter[chat_id_cur] = 0
		return 1

	
	if message['message']['text'].find('Показать больше авто') > -1:
		clas = message['message']['text'][21:]
		counter[chat_id_cur] += num
		shpw_one_clas(message, clas, num, counter[chat_id_cur])
		return 1
	
	
	if flag_car[chat_id_cur] == 1:
		
		flag_car[chat_id_cur] = 2
		
		length = len(managers.columns)
		man_id = -1
		for i in range(length):
			try:
				if (managers[i][1].lower() == 'Менеджер'.lower()):
					man_id = managers[i][2]
					break
			except:
				break
		if int(man_id) == -1:
			send_message(message['message']['chat']['id'], 'К сожалению, менеджер еще не пользуется ботом')
			return 1
		cur_message[message['message']['chat']['id']] += 'Город: ' + message['message']['text'] + '\n'
		send_message(message['message']['chat']['id'], '2. Введите марку автомобиля')
		return 1


	

	elif len(cur_manager[chat_id_cur]) > 0:
		if int(cur_manager[chat_id_cur][0]) > -1 and flag_car[chat_id_cur] == 0:
			chats.append([send_message(cur_manager[chat_id_cur][0], 'От пользователя id ' + message['message']['chat']['first_name'] + str(message['message']['chat']['id'])[5:] + ': ' + message['message']['text'])['result']['message_id'], message['message']['chat']['id']])
			username = ' '
			if str(message).find('username') > -1:
				username = message['message']['chat']['username']
			f_write('От пользователя id ' + str(message['message']['chat']['id'])[5:] + ': ' + message['message']['text'], cur_manager[chat_id_cur][1], message['message']['chat']['id'], username, datetime.datetime.now())
			editReplyMarkup(message['message']['chat']['id'], gl_clas[chat_id_cur], 'Сообщение доставлено менеджеру')
			return 1
	
	if flag_car[chat_id_cur] == 2:
		cur_message[message['message']['chat']['id']] += 'Марка: ' + message['message']['text'] + '\n'
		send_message(message['message']['chat']['id'], '3. Отправьте модель')
		flag_car[chat_id_cur] = 3
		return 1

	if flag_car[chat_id_cur] == 3:
		cur_message[message['message']['chat']['id']] += 'Модель: ' + message['message']['text'] + '\n'
		send_message(message['message']['chat']['id'], '4. Отправьте пробег')
		flag_car[chat_id_cur] = 4
		return 1


	if flag_car[chat_id_cur] == 4:
		cur_message[message['message']['chat']['id']] += 'Пробег: '+ message['message']['text'] + '\n'
		send_message(message['message']['chat']['id'], '5. Отправьте VIN')
		flag_car[chat_id_cur] = 5
		return 1


	if flag_car[chat_id_cur] == 5:
		cur_message[message['message']['chat']['id']] += 'VIN: ' + message['message']['text'] + '\n'
		send_message(message['message']['chat']['id'], '6. Отправьте фото (формат .webp, к сожалению, не поддерживается) и ОТДЕЛЬНЫМ СООБЩЕНИЕМ желаемую цену')
		flag_car[chat_id_cur] = 7
		return 1

	



def find_manager(message):
	length = len(managers.columns)
	for i in range(length):
		try:
			message['callback_query']['data'][message['callback_query']['data'].find('_') + 1:].lower(), managers[i][1].lower()
			if message['callback_query']['data'][message['callback_query']['data'].find('_') + 1:].lower() == managers[i][1].lower():
				if int(managers[i][2]) > -1:
					return i
		except:
			break
	return -1



def check_query(message):
	if str(message).find('query') == -1:
		return


	global cur_manager

	chat_id_cur = message['callback_query']['message']['chat']['id']

	if message['callback_query']['data'].find('show') > -1:
		pos = message['callback_query']['data'].find('_')
		for i in range(len(data)):
			if data[i][0] == 'id: ' + message['callback_query']['data'][8:pos]:
				res = i
		editMessageCaption(message['callback_query']['message']['message_id'], message['callback_query']['from']['id'], res, 'hide', 17, message['callback_query']['data'][pos + 1:])
		return

	
	if message['callback_query']['data'] == 'date':
		send_message(message['callback_query']['message']['chat']['id'], "Введите дату в формате mm-dd-yy")
		flag_mes[chat_id_cur] = 2
		return 1
	if message['callback_query']['data'] == 'id':
		send_message(message['callback_query']['message']['chat']['id'], "Введите id клиента")
		flag_mes[chat_id_cur] = -2
		return 1
	if message['callback_query']['data'] == 'username':
		send_message(message['callback_query']['message']['chat']['id'], "Введите username клиента")
		flag_mes[chat_id_cur] = -3
		return 1

	if message['callback_query']['data'].find('compl') > -1:
		i = int(message['callback_query']['data'][5:])
		compl_arr = complaints[i].split(' ')
		print(compl_arr)
		l = len(compl_arr)
		manager = ''
		for i in range(l - 3):
			manager += compl_arr[i] + ' '
			print(manager)
		manager += compl_arr[l - 3]
		print(manager, compl_arr[l - 2], compl_arr[l - 1])
		get_mes_by_client_date(manager, compl_arr[l - 2], compl_arr[l - 1], message['callback_query']['message']['chat']['id'])
		flag_complaint[message['callback_query']['message']['chat']['id']] = 0
		return 1


	if message['callback_query']['data'].find('manager') > -1:
		man = find_manager(message)
		if not man == -1:
			if not cur_manager[chat_id_cur][0] == -1 and not cur_manager[chat_id_cur][0] == managers[man][2]:
				send_message(message['callback_query']['message']['chat']['id'], 'Вы начали диалог с менеджером салона ' + str(managers[man][1]) + '. Чтобы продолжить переписку с менеджером из салона ' + cur_manager[chat_id_cur][1] + ' еще раз свяжитесь с ним')
				flag_car[message['callback_query']['message']['chat']['id']] = 0
				length_chats = len(chats)
				for i in range(length_chats):
					if chats[i][1] ==  message['callback_query']['message']['chat']['id']:
						chats.pop(i)
						break    						#if manager == client - change?
			try:
				cur_manager[chat_id_cur][0] = managers[man][2]
				cur_manager[chat_id_cur][1] = managers[man][1]
				car_id = message['callback_query']['data'][7:message['callback_query']['data'].find('_')] 
				mes = car_id + ', ' + data[int(car_id[4:])][1] + ', ' + data[int(car_id[4:])][17] 			#???
				user = ''
				if str(message['callback_query']['message']['chat']).find('username') > -1:
					user = message['callback_query']['message']['chat']['username'] + ' '
				first_name = user + message['callback_query']['message']['chat']['first_name']
				#last_name = message['callback_query']['message']['chat']['last_name']
				chat_id = message['callback_query']['message']['chat']['id']
				chats.append([send_message(cur_manager[chat_id_cur][0], 'Сообщение от ' + first_name + ' ' + str(chat_id) + ' по поводу машины ' + mes)['result']['message_id'], chat_id])
				username = ' '
				if str(message).find('username') > -1:
					username = message['callback_query']['message']['chat']['username']
				f_write('Сообщение от пользователя ' + str(chat_id) + ' по поводу машины ' + mes, cur_manager[chat_id_cur][1], chat_id, username, datetime.datetime.now())
				send_message(chat_id, 'Менеджер ответит вам в ближайшее время')
			except:
				send_message(chat_id_cur, 'Произошел сбой, пожалуйста, отправьте запрос повторно')
		else:
			send_message(message['callback_query']['message']['chat']['id'], 'К сожалению, менеджер еще не пользуется ботом')
			#cur_manager[chat_id_cur][0] = -1
		return




def run():
	global banned

	date = datetime.date.today()
	tt = datetime.datetime.now()
	fl = True
	ban_flag = False
	it = {}

	parse_data("2019-01-01")
	
	get_admins()
	print("Admins: ", admin_name)
	get_managers()
	print("Managers: ", managers)
	get_svisors()
	print("Supervisors: ", supervisors)
	fl = True
	while fl:
		try:
			update_id = get_updates()[-1]['update_id']
			fl = False
		except:
			time.sleep(1)
	while True:
		cur_time = datetime.datetime.now()
		cur_date = datetime.date.today()
		if int(cur_time.minute) >= int(tt.minute) + 15:
			try:
				thread3 = Thread(target = parse_data, args = [str(date.year) + '-' + str(date.month) + '-' + str(date.day)])
				thread3.start()
				date = cur_date
				tt = cur_time
			except:
				print("Unable to get today`s updates")
		try:
			messages = get_updates(update_id)
		except:
			time.sleep(1)
		for message in messages:
			if update_id != message['update_id']:
				if update_id < message['update_id']:
					update_id = message['update_id']

									
				for ban in banned:
					if str(message).find('query') == -1:
						if str(ban) == str(message['message']['chat']['id']):
							ban_flag = True
							send_message(ban, 'Вы забанены')
					else:
						if ban == message['callback_query']['message']['chat']['id']:
							ban_flag = True
							send_message(ban, 'Вы забанены')

				if ban_flag:
					ban_flag = False
					continue

				try:

					for ch_id in chat_ids:
						if str(message).find('query') > -1:
							break
						if str(message).find('message') > -1:
							if message['message']['chat']['id'] == ch_id:
								break
					else:
						if str(message).find('query') == -1:	
							flag[message['message']['chat']['id']] = 0
							flag_data[message['message']['chat']['id']] = 0
							flag_car[message['message']['chat']['id']] = 0
							flag_admin[message['message']['chat']['id']] = 0
							flag_user[message['message']['chat']['id']] = 0
							flag_visor[message['message']['chat']['id']] = 0
							flag_mes[message['message']['chat']['id']] = 0
							flag_complaint[message['message']['chat']['id']] = 0
							counter[message['message']['chat']['id']] = 0
							num_of_photos[message['message']['chat']['id']] = 0
							cur_manager[message['message']['chat']['id']] = [-1, -1]
							cur_salon[message['message']['chat']['id']] = ''
							gl_clas[message['message']['chat']['id']] = '' 
							chat_ids.append(message['message']['chat']['id'])
							cur_message[message['message']['chat']['id']] = ''
							it[message['message']['chat']['id']] = 0
							gl_flag[message['message']['chat']['id']] = 0
							if str(message).find('username') > -1:
								it2[message['message']['chat']['username']] = 0
								it3[message['message']['chat']['username']] = 0
				except:
					continue


				username = ''
				length = len(managers.columns)
				length_v = len(supervisors.columns)
				if str(message).find('query') == -1:
					if str(message['message']['chat']).find('username') > -1:
						username = message['message']['chat']['username']
						for i in range(length):
							try:
								if len(managers[i]) == 0:
									break
								if str(managers[i][0]) == str(username):
									managers[i][2] = message['message']['chat']['id']
							except:
								break
						for name in admin_name:						
							if str(username) == name[0]:	
								name[1] = message['message']['chat']['id']
								
				if str(message).find('username') > -1 and str(message).find('query') == -1:
					if it2[message['message']['chat']['username']] == 1 or it3[message['message']['chat']['username']] == 1:
						it[message['message']['chat']['id']] = 0
				

				if str(message).find('query') == -1:
					if it[message['message']['chat']['id']] == 0:	

						username = ""
						if str(message['message']['chat']).find('username') > -1:
								username = message['message']['chat']['username']
						for name in admin_name:						
							if str(username) == name[0]:	
								name[1] = message['message']['chat']['id']
								
								for i in range(length):
									try:
										if managers[i][0] == name[0]:
											managers[i][2] = message['message']['chat']['id']
											reply_admin_manager_keyboard(message['message']['chat']['id'], 'Вас назаначили админом и менеджером')
											break
									except:
										break
								else:
									reply_admin_keyboard(message['message']['chat']['id'], 'Вас назаначили админом')
								break
						else:
							for j in range(length):
								try:
									if str(username) == str(managers[j][0]):
										managers[j][2] = message['message']['chat']['id']
										reply_manager_keyboard(managers[j][2], 'Вас назначили менеджером')
										break
								except:
									break
							else:
								for j in range(length_v):
									try:
										if str(username) == str(supervisors[j][0]):
											supervisors[j][2] = message['message']['chat']['id']
											reply_svisor_keyboard(supervisors[j][2], 'Вас назначили супервизором')
											break
									except:
										break
								else:
									text = 'Добро пожаловать!'
									if username != "":
										if it2[username] == 1:
											text = 'Вас удалили из списка менеджеров'
											flag_data[message['message']['chat']['id']] = 0
										if it3[username] == 1:
											text = 'Вас удалили из списка супервизоров'
											flag_visor[message['message']['chat']['id']] = 0
									reply_keyboard(message['message']['chat']['id'], text)
						it[message['message']['chat']['id']] = 1
						if username != "":
							it2[username] = 0
							it3[username] = 0
				
				mes1 = message
				mes2 = message
				try:
					thread1 = Thread(target=check_message, args=[mes1])
					thread2 = Thread(target=check_query, args=[mes2])
					thread1.start()
					thread2.start()
				except:
					send_message(message['message']['chat']['id'], 'Произошел сбой, пожалуйста, отправьте свое сообщение повторно')
				

run()
