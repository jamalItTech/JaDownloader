from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import yt_dlp
import threading
import os

stop_download = False
dark_mode = True

languages = {
    "English": {
        "url": "Video or Playlist URL:",
        "type": "Select download type:",
        "logs": "Logs:",
        "download": "Download",
        "cancel": "Cancel Download",
        "about": "About Developer"
    },
    "Arabic": {
        "url": "رابط الفيديو أو القائمة:",
        "type": "اختر نوع التحميل:",
        "logs": "سجل التحميل:",
        "download": "تحميل",
        "cancel": "إلغاء التحميل",
        "about": "عن المطور"
    }
}

developer_info = """
JaFlex Downloader v1.0
Developed by: Jamal Alqadi
Email: jamal77alqadi@gmail.com
Phone: +967783234301
"""

class Downloader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.padding = 10
        self.spacing = 10
        self.current_language = "English"

        # اختيار اللغة
        self.lang_spinner = Spinner(
            text='English',
            values=('English', 'Arabic')
        )
        self.lang_spinner.bind(text=self.change_language)
        self.add_widget(self.lang_spinner)

        # الواجهة
        self.labels = {}
        self.labels['url'] = Label(text=languages["English"]["url"])
        self.add_widget(self.labels['url'])

        self.url_input = TextInput(multiline=False)
        self.add_widget(self.url_input)

        self.labels['type'] = Label(text=languages["English"]["type"])
        self.add_widget(self.labels['type'])

        self.quality_spinner = Spinner(
            text='Best Quality (Video + Audio)',
            values=('Best Quality (Video + Audio)', 'Lowest Video Quality', 'Audio Only (MP3)')
        )
        self.add_widget(self.quality_spinner)

        self.labels['logs'] = Label(text=languages["English"]["logs"])
        self.add_widget(self.labels['logs'])

        self.logs = Label(text="", size_hint_y=None)
        self.logs.bind(texture_size=self.logs.setter('size'))
        scroll = ScrollView(size_hint=(1, 0.4))
        scroll.add_widget(self.logs)
        self.add_widget(scroll)

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.download_btn = Button(text=languages["English"]["download"])
        self.download_btn.bind(on_press=self.start_download)
        btn_layout.add_widget(self.download_btn)

        self.cancel_btn = Button(text=languages["English"]["cancel"])
        self.cancel_btn.bind(on_press=self.cancel_download)
        btn_layout.add_widget(self.cancel_btn)

        self.add_widget(btn_layout)

        self.about_btn = Button(text=languages["English"]["about"])
        self.about_btn.bind(on_press=self.show_about)
        self.add_widget(self.about_btn)

    def change_language(self, spinner, text):
        self.current_language = text
        lang = languages[text]
        self.labels['url'].text = lang["url"]
        self.labels['type'].text = lang["type"]
        self.labels['logs'].text = lang["logs"]
        self.download_btn.text = lang["download"]
        self.cancel_btn.text = lang["cancel"]
        self.about_btn.text = lang["about"]

    def log(self, text):
        self.logs.text += text + "\n"

    def cancel_download(self, instance):
        global stop_download
        stop_download = True
        self.log("⛔️ Download cancelled by user.")

    def start_download(self, instance):
        global stop_download
        stop_download = False
        url = self.url_input.text
        quality = self.quality_spinner.text

        if not url:
            self.show_popup("Error", "Please enter the video URL.")
            return

        save_path = os.path.expanduser("~")  # مجلد المستخدم

        self.log(f"📥 Starting download: {url}")

        def progress_hook(d):
            if stop_download:
                raise yt_dlp.utils.DownloadCancelled("Cancelled")

            if d['status'] == 'downloading':
                percent = d.get('_percent_str', '0%').strip()
                self.log(f"Downloading... {percent}")
            elif d['status'] == 'finished':
                self.log("✅ Download complete!")

        def run():
            if quality == "Audio Only (MP3)":
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_hook],
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                }
            elif quality == "Lowest Video Quality":
                ydl_opts = {
                    'format': 'worstvideo+bestaudio',
                    'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_hook],
                    'quiet': True
                }
            else:
                ydl_opts = {
                    'format': 'bestvideo+bestaudio',
                    'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_hook],
                    'quiet': True
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                    self.show_popup("Done", "✅ Download completed.")
                except Exception as e:
                    self.log(f"❌ Error: {e}")
                    self.show_popup("Error", str(e))

        threading.Thread(target=run).start()

    def show_about(self, instance=None):
        popup = Popup(title="About Developer", content=Label(text=developer_info),
                      size_hint=(None, None), size=(400, 250))
        popup.open()

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


class DownloaderApp(App):
    def build(self):
        self.title = "JaFlex Downloader (Kivy Version)"
        return Downloader()

if __name__ == '__main__':
    DownloaderApp().run()
