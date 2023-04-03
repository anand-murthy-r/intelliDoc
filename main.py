import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager,Screen, FadeTransition, SlideTransition
import win32gui
import tkinter
from tkinter import filedialog
from PIL import Image as Img


#initialize kivy version
kivy.require('2.1.0')



class MyButton(Button):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.font_name = 'AGENCYR'
        self.font_size = 20
        self.size_hint_y = None
        self.height = 50
        self.size_hint_x = None
        self.width = 200
        self.background_color[3] = 0.5


class SelectFilePopup:
    def __init__(self,title,initialdir):
        self.title = title
        self.filename = None
        self.title = title
        self.initialdir = initialdir

    def open(self):
        self.filename = filedialog.askopenfilename(
            initialdir=self.initialdir,
            title=self.title,
            filetypes=(("PNG Files","*.png"),("JPG Files","*.jpg"))
        )

    def getDir(self):
        return self.filename

class Interface(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        with self.canvas.before:
            # Load the image and use it as the texture of the Rectangle
            self.bg = Image(source='background.jpg').texture
            # Set the size and position of the Rectangle to cover the entire GridLayout
            self.rect = Rectangle(texture=self.bg, pos=self.pos, size=self.size)
            # Bind the size and position of the Rectangle to the size and position of the GridLayout
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class LoginPage(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.LoginLayout = GridLayout(cols=2) # Layout for the Login page
        self.mainLayout = BoxLayout() # Layout for the main stuff
        self.Layout2 = AnchorLayout()
        self.Layout3 = GridLayout(
            size_hint_y=None,
            height=120,
            size_hint_x=None,
            width=300
        )
        self.cols = 2
        self.Layout2.orientation = 'vertical'
        self.Layout2.cols = 3
        self.Layout3.cols = 2
        self.Layout3.add_widget(Label(
            text="Enter Username ",
            font_size=30,
            font_name='AGENCYR'
        )
        )
        self.usernameInp = TextInput(multiline=False)
        self.Layout3.add_widget(self.usernameInp)
        self.Layout3.add_widget(Label(
            text="Enter Password ",
            font_size=30,
            font_name='AGENCYR'
        )
        )
        self.passwordInp = TextInput(multiline=False, password=True)
        self.Layout3.add_widget(self.passwordInp)
        self.loginButton = Button(
            text='LOGIN',
            size_hint_y=None,
            height=50,
            size_hint_x=None,
            width=200,
            background_color=(0, 1, 0, 0.5)
        )
        self.skipButton = Button(
            text='SKIP LOGIN',
            size_hint_y=None,
            height=50,
            size_hint_x=None,
            width=200,
            background_color=(1,1,1,0.5)
        )
        self.loginButton.bind(on_release=self.switch_layout)
        self.skipButton.bind(on_release=self.switch_layout)
        self.Layout3.add_widget(self.loginButton)
        self.Layout3.add_widget(self.skipButton)
        self.Layout2.add_widget(self.Layout3)
        self.LoginLayout.add_widget(self.Layout2)
        self.LoginLayout.add_widget(
            Label(
                text="intelliDoc",
                font_size=50,
                font_name='BAUHS93'
            )
        )
        self.add_widget(self.LoginLayout)

    def switch_layout(self,*args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'main'

class MainScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.CenterLayout = FloatLayout()
        self.MainLayout = BoxLayout(orientation='vertical', spacing=10)
        StartButton = MyButton(
            text='START SCANNING',
            background_color=(0, 1, 0, 0.5)
        )
        SettingButton = MyButton(
            text='Settings',
            background_color=(1,1,1,0.5)
        )
        ReturnButton = MyButton(
            text='Log out',
            background_color=(1, 0, 0, 0.5)
        )
        StartButton.bind(on_release=self.switch_to_ScanScreen)
        ReturnButton.bind(on_release=self.switch_to_LoginScreen)
        SettingButton.bind(on_release=self.switch_to_SettingScreen)
        self.MainLayout.add_widget(StartButton)
        self.MainLayout.add_widget(SettingButton)
        self.MainLayout.add_widget(ReturnButton)
        self.CenterLayout.add_widget(self.MainLayout)
        #self.MainLayout.pos_hint = {'center_x':0.5,'center_y':0.5}
        self.add_widget(self.CenterLayout)

    def switch_to_LoginScreen(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'

    def switch_to_SettingScreen(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'setting'

    def switch_to_ScanScreen(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'scan'


class SettingScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='COMING SOON'))
        self.BackButton = MyButton(
            text = 'BACK'
        )
        self.BackButton.bind(on_release=self.switch_to_MainScreen)
        self.add_widget(self.BackButton)

    def switch_to_MainScreen(self,*args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main'


class ScanScreen(Screen):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        popup = Popup(
            title='Error',
            content=None,
            size_hint=(0.5, 0.5),
            auto_dismiss=False
        )
        self.ScanLayout = FloatLayout()
        self.BrowseButton = MyButton(
            text='BROWSE IMAGE',
            background_color=(1,1,0,0.5),
            pos_hint={'center_x': 0.5,'center_y': 0.5}
        )
        self.BackButton = MyButton(
            text='BACK'
        )
        self.BackButton.bind(on_release=self.switch_to_MainScreen)
        self.BrowseButton.bind(on_release=self.Work)
        self.add_widget(self.BrowseButton)
        self.add_widget(self.BackButton)
        self.add_widget(self.ScanLayout)


    def switch_to_MainScreen(self,*args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main'

    def Work(self,*args):
        filename = self.openPopup()
        try:
            img = Img.open(filename)
            img.show()
        except AttributeError:
            pass

    def openPopup(self,*args):
        popup = SelectFilePopup("Select Image","/")
        popup.open()
        return popup.getDir()




class MyApp(App):
    def build(self):
        ParentLayout = Interface()
        screen_manager = ScreenManager()
        loginScreen = LoginPage(name='login')
        mainScreen = MainScreen(name='main')
        mainSettingScreen = SettingScreen(name='setting')
        scanScreen = ScanScreen(name='scan')
        screen_manager.add_widget(loginScreen)
        screen_manager.add_widget(mainScreen)
        screen_manager.add_widget(mainSettingScreen)
        screen_manager.add_widget(scanScreen)
        ParentLayout.add_widget(screen_manager)
        return ParentLayout


# starting app
app = MyApp()

if __name__ == '__main__':
    app.run()