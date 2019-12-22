from random import sample
from string import ascii_lowercase

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

import time

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
            text: 'Build Lexicon'
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


class SearchEngine(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.searcher = Searcher()

    

    def update_lexicon(self):
        self.searcher.lexicon = load_lexicon(update=True)

    def search(self, query):
        print(query)

        if len(parse_string(query)) < 1:
            return

        try:
            results = self.searcher.search(query, limit=40)
            self.resultArea.data = [{'text': result['title']} for result in results]
            self.resultArea.refresh_from_data()
        except Exception as e:
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


class SearchEngineApp(App):
    def build(self):
        return SearchEngine()


if __name__ == '__main__':
    SearchEngineApp().run()