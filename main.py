from kivy.app import App
from kivy.uix.label import Label

class JaFlexDownloader(App):
    def build(self):
        return Label(text='JaFlex Downloader - Ready to Download Videos!')

if __name__ == '__main__':
    JaFlexDownloader().run()
