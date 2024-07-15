import kivy
from kivymd.toast import toast
import dmcheck as dm
import pandas as pd
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
kivy.require('1.9.0')


def InvalidFile():
    content = Button(text='Invalid Input File')
    popup = Popup(title="ERROR", content=content, auto_dismiss=False,
                  size_hint=(None, None), size=(300, 200))
    popup.open()

    content.bind(on_press=popup.dismiss)


def auth_error():
    content = Button(text='Close')
    popup = Popup(title="Authentication Failed", content=content, auto_dismiss=False,
                  size_hint=(None, None), size=(300, 200))
    popup.open()

    content.bind(on_press=popup.dismiss)


def show_popup():
    content = Button(text='Close')
    popup = Popup(title="Download Completed", content=content, auto_dismiss=False,
                  size_hint=(None, None), size=(300, 200))
    popup.open()

    content.bind(on_press=popup.dismiss)


def error_popup():
    content = Button(text='Error Reading File')
    popup = Popup(title="Re Try", content=content, auto_dismiss=False,
                  size_hint=(None, None), size=(300, 200))
    popup.open()

    content.bind(on_press=popup.dismiss)


def empty_input():
    content = Button(text='Input Fields Are Empty')
    popup = Popup(title="Missing Input", content=content,
                  auto_dismiss=False,
                  size_hint=(None, None), size=(300, 200))
    popup.open()

    content.bind(on_press=popup.dismiss)


def cred_error():
    content = Button(text='Please Set Your Twitter Credentials')
    popup = Popup(title="Missing Credentials", content=content,
                  auto_dismiss=False,
                  size_hint=(None, None), size=(300, 200))
    popup.open()

    content.bind(on_press=popup.dismiss)


def saved():
    content = Button(text='Your Twitter Credentials Saved')
    popup = Popup(title="Credentials Saved", content=content,
                  auto_dismiss=False,
                  size_hint=(None, None), size=(300, 200))
    popup.open()

    content.bind(on_press=popup.dismiss)


def download(filename):
    try:
        # toast(" Checking credentials...")
        pd.read_csv(filename)
        Config.read("myapp1.ini")
        ck = Config.get("DEFAULT", "consumer_key")
        cs = Config.get("DEFAULT", "consumer_secret")
        #print("consumer_key:\t{0}\nconsumer_secret:\t{1}".format(ck, cs))
        if ck == "" and cs == "":
            cred_error()
        else:
            # toast("Fetching Data ...")
            resp = dm.fetch(filename)
            if resp == "error":
                auth_error()
                MainWindow().reset()

            elif resp == "Done":
                #print(resp)
                MainWindow().reset()
                # self.download_complete()
                toast("Done")
    except:
        InvalidFile()
        MainWindow().reset()


class MainWindow(Screen):
    filename = ObjectProperty(None)

    def btn(self):
        # print("ok")
        # toast("Checking file...")
        # print("Filename :\t{0}".format(self.filename.text))
        download(self.filename.text)

    def reset(self):
        self.filename.text = ""


class SecondWindow(Screen):
    consumer_key = ObjectProperty(None)
    consumer_secret = ObjectProperty(None)

    def save_config(self):
        #print("Save conf")
        #print("consumer_key:\t{0}\nconsumer_secret:\t{1}".format(self.consumer_key.text, self.consumer_secret.text))
        Config.read("myapp1.ini")
        Config.set("DEFAULT", "consumer_key", self.consumer_key.text)
        Config.set("DEFAULT", "consumer_secret", self.consumer_secret.text)
        Config.write()
        saved()
        self.reset()

    def reset(self):
        self.consumer_key.text = ""
        self.consumer_secret.text = ""


class ThirdWindow(Screen):
    def selected(self, filepath):
        print("selected: %s" % filepath[0])
        download(filepath[0])


class WindowManager(ScreenManager):
    pass


KV = """

WindowManager:
    MainWindow:
    SecondWindow:
    ThirdWindow:

<MainWindow@BoxLayout>:
    name: 'main'
    filename: filename
    BoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: "TWITTER DM"
            halign: "center"
            valign: "center"


        BoxLayout:
            spacing: "40dp"
            padding: "250dp"
            orientation: 'vertical'
            BoxLayout:
                MDTextField:
                    id: filename
                    hint_text: "FILE PATH"
                    helper_text: "Input CSV File Path"
                    text_color: app.theme_cls.primary_light
                    helper_text_mode: "on_error"
                    required: True
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: "50dp"
                    increment_width: "300dp"
                MDFloatingActionButton:
                    icon: "clipboard-file"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    md_bg_color: app.theme_cls.primary_light
                    user_font_size: "40sp"
                    on_release: app.root.current = 'third'

            MDFlatButton:
                text: "DOWNLOAD"
                increment_width: "250dp"
                spacing: 50
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.btn()


        MDIconButton:
            icon: "key-plus"
            theme_text_color: "Custom"
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation_normal: 12
            on_release: app.root.current = 'second'

<SecondWindow>:
    name: 'second'
    consumer_key: consumer_key
    consumer_secret: consumer_secret

    BoxLayout:
        padding: 250
        spacing: "30dp"
        orientation: 'vertical'
        MDTextField:
            id: consumer_key
            hint_text: "Consumer Key"
            helper_text: "Twitter Consumer Key"
            helper_text_mode: "on_error"
            required: True
            text_color: app.theme_cls.primary_color
            pos_hint: {'center_y': .7}

        MDTextField:
            id: consumer_secret
            hint_text: "Consumer Secret"
            helper_text: "Twitter Consumer Secret"
            helper_text_mode: "on_error"
            required: True
            text_color: app.theme_cls.primary_color
            pos_hint: {'center_y': .5}
        GridLayout:
            cols:2
            padding: "50dp"
            spacing: 50
            MDRectangleFlatButton:
                text: "CLOSE"
                pos_hint: {'center_x': .5, 'center_y': .1}
                padding: dp(48)
                spacing: dp(15)
                text_color: app.theme_cls.primary_dark
                md_bg_color: 0,0,0,0
                on_release: app.root.current = 'main'


            MDRectangleFlatButton:
                text: "SAVE"
                pos_hint: {'center_x': .5, 'center_y': .1}
                padding: dp(48)
                spacing: dp(15)
                text_color: app.theme_cls.primary_dark
                md_bg_color: 0,0,0,0
                on_press: root.save_config()
                on_release: app.root.current = 'main'


<ThirdWindow@BoxLayout>:
    name: 'third'
    canvas:
        Color:
            rgba: app.theme_cls.primary_color
        Rectangle:
            pos: self.pos
            size: self.size

    FileChooserIconView:
        id: filechooser
        on_selection: root.selected(filechooser.selection)
    MDFloatingActionButton:
        icon: "check"
        pos_hint: {"center_x": .5, "center_y": .1}
        md_bg_color: app.theme_cls.primary_color
        on_release: app.root.current = 'main'


"""


class MyMainApp(MDApp):
    def build(self):
        self.icon = 'icon.png'
        self.theme_cls.primary_palette = "Cyan"
        return Builder.load_string(KV)


if __name__ == "__main__":
    MyMainApp().run()
