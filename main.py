import calendar
import datetime
import os
from random import randint

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.codeinput import CodeInput
from kivy.core.window import Window

Builder.load_file('calendar.kv')

def rgb(color):

	return (
		color[0] / 255,
		color[1] / 255,
		color[2] / 255,
		color[3] / 255,
	)

class CustomButton(Button):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.color = (.2, .2, .2, 1)
		self.background_color = (.76, .81, .82, 1)
		self.background_normal = ''
		self.background_down = ''


class MonthScreen(Screen):

	week_days = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
	months = {
		1:  ["ЯНВАРЬ", rgb((128, 200, 200, 200))],
	    2:  ["ФЕВРАЛЬ", rgb((36, 200, 204, 200))],
	    3:  ["МАРТ", rgb((220, 220, 60, 200))],
	    4:  ["АПРЕЛЬ", rgb((171, 230, 26, 200))],
	    5:  ["МАЙ", rgb((112, 200, 32, 200))],
	    6:  ["ИЮНЬ", rgb((252, 30, 12, 200))],
	    7:  ["ИЮЛЬ", rgb((230, 12, 50, 200))],
	    8:  ["АВГУСТ", rgb((255, 81, 81, 200))],
	    9:  ["СЕНТЯБРЬ", rgb((255, 201, 47, 200))],
	    10: ["ОКТЯБРЬ", rgb((255, 133, 50, 200))],
	    11: ["НОЯБРЬ", rgb((255, 99, 64, 200))],
	    12: ["ДЕКАБРЬ", rgb((126, 182, 254, 200))]
			  }

	w, h = Window.width, Window.height
	font_size = int(w / 20)
	month_now = int(datetime.datetime.now().strftime("%m"))
	year_now = int(datetime.datetime.now().strftime("%Y"))
	root_path = os.path.dirname(os.path.abspath(__file__))
	background_source = StringProperty(f"{root_path}/months/{month_now}/{randint(1, 5)}.jpg")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.move = []
		self.plus_month = None
		self.minus_month = None
		self.old = None

		self.lbl1 = Label(text='МЕСЯЦ:')
		self.lbl2 = Label(text='ГОД:')
		self.tf1 = CodeInput(font_size=40)
		self.tf2 = CodeInput(font_size=40)
		self.b_ok = CustomButton(text='ПЕРЕЙТИ')
		self.b_cancel = CustomButton(text='ОТМЕНА')
		self.lbl3 = Label()
		self.lbl4 = Label()

		for day in self.week_days:
			self.ids.week.add_widget(Label(text = day, font_size = self.font_size))

		self.create_month(self.month_now, self.year_now)
		self.ids.nowBTN.text = f"СЕЙЧАС: {self.months[self.month_now][0]} {self.year_now}"
		self.ids.nowBTN.on_press = lambda: self.create_month(self.month_now, self.year_now)

	def now_date_update(self, dt):
		self.ids.nowBTN.text = f"СЕЙЧАС: {self.months[int(datetime.datetime.now().strftime('%m'))][0]} {int(datetime.datetime.now().strftime('%Y'))}"

	def on_touch_down(self, touch):
		self.move = [touch.x]
		return super().on_touch_down(touch)

	def on_touch_move(self, touch):
		self.move.append(touch.x)
		return super().on_touch_move(touch)

	def on_touch_up(self, touch):

		if len(self.move) >= 2:

			if self.move[0] > self.move[-1]:  # Свайп влево
				self.plus_month()
			elif self.move[0] < self.move[-1]:  # Свайп вправо
				self.minus_month()

		self.move.clear()
		return super().on_touch_up(touch)

	def create_month(self, mon, year):
		Window.clearcolor = self.months[mon][1]

		if self.ids.dateScreen.cols != 7:
			return

		prw = mon - 1 if mon - 1 != 0 else 12
		nxt = mon + 1 if mon + 1 != 13 else 1
		self.ids.month.clear_widgets()
		self.background_source = f"{self.root_path}/months/{mon}/{randint(1, 5)}.jpg"
		self.ids.month.add_widget(Label(text=self.months[mon][0] + ' ' + str(year), font_size=self.font_size))
		self.ids.backBTN.text = self.months[prw][0]
		self.ids.forwBTN.text = self.months[nxt][0]
		self.ids.backBTN.background_color = self.months[prw][1]
		self.ids.forwBTN.background_color = self.months[nxt][1]
		self.plus_month = lambda: self.change_month(nxt, year if mon != 12 else year + 1)
		self.minus_month = lambda: self.change_month(prw, year if mon != 1 else year - 1)
		self.ids.backBTN.on_press = self.minus_month
		self.ids.forwBTN.on_press = self.plus_month
		self.ids.dateScreen.clear_widgets()
		days = calendar.monthrange(year, mon)[-1]

		for i in range(datetime.date(year, mon, 1).isoweekday() - 1):
			self.ids.dateScreen.add_widget(Label(text = ''))

		for i in range(days):

			if datetime.datetime.now().strftime('%Y-%m-%d') == str(datetime.date(year, mon, i + 1)):
				color = (.1, .8, .2, .75)
			elif datetime.date(year, mon, i + 1).isoweekday() == 6 or datetime.date(year, mon, i + 1).isoweekday() == 7:
				color = (.85, .1, .1, .75)
			else:
				color = (.95, .95, .95, .75)

			self.ids.dateScreen.add_widget(
						Button(text = str(i + 1),
					    color=(.2, .2, .2, 1),
						font_size = self.font_size,
					    background_normal = '',
						background_down = '',
						background_color = color))

	def change_month(self, mon, year):

		if self.ids.dateScreen.cols == 7 and 0 < year < 10000:
			self.ids.dateScreen.clear_widgets()
			self.create_month(mon, year)

	def jump_to_date(self):

		if self.old is None:
			self.old = list(self.ids.dateScreen.children)

		self.ids.dateScreen.clear_widgets()
		self.ids.dateScreen.rows = 8
		self.ids.dateScreen.cols = 2
		self.tf1.text = ''
		self.tf2.text = ''
		self.lbl3.text = ''
		self.lbl4.text = ''
		self.b_cancel.on_press = lambda *args: self.cancel_jump(self.old)
		self.b_ok.on_press = lambda *args: self.apply_jump(self.tf1.text, self.tf2.text)

		self.ids.dateScreen.add_widget(self.lbl1)
		self.ids.dateScreen.add_widget(self.lbl2)
		self.ids.dateScreen.add_widget(self.tf1)
		self.ids.dateScreen.add_widget(self.tf2)
		self.ids.dateScreen.add_widget(self.b_ok)
		self.ids.dateScreen.add_widget(self.b_cancel)
		self.ids.dateScreen.add_widget(self.lbl3)
		self.ids.dateScreen.add_widget(self.lbl4)

		for _ in range(8):
			self.ids.dateScreen.add_widget(Label())

	def apply_jump(self, m, y):

		try:
			m1 = int(m)
			y1 = int(y)

			if 0 < m1 < 13 and 0 < y1 < 10000:
				self.ids.dateScreen.rows = 6
				self.ids.dateScreen.cols = 7
				self.old = None
				self.change_month(m1, y1)
			else:
				self.lbl3.text = 'ВВЕДИТЕ КОРРЕКТУЮ ДАТУ!'
				self.lbl4.text = ''

		except (TypeError, ValueError):
			self.lbl3.text = 'ВВЕДИТЕ КОРРЕКТУЮ ДАТУ!'
			self.lbl4.text = ''

	def cancel_jump(self, old):
		self.ids.dateScreen.clear_widgets()
		self.ids.dateScreen.rows = 6
		self.ids.dateScreen.cols = 7
		self.old = None

		for widget in reversed(old):
			self.ids.dateScreen.add_widget(widget)


class CalendarApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		sm = ScreenManager()
		sm.add_widget(MonthScreen(name='NowYear'))
		return sm


CalendarApp().run()
