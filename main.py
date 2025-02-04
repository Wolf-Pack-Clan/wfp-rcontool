from kivy.uix.behaviors import ButtonBehavior
################ Imports ##################
from kivy.config import Config

Config.set('graphics', 'dpi', 'auto')
Config.set('graphics', 'maxfps', '60')
Config.set('graphics', 'fbo', 'force-hardware')


from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.transition import MDFadeSlideTransition

from kivymd.uix.menu import MDDropdownMenu

from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.core.window import Window

from kivy.utils import hex_colormap

from os import path
from time import sleep
import threading
###########################################

currentdir = path.dirname(path.realpath(__file__))

myFont = path.join(currentdir, "font/playwritedegrund.ttf")
dejavu = path.join(currentdir, "font/dejavusans.ttf")

global valid_colors
valid_colors = ['Aliceblue', 'Antiquewhite', 'Aqua', 'Aquamarine', 'Azure',
                'Beige', 'Bisque', 'Black', 'Blanchedalmond', 'Blue', 'Blueviolet',
                'Brown', 'Burlywood', 'Cadetblue', 'Chartreuse', 'Chocolate', 'Coral',
                'Cornflowerblue', 'Cornsilk', 'Crimson', 'Cyan', 'Darkblue', 'Darkcyan',
                'Darkgoldenrod', 'Darkgray', 'Darkgrey', 'Darkgreen', 'Darkkhaki', 'Darkmagenta',
                'Darkolivegreen', 'Darkorange', 'Darkorchid', 'Darkred', 'Darksalmon', 'Darkseagreen',
                'Darkslateblue', 'Darkslategray', 'Darkslategrey', 'Darkturquoise', 'Darkviolet',
                'Deeppink', 'Deepskyblue', 'Dimgray', 'Dimgrey', 'Dodgerblue', 'Firebrick',
                'Floralwhite', 'Forestgreen', 'Fuchsia', 'Gainsboro', 'Ghostwhite', 'Gold',
                'Goldenrod', 'Gray', 'Grey', 'Green', 'Greenyellow', 'Honeydew', 'Hotpink',
                'Indianred', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'Lavenderblush', 'Lawngreen',
                'Lemonchiffon', 'Lightblue', 'Lightcoral', 'Lightcyan', 'Lightgoldenrodyellow',
                'Lightgreen', 'Lightgray', 'Lightgrey', 'Lightpink', 'Lightsalmon', 'Lightseagreen',
                'Lightskyblue', 'Lightslategray', 'Lightslategrey', 'Lightsteelblue', 'Lightyellow',
                'Lime', 'Limegreen', 'Linen', 'Magenta', 'Maroon', 'Mediumaquamarine', 'Mediumblue',
                'Mediumorchid', 'Mediumpurple', 'Mediumseagreen', 'Mediumslateblue', 'Mediumspringgreen',
                'Mediumturquoise', 'Mediumvioletred', 'Midnightblue', 'Mintcream', 'Mistyrose',
                'Moccasin', 'Navajowhite', 'Navy', 'Oldlace', 'Olive', 'Olivedrab', 'Orange',
                'Orangered', 'Orchid', 'Palegoldenrod', 'Palegreen', 'Paleturquoise', 'Palevioletred',
                'Papayawhip', 'Peachpuff', 'Peru', 'Pink', 'Plum', 'Powderblue', 'Purple', 'Red',
                'Rosybrown', 'Royalblue', 'Saddlebrown', 'Salmon', 'Sandybrown', 'Seagreen',
                'Seashell', 'Sienna', 'Silver', 'Skyblue', 'Slateblue', 'Slategray', 'Slategrey',
                'Snow', 'Springgreen', 'Steelblue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise',
                'Violet', 'Wheat', 'White', 'Whitesmoke', 'Yellow', 'Yellowgreen']
print(len(valid_colors))
global currentColorIndex
currentColorIndex = 147

########################################################

class MainScreen(MDScreen):
    def on_enter(self, *args):
        print("hey")
        self.console = self.ids.console
        self.cmdInput = self.ids.commandInput
        
        self.console.bind(on_touch_down=self.clear_selection)
        
        app = MDApp.get_running_app()
        app.console = self.console
    
    def callback_exec(self):
        print(self.cmdInput.focused)#
        threading.Thread(target=self.process_cmd).start()
    
    def process_cmd(self):
        app = MDApp.get_running_app()
        self.cmdInput.focus = True
        Clock.schedule_once(lambda dt: app.settext(self.cmdInput, ""))
        threading.Thread(target=self.returnFocus).start()
        if self.cmdInput.text == "clear":
            Clock.schedule_once(lambda dt: app.settext(self.console, ""))
    
    def returnFocus(self):
        sleep(0.5)
        self.cmdInput.focused = True
    
    def clear_selection(self, instance, touch):
        if self.console.collide_point(*touch.pos):
            self.console.cancel_selection()

class SettingsScreen(MDScreen):
    def on_enter(self, *args):
        print("Settings Screen")

class AppearanceSettings(MDScreen):
    def on_enter(self, *args):
        print("Appearance Settings")
    
    def colorMenu(self, set, *args):
        global colorSet1, colorSet2
        if set == 1:
            menu_items = colorSet1
        else:
            menu_items = colorSet2
        MDDropdownMenu(caller=(self.ids.colorMenuButton1 if set == 1 else self.ids.colorMenuButton2), items=menu_items).open()

class RCONApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellowgreen"
        self.theme_cls.secondary_palette = "Purple"
        self.theme_cls.theme_style_switch_animation = True
        
        print(hex_colormap)
        
        self.title = "RCON Tool"
        
        global sm
        sm = MDScreenManager()
        sm.transition = MDFadeSlideTransition()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(AppearanceSettings(name="appearance"))
        sm.current = "main"
        
        Clock.schedule_once(lambda x: Window.bind(on_keyboard=self.onKeyboard))
        
        return sm
    
    def on_start(self):
        #self.fps_monitor_start()
        global colorSet1, colorSet2
        global valid_colors
        colorSet1 = []; colorSet2 = []
        for _color in valid_colors[:74]:
            _colorChoice = {
                "text": _color,
                "text_color": hex_colormap[_color.lower()],
                "on_release": lambda color=_color: self.changePrimaryColor(color=color),
            }
            colorSet1.append(_colorChoice)
        
        for _color in valid_colors[74:]:
            _colorChoice = {
                "text": _color,
                "text_color": hex_colormap[_color.lower()],
                "on_release": lambda color=_color: self.changePrimaryColor(color=color),
            }
            colorSet2.append(_colorChoice)
        
        return super().on_start()
    
    def settext(self, element, text):
        if isinstance(text, str):
            element.text = text
    
    def toggleDarkMode(self):
        #app = MDApp.get_running_app()
        self.theme_cls.theme_style = ("Dark" if self.theme_cls.theme_style == "Light" else "Light")
        if self.theme_cls.theme_style == "Dark":
            self.console.foreground_color = (1,1,1,1)
        else:
            self.console.foreground_color = (0,0,0,1)
    
    def changePrimaryColor(self, color, *args):
        print(color)
        self.theme_cls.primary_palette = color
    
    def onKeyboard(self, window, key, *args):
        if key==27:
            global sm
            sm.current = sm.previous()

if __name__ == "__main__":
    LabelBase.register(name="myfont", fn_regular=myFont)
    LabelBase.register(name="dejavu", fn_regular=dejavu)
    RCONApp().run()