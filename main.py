from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class AutoDnsRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(AutoDnsRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20
        
        # ခေါင်းစဉ် စာသား
        self.title_label = Label(
            text='Auto-DNS Manager',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.title_label)
        
        # အခြေပြ စာသား
        self.status_label = Label(
            text='Status: Ready to configure DNS',
            font_size='16sp'
        )
        self.add_widget(self.status_label)
        
        # ခလုတ် (Button)
        self.action_btn = Button(
            text='Start Process',
            size_hint_y=None,
            height=60
        )
        self.action_btn.bind(on_press=self.on_button_click)
        self.add_widget(self.action_btn)

    def on_button_click(self, instance):
        self.status_label.text = 'Status: Running DNS task...'

class AutoDnsApp(App):
    def build(self):
        return AutoDnsRoot()

if __name__ == '__main__':
    AutoDnsApp().run()

