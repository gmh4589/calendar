#-*- coding:utf-8 -*-
import datetime

import kivy
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label

Builder.load_file('calendar.kv')

flag = int(datetime.datetime.now().strftime("%m"))

class MonthScreen(Screen):

	weekDays = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']
	month = {1:"ЯНВАРЬ", 2:"ФЕВРАЛЬ", 3:"МАРТ", 4:"АПРЕЛЬ", 5:"МАЙ", 6:"ИЮНЬ", 7:"ИЮЛЬ", 8:"АВГУСТ", 9:"СЕНТЯБРЬ", 10:"ОКТЯБРЬ", 11:"НОЯБРЬ", 12:"ДЕКАБРЬ"}
	month2 = int(datetime.datetime.now().strftime("%m"))
	year = int(datetime.datetime.now().strftime("%Y"))

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		for day in self.weekDays: self.ids['week'].add_widget(Label(text = day))
		self.createMonth(self.month2, self.year)

	def monthDay(self, year, mon):
		match mon:
			case 1 | 3 | 5 | 7 | 8 | 10 | 12: return 31
			case 4 | 6 | 9 | 11: return 30
			case 2:
				if year % 400 == 0: return 29
				if year % 100 == 0: return 28
				if year % 4 == 0: return 29
				else: return 28

	def createMonth(self, mon, year):
		prw = mon - 1 if mon - 1 != 0 else 12
		nxt = mon + 1 if mon + 1 != 13 else 1
		self.setMonth(mon, year)

		self.ids['backBTN'].text = self.month[prw]
		self.ids['forwBTN'].text = self.month[nxt]
		self.ids['backBTN'].on_press = lambda: self.chngMonth(prw, year, -1)
		self.ids['forwBTN'].on_press = lambda: self.chngMonth(nxt, year, 1)

		self.enptyWidget(datetime.date(year, mon, 1).isoweekday() - 1)
		self.setDays(self.monthDay(year, mon), mon, year)

	def setDays(self, days, mon, year):

		for i in range(days):
			if datetime.datetime.now().strftime('%Y-%m-%d') == str(datetime.date(year, mon, i + 1)): 
				color = (.1, .8, .2, 1)
			elif datetime.date(year, mon, i + 1).isoweekday() == 6 or datetime.date(year, mon, i + 1).isoweekday() == 7: 
				color = (.85, .1, .1, 1)
			else:color = (.45, .45, .6, 1)
			
			self.ids['dateScreen'].add_widget(
						Button(text = str(i + 1), 
						font_size = 30, background_normal = '', 
						background_down = '', 
						background_color = color))

	def setMonth(self, mon, year):
		self.ids['month'].clear_widgets()
		self.ids['month'].add_widget(Label(text = self.month[mon] + ' ' + str(year), font_size = 30))

	def enptyWidget(self, num):
		for i in range(num): self.ids['dateScreen'].add_widget(Label(text = ''))

	def chngMonth(self, mon, year, f):
		global flag
		flag += f
		plus = flag // 13

		if flag == 0:
			flag = 12
			year -= 1
		else: year += plus

		self.ids['dateScreen'].clear_widgets()
		self.createMonth(mon, year)

		if plus != 0: flag = 1

class CalendarApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		sm = ScreenManager()
		sm.add_widget(MonthScreen(name='NowYear'))
		return sm

CalendarApp().run()
