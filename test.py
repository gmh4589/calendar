from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

kv = """
#:import Factory kivy.factory.Factory

<AddAccount>:
    auto_dismiss: False
    title: 'Add ' + root.type
    size_hint: .7, .7
    BoxLayout:
        orientation: "vertical"
        AnchorLayout:
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: 30
                Label:
                    text: root.type + " Name"
                TextInput:
                    id: ti
                    multiline: False
        BoxLayout:
            orientation: "horizontal"
            size_hint: (None, None)
            spacing: 10
            size: 200,30
            pos_hint: {'center_x': .5}
            Button:
                text: "Save"
                on_release:
                    app.root.ids.label.text = ti.text
                    root.dismiss()
            Button:
                text: "Cancel"
                on_release: root.dismiss()

BoxLayout:
    orientation: 'vertical'
    Label:
        id: label
        text: 'Test Popup'
    Button:
        size_hint_y:None
        height: 48
        text: 'Open Popup'
        on_release: Factory.AddAccount().open()
"""


class AddAccount(Popup):
    type = StringProperty('New Account')

class NewPopTestApp(App):
    def build(self):
        return Builder.load_string(kv)


NewPopTestApp().run()