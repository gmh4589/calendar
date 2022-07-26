#-*- coding:utf-8 -*-
import time
import datetime
from calendar import monthrange

import kivy
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

Builder.load_file('calendar.kv')

flag = int(datetime.datetime.now().strftime("%m"))

class MonthScreen(Screen):

	weekDays = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']
	month = ['', "ЯНВАРЬ", "ФЕВРАЛЬ", "МАРТ", "АПРЕЛЬ", "МАЙ", "ИЮНЬ", "ИЮЛЬ", "АВГУСТ", "СЕНТЯБРЬ", "ОКТЯБРЬ", "НОЯБРЬ", "ДЕКАБРЬ"]
	month2 = int(datetime.datetime.now().strftime("%m"))
	year = int(datetime.datetime.now().strftime("%Y"))

	def __init__(self, **kwargs):

		super().__init__(**kwargs)
		for i in range(7):
			self.ids['week'].add_widget(Label(text = self.weekDays[i]))
		self.createMonth(self.month2, self.year)

	def createMonth(self, mon, year):

		prw = mon - 1 if mon - 1 != 0 else 12
		nxt = mon + 1 if mon + 1 != 13 else 1
		self.setMonth(mon, year)

		self.ids['backBTN'].text = self.month[prw]
		self.ids['forwBTN'].text = self.month[nxt]
		self.ids['backBTN'].on_press = lambda: self.chngMonth(prw, year, -1)
		self.ids['forwBTN'].on_press = lambda: self.chngMonth(nxt, year, 1)

		self.enptyWidget(datetime.date(year, mon, 1).isoweekday() - 1)
		self.setDays(monthrange(year, mon)[1], mon, year)

	def setDays(self, days, mon, year):

		for i in range(days):
			if datetime.date(year, mon, i + 1).isoweekday() == 6 or datetime.date(year, mon, i + 1).isoweekday() == 7:
				color = (.85, .1, .1, 1)
			elif datetime.datetime.now().strftime('%Y-%m-%d') == str(datetime.date(year, mon, i + 1)):
				color = (.1, .8, .2, 1)
			else:
				color = (.45, .45, .6, 1)
			self.ids['dateScreen'].add_widget(Button(text = str(i + 1), font_size = 30, background_normal = '', 
												background_down = '', background_color = color))

	def setMonth(self, mon, year):

		self.ids['month'].clear_widgets()
		self.ids['month'].add_widget(Button(text = str(self.month[mon]) + ' ' + str(year), background_normal = '', 
													font_size = 30, background_down = '', 
													background_color = (.21, .56, .18, 1)))

	def enptyWidget(self, num):

		for i in range(num):
			self.ids['dateScreen'].add_widget(Button(text = '', background_normal = '', 
												background_down = '', background_color = (.21, .56, .18, 1)))

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
