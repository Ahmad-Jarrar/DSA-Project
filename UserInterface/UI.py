import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from functools import partial

class SearchArea(BoxLayout):
    
    def __init__(self):
        
        super().__init__(orientation='horizontal', spacing=20)
        self.txt = TextInput(hint_text='Search', multiline=False, on_text_validate=self.search,size_hint=(0.5,0.9))
        self.search_btn = Button(text='Search', on_press=self.search, size_hint=(0.1,0.9))
        self.clear_btn = Button(text='Clear All', on_press=self.clearText, size_hint=(0.1,0.9))
        self.add_widget(self.txt)
        self.add_widget(self.search_btn)
        self.add_widget(self.clear_btn)

    def search(self, instance):
        print("Query: " + self.txt.text)
        # self.clearText(instance)

    def clearText(self, instance):
 
        self.txt.text = ''

Builder.load_string('''
 
<ResultArea>:
 
    viewclass: 'Button'
    
    RecycleBoxLayout:
        
        size_hint_y: None
        
        height: self.minimum_height
        
        orientation: 'vertical'
        
''')

class ResultArea(RecycleView):
    def __init__(self, **kwargs):
 
        super(ResultArea, self).__init__(**kwargs)

        self.data = [{'text': "Link " + str(x), 'size_hint_x': 1.0} for x in range(20)]

class IndexPage(BoxLayout):
    def __init__(self):
        
        super().__init__(orientation='vertical', spacing=20)
        
        self.search_area = SearchArea()
        self.search_area.size_hint = (1.0, 0.2)
        self.result_area = ResultArea()
        self.add_widget(self.search_area)
        self.add_widget(self.result_area)

class SearchEngine(App):

    def build(self):
        return IndexPage()

if __name__ == "__main__":
    SearchEngine().run()