import os

from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField

font_size = 40

class CustomButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (.2, .2, .2, 1)
        self.background_color = (.76, .81, .82, 1)
        self.background_normal = ''
        self.background_down = ''

# Красная кнопка
class RedButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.font_size = font_size
        self.background_color = (.85, .1, .1, 1)

class ErrorPopup(Popup):

    def __init__(self, title='ВНИМАНИЕ!', label_text='', **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.title = title
        self.size_hint = (.75, .25)
        self.valid = 0
        self.layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        label = Label(text=label_text, font_size=font_size)
        self.ok_btn = RedButton(text='ОК',
                                on_press=lambda *args: self.btn_action(1))
        self.ok_btn.font_size = font_size
        self.layout.add_widget(label)
        self.layout.add_widget(self.ok_btn)
        self.content = self.layout

    def btn_action(self, action):
        self.valid = action
        self.dismiss()


class EditTask(Popup):

    def __init__(self, text_data='', title='РЕДАКТИРОВАНИЕ', **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.size_hint = (.9, .5)
        self.pos_hint={'top': .95}
        self.title = title
        self.valid = 0
        self.idx = 0
        self.text_data = text_data
        self.yes_now = Factory.YesNoPopup(label_text='Удалить заметку?')

        self.layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        self.input_field = MDTextField(font_size=font_size, size_hint_y=.7, multiline=True,
                                       mode='fill' if os.path.exists("C:\\Program Files") else 'filled',
                                       background_color=(0, 0, 0, .75), foreground_color=(1, 1, 1, 1))
        self.debug_label = Label(size_hint=(1, .25))
        self.buttons = GridLayout(cols=3, rows=2, padding=5, spacing=5, size_hint_y=.3)
        self.clear_text = RedButton(text='ОЧИСТИТЬ\n     ТЕКСТ', on_press=lambda *args: self.clear_all_text())
        self.select_all = RedButton(text='ВЫДЕЛИТЬ\n       ВСЁ', on_release=lambda *args: self.sel_all())
        self.del_sym = RedButton(text='<-', on_press=lambda *args: self.delete_sym())
        self.ok_btn = RedButton(text='ОК', on_press=lambda *args: self.get_text())
        self.del_btn = RedButton(text='УДАЛИТЬ\nЗАМЕТКУ', on_press=lambda *args: self.delete_task())
        self.cancel_btn = RedButton(text='ОТМЕНА', on_press=lambda *args: self.btn_action(-1))
        self.clear_text.font_size = 30
        self.select_all.font_size = 30
        self.del_btn.font_size = 30
        self.buttons.add_widget(self.clear_text)
        self.buttons.add_widget(self.select_all)
        self.buttons.add_widget(self.del_sym)
        self.buttons.add_widget(self.ok_btn)
        self.buttons.add_widget(self.del_btn)
        self.buttons.add_widget(self.cancel_btn)

        self.content = self.layout
        self.layout.add_widget(self.input_field)
        self.layout.add_widget(self.buttons)

    def sel_all(self):
        self.input_field.select_text(0, len(self.text_data))

    def clear_all_text(self):
        self.input_field.text = ''

    def delete_sym(self):

        if self.input_field.text:
            self.input_field.text = self.input_field.text[:-1]

    def on_open(self):
        self.input_field.text = self.text_data
        self.input_field.focus = True

    def get_text(self):
        self.valid = self.input_field.text
        self.dismiss()

    def delete_complete(self, dt):

        if self.yes_now.valid == 1:
            self.btn_action(-100)
            Clock.unschedule(self.delete_complete)
            self.yes_now.valid = 0
            self.yes_now.dismiss()
            self.dismiss()
        elif self.yes_now.valid == -1:
            self.yes_now.valid = 0
            self.yes_now.dismiss()

    def delete_task(self):
        self.yes_now.open()
        Clock.schedule_interval(self.delete_complete, .1)

    def btn_action(self, data):
        self.valid = data if data else 'Новое дело'
        self.dismiss()


class Popups(Popup):

    def __init__(self, title='ВНИМАНИЕ!', label_text='', **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.label_text = label_text
        self.title = title
        self.size_hint = (.75, .25)
        self.valid = 0
        self.layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        self.content = self.layout

    def btn_action(self, action, dismiss=True):
        self.valid = action

        if dismiss:
            self.dismiss()

class YesNoPopup(Popups):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text=self.label_text, font_size=20)
        box = BoxLayout(orientation='horizontal', padding=5, spacing=5)
        self.ok_btn = RedButton(text='ДА',
                                        on_press=lambda *args: self.btn_action(1),
                                        on_release=lambda *args: self.dismiss())
        self.ok_btn.font_size = 30
        self.cancel_btn = RedButton(text='НЕТ',
                                            on_press=lambda *args: self.btn_action(-1),
                                            on_release=lambda *args: self.dismiss())
        self.cancel_btn.font_size = 30
        box.add_widget(self.ok_btn)
        box.add_widget(self.cancel_btn)
        self.layout.add_widget(label)
        self.layout.add_widget(box)

class PinPopup(Popup):
    root_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, task_base, title='СПИСОК ДЕЛ НА СЕГОДНЯ:', **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.task_base = task_base
        self.size_hint = (.75, .75)
        self.title = title
        self.popup = None
        self.reopen = False
        self.font_size = 0

        self.layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        self.label_d = Label(font_size=self.font_size, size_hint_y=None, height=50)
        self.add_task_btn = RedButton(text='+', size_hint_y=.1,
                                      on_release=lambda *args: self.add_task())
        self.bck_btn = RedButton(text='НАЗАД', size_hint_y=.1, on_release=self.dismiss)
        self.task_block = GridLayout(size_hint_y=None, cols=1, padding=5, spacing=20)
        self.scroll = ScrollView(size_hint_y=1)
        self.task_list = {}

        self.content = self.layout
        self.layout.add_widget(self.label_d)

    def on_open(self):
        self.font_size = self.width / 20
        self.label_d.font_size = self.font_size

        for tsk in self.task_list:

            for wid in self.task_list[tsk].children:
                wid.font_size = self.font_size

    def _update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

    def set_task(self, i, idx, text, completed=False):
        max_long = 25
        new_pin = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=5, spacing=5)
        new_pin.add_widget(Label(text=f'{i}.', font_size=self.font_size, size_hint_x=.05))
        button_text = text[:max_long].replace("\n", " ")
        points = "." if len(text) <= max_long else "..."
        new_pin.add_widget(Button(text=f'{button_text}{points}',
                                  background_normal='', background_down='',
                                  background_color=(40/255, 40/255, 40/255, 1),
                                  font_size=self.font_size, size_hint_x=.8,
                                  on_press=lambda *args: self.edit_text(text, idx)))
        complete_cb = CheckBox(size_hint_x=.05, active=completed)
        complete_cb.bind(active=lambda *args: self.set_complete(idx))
        new_pin.add_widget(complete_cb)
        self.task_block.add_widget(new_pin)
        self.task_list[idx] = new_pin

    def waiter(self, dt):

        if self.popup.valid != 0:
            Clock.unschedule(self.waiter)

            if self.popup.valid == -100:
                self.task_base.delete_task(self.label_d.text, self.popup.idx)
                self.task_list[self.popup.idx].visible = False
            else:
                self.task_base.edit_task(self.label_d.text, self.popup.idx, self.popup.valid)

            self.popup = None
            self.dismiss()
            self.reopen = True

    def edit_text(self, text, idx):
        returned = EditTask(text_data=text)
        returned.idx = idx
        self.popup = returned
        returned.open()
        Clock.schedule_interval(self.waiter, .1)

    def show_task_list(self, task_list):
        self.task_block.bind(minimum_height=self.task_block.setter('height'))
        # print(task_list)

        for i, task in enumerate(task_list):
            # self.set_task(i + 1, task[0], task[1], True if task[2] > 0 else False)
            self.set_task(i + 1, task['id'], task['task'], True if task['completed'] > 0 else False)

        self.scroll.add_widget(self.task_block)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.add_task_btn)
        self.layout.add_widget(self.bck_btn)

        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 1))

    def add_task(self, task_text='Новое дело'):
        index, i = self.task_base.add_task(self.label_d.text, task_text, 0)
        self.set_task(i, index, task_text, False)
        self.edit_text(task_text, index)

    def set_complete(self, idx):
        self.task_base.complete_task(self.label_d.text, idx,
                                     completed=1 if self.task_list[idx].children[0].active else 0)
