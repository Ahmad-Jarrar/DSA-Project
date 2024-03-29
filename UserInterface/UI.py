from random import sample
from string import ascii_lowercase

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

import time
from functools import partial

from config import *
from Lexicon.lexicon import load_lexicon
from Indexing.ForwardIndex import *
from Indexing.InvertedIndex import *
from helper.functions import *
from Search.Search import Searcher


kv = """
<Row@BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Rectangle:
            size: self.size
            pos: self.pos
    value: 'Search App'
    Label:
        text: root.value
<SearchEngine>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    name: "main"
    resultArea: resultArea
    search_box: search_box
    orientation: 'vertical'
    GridLayout:
        cols: 3
        rows: 1
        size_hint_y: None
        height: dp(96)
        padding: dp(12)
        spacing: dp(24)
        Button:
            text: 'Update Lexicon'
            on_press: root.update_lexicon()
        Button:
            text: 'Update Index'
            on_press: root.update_index()
        Button:
            text: 'Clear'
            on_press: root.clear()
    
    BoxLayout:
        size_hint_y: None
        height: dp(96)
        padding: dp(12)
        spacing: dp(24)
        TextInput:
            id: search_box
            size_hint_x: 1.5
            multiline:False
            hint_text: 'Search'
            on_text_validate: root.search(search_box.text)
            padding: dp(10), dp(10), 0, 0
        Button:
            text: 'Search'
            on_press: root.search(search_box.text)
        
    RecycleView:
        id: resultArea
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        padding: dp(10), dp(10), dp(10), dp(10)
        bar_width: dp(10)
        viewclass: 'Button'
        RecycleBoxLayout:
            default_size: None, dp(64)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)
"""

Builder.load_string(kv)

class WrappedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

class PostView(Popup):
    def __init__(self, content):
        super().__init__(title=content['title'], size_hint=(1., 1.))

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(WrappedLabel(text=content['url'], size_hint=(1.0, 0.2), font_size="14sp"))
        scroll = ScrollView()
        scroll.add_widget(WrappedLabel(text=content['text'], size_hint=(1.0, None), font_size="20sp"))
        box.add_widget(scroll)
        
        box.add_widget(Button(text="Back", on_press=self.dismiss, size_hint=(1., 0.15)))
        self.content = box
        self.open()

class SearchEngine(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_paths()
        self.searcher = Searcher()

    

    def update_lexicon(self):
        content = Button(text='Dismiss')
        popup = Popup(title='Warning!\n For Initial Lexicon build by uncommenting in run.py\n Else it will cause program to no respond', content=content, size_hint=(0.5, 0.2), auto_dismiss=False)

        content.bind(on_press=popup.dismiss)
        popup.open()
        self.searcher.lexicon = load_lexicon(update=True)

    def search(self, query):
        print(query)

        if len(parse_string(query)) < 1:
            return

        try:
            start = time.process_time()
            results = self.searcher.search(query, limit=40)
            self.resultArea.data = [{'text': result['title'], 'on_press': partial(self.open_post, content=result)} for result in results]
            self.resultArea.refresh_from_data()
            print("Elapsed Time: " + str(time.process_time() - start))
        except Exception:
            content = Button(text='Dismiss')
            popup = Popup(title='Exception\nword not in dictionary!', content=content, size_hint=(0.4, 0.2), auto_dismiss=False)

            content.bind(on_press=popup.dismiss)
            popup.open()
    
    # True
    def update_index(self):
        content = Button(text='Continue', size_hint=(0.9, 0.9))
        popup = Popup(title='Index new Files\n add your files in a folder to path:\n{}'.format(DATA_PATH), content=content, size_hint=(0.6, 0.25), auto_dismiss=False)
        content.bind(on_press=popup.dismiss)
        popup.open()
        popup.bind(on_dismiss=self.reindex)
        pass
    def reindex(self, _):
        forward_index()
        inverted_index()
        self.searcher.initialize()

    def clear(self):
        self.resultArea.data = []
        self.search_box.text = ""

    def open_post(self, content=None):
        return PostView(content)

class SearchEngineApp(App):
    def build(self):
        return SearchEngine()


if __name__ == '__main__':
    SearchEngineApp().run()