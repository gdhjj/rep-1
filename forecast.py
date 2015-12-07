from pymongo import MongoClient
client = MongoClient()
db = client.test

#ввод номера магазина:
input_store_str = input("Please, type a store number from 1 to 500, to calculate forecast:""\n",) 
input_store = int(input_store_str)

#расчет тренда методом наименьших квадратов

def list_period(input_store):
	#заполняет список period порядковым номером периода продаж, данные значения являются отметками по оси x. 
	period = []
	global n
	n = db.train.find({"Store":input_store}).count() #кол-во периодов.
	period = [x+1 for x in range(n)]
	return period

def list_sales(input_store):
	#заполняет список sales сумами продаж за день, данные значения являются отметками по оси y.
	sales = []
	for i in db.train.find({"Store":input_store}):
	    sales.append(i["Sales"])
	return sales

#рассчитаем значения xy, x^2, y^2 для элементов списков period(x) и sales(y):
xy = list(map(lambda period, sales: period*sales, list_period(input_store), list_sales(input_store)))
x2 = [i**2 for i in list_period(input_store)]
y2 = [i**2 for i in list_sales(input_store)]

#просумируем значения для x, y, xy, x^2, y^2:
sum_x = sum(list_period(input_store))
sum_y = sum(list_sales(input_store))
sum_xy = sum(xy)
sum_x2 = sum(x2)
sum_y2 = sum(y2)

b = (n*sum_xy-sum_x*sum_y)/(n*sum_x2-(sum_x**2)) 
a = (sum_y/n) - b * (sum_x/n)

#функция тренда, для прогноза будующих продаж, где next_pr - прогнозный период в днях, кол-во которых вводит пользователь:
input_days = input("Please, type a number of days for period witch you want to forecast:""\n",) 
next_pr = int(input_days) + n

def forecast(next_pr):
	forecast = []
	i = n
	while i < next_pr:
		forecast.append(round(a + b*i,3))
		i+=1
	return forecast

print (forecast(next_pr))

input ()
