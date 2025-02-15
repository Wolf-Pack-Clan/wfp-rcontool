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
from kivymd.uix.list import MDListItem, MDListItemSupportingText
from kivymd.uix.button import MDIconButton, MDButton

from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivy.utils import hex_colormap
from kivy import platform
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer

from os import path

if platform == "android":
    #from android.permissions import request_permissions, Permission # type: ignore
    from kivymd.toast import toast
    from android import mActivity # type: ignore
    context = mActivity.getApplicationContext()
    result =  context.getExternalFilesDir(None)
    if result:
        #toast(str(result.toString()), 10, 80)
        test = path.join(str(result.toString()), "test")
        toast(test)
        open(test, 'w').close()

from time import sleep
import threading
import json
from typing import Optional

from util import rcon_command, monotone, loadSavedServers, saveServers, valid_colors
###########################################

currentdir = path.dirname(path.realpath(__file__))
svListPath = path.join(currentdir, "saved_servers.json")
configPath = path.join(currentdir, "settings.json")

if not path.isfile(svListPath):
    open(svListPath, 'w').close()

if not path.isfile(configPath):
    open(configPath, 'w').close()

savedServers = loadSavedServers(svListPath)
loadedServers = []
loadedSVwidgets = []

global server_ip
global server_port
global rcon_password
server_ip = "1.1.1.1"
server_port = 28960
rcon_password = "12345"

global currentColorIndex
currentColorIndex = 147

########################################################

class MainScreen(MDScreen):
    def on_enter(self, *args):
        print("Main Screen")
        self.console = self.ids.console
        self.cmdInput = self.ids.commandInput
        
        self.console.bind(on_touch_down=self.clear_selection)
        
        app = MDApp.get_running_app()
        app.console = self.console
        if app.theme_cls.theme_style == "Dark":
            self.console.foreground_color = (1,1,1,1)
        else:
            self.console.foreground_color = (0,0,0,1)
    
    def callback_exec(self):
        #print(self.cmdInput.focused)#
        threading.Thread(target=self.process_cmd).start()
    
    def process_cmd(self):
        app = MDApp.get_running_app()
        self.cmdInput.focus = True
        Clock.schedule_once(lambda arg: app.settext(self.cmdInput, ""))
        threading.Thread(target=self.returnFocus).start()
        if self.cmdInput.text == "clear":
            Clock.schedule_once(lambda arg: app.settext(self.console, ""))
    
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
        global colorSet1, colorSet2, colorSet3, colorSet4
        if set == 1:
            menu_items = colorSet1
            _caller = self.ids.colorMenuButton1
        elif set == 2:
            menu_items = colorSet2
            _caller = self.ids.colorMenuButton2
        elif set == 3:
            menu_items = colorSet3
            _caller = self.ids.colorMenuButton3
        else:
            menu_items = colorSet4
            _caller = self.ids.colorMenuButton4
        
        global colormenu
        colormenu = MDDropdownMenu(caller=_caller, items=menu_items)
        colormenu.open()
    
    def tFieldStyleMenu(self, *args):
        choices = []
        filledChoice = {
            "text": "Filled",
            "on_release": lambda style="filled": self.changeFieldStyle(style)
        }
        choices.append(filledChoice)
        outlinedChoice = {
            "text": "Outlined",
            "on_release": lambda style="outlined": self.changeFieldStyle(style)
        }
        choices.append(outlinedChoice)
        _caller = self.ids.fStyleMenuButton
        
        global tfstylemenu
        tfstylemenu = MDDropdownMenu(caller=_caller, items=choices)
        tfstylemenu.open()
    
    def changeFieldStyle(self, style, *args):
        print(style)
        app = MDApp.get_running_app()
        app.textFieldStyle = ("filled" if style == "filled" else "outlined")
        global tfstylemenu
        tfstylemenu.dismiss()
        app.saveAppSettings()
    
    def resetTheme(self, *args):
        print("reset")
        app = MDApp.get_running_app()
        app.theme_cls.theme_style = "Dark"
        app.theme_cls.primary_palette = "Yellowgreen"
        app.textFieldStyle = "filled"
    
    def themepreview(self):
        app:RCONApp = MDApp.get_running_app()
        app.show_alert_dialog(icon="information", headline="Not Implemented...yet.")

class ServerScreen(MDScreen):
    def on_enter(self, *args):
        print("Servers Screen")
        
        savedServers = loadSavedServers(svListPath)
        if isinstance(savedServers, dict):
            for server in savedServers:
                if server in loadedServers:
                    print("Server already loaded:", server)
                    continue
                sv_btn = MDListItem()
                sv_text = MDListItemSupportingText()
                sv_text.text = server
                sv_btn.add_widget(sv_text)
                sv_del = MDIconButton()
                sv_del.icon = "delete"
                sv_del.on_release = lambda x=server, y=sv_btn: self.delServer(x,y)
                sv_btn.on_release = lambda z="hello": print(z)
                sv_btn.add_widget(sv_del)
                self.ids.serverList.add_widget(sv_btn)
                loadedServers.append(server)
                loadedSVwidgets.append(sv_btn)
    
    def delServer(self, name, widget, *args):
        savedServers.pop(name)
        saveServers(svListPath, savedServers)
        for _widget in loadedSVwidgets:
            if widget == _widget:
                self.ids.serverList.remove_widget(widget)
                return

class AddServerScreen(MDScreen):
    def on_enter(self, *args):
        print("Add Server Screen")
    
    """def on_pre_leave(self, *args):
        app = MDApp.get_running_app()
        #Clock.schedule_once(lambda arg: app.saveAppSettings())
        print("leaving")
        app.saveAppSettings()"""
    
    def saveNewServer(self, *args):
        name = str(self.ids.newSrvName.text)
        ip_port = str(self.ids.newSrvIP.text)
        rcon_pass = str(self.ids.newSrvPass.text)
        savedServers[name] = {
            "ip": ip_port,
            "rcon_pass": rcon_pass
        }
        print(savedServers)
        saveServers(svListPath, savedServers)
        global sm
        sm.current = "servers"

class AboutScreen(MDScreen):
    def on_enter(self, *args):
        print("About Screen")
        self.ids.WolfPackLogo.source = path.join(currentdir, "icons/wolfpack.png")
        self.ids.GHLogo.source = path.join(currentdir, "icons/github-mark.png")
        self.ids.kivyMDLogo.source = path.join(currentdir, "icons/kivymd_logo_blue.png")

class RCONApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.loadAppSettings()
        
        self.title = "RCON Tool"
        
        global sm
        sm = MDScreenManager()
        sm.transition = MDFadeSlideTransition()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(AppearanceSettings(name="appearance"))
        sm.add_widget(ServerScreen(name="servers"))
        sm.add_widget(AddServerScreen(name="addserver"))
        sm.add_widget(AboutScreen(name="about"))
        sm.current = "main"
        
        Clock.schedule_once(lambda x: Window.bind(on_keyboard=self.onKeyboard))
        
        return sm
    
    def on_start(self):
        #self.fps_monitor_start()
        global colorSet1, colorSet2, colorSet3, colorSet4
        global valid_colors
        colorSet1 = []; colorSet2 = []; colorSet3 = []; colorSet4 = []
        for _color in valid_colors[:37]:
            _colorChoice = {
                "text": _color,
                "text_color": hex_colormap[_color.lower()],
                "on_release": lambda color=_color: self.changePrimaryColor(color=color),
            }
            colorSet1.append(_colorChoice)
        
        for _color in valid_colors[37:74]:
            _colorChoice = {
                "text": _color,
                "text_color": hex_colormap[_color.lower()],
                "on_release": lambda color=_color: self.changePrimaryColor(color=color),
            }
            colorSet2.append(_colorChoice)
        
        for _color in valid_colors[74:111]:
            _colorChoice = {
                "text": _color,
                "text_color": hex_colormap[_color.lower()],
                "on_release": lambda color=_color: self.changePrimaryColor(color=color),
            }
            colorSet3.append(_colorChoice)
        
        for _color in valid_colors[111:]:
            _colorChoice = {
                "text": _color,
                "text_color": hex_colormap[_color.lower()],
                "on_release": lambda color=_color: self.changePrimaryColor(color=color),
            }
            colorSet4.append(_colorChoice)
        
        #print(len(colorSet2), len(colorSet1), len(colorSet3), len(colorSet4))
        self.show_alert_dialog(icon="information", headline="What's new?", text="You can create and delete servers.\nMenus in settings close after selecting an option.\nThis very popup :D")
        
        return super().on_start()
    
    #def show_alert_dialog(self, icon:str, headline:str, text:str):
    def show_alert_dialog(self, icon: Optional[str] = None, headline: Optional[str] = None, text: Optional[str] = None):
        """
        Shows an info dialog with no buttons.
        """
        mydialog = MDDialog()
        if icon:
            mydialog.add_widget(MDDialogIcon(icon=icon))
        if headline:
            mydialog.add_widget(MDDialogHeadlineText(text=headline))
        if text:
            mydialog.add_widget(MDDialogSupportingText(text=text))
        
        mydialog.open()
    
    def on_stop(self):
        print("bye")
        #Clock.schedule_once(lambda arg: self.saveAppSettings())
        self.saveAppSettings()
    
    def on_pause(self):
        Clock.schedule_once(lambda arg: self.saveAppSettings())
    
    def onKeyboard(self, window, key, *args):
        if key==27:
            global sm
            sm.current = sm.previous()
    
    def settext(self, element, text):
        if isinstance(text, str):
            element.text = text
    
    def toggleDarkMode(self):
        self.theme_cls.theme_style = ("Dark" if self.theme_cls.theme_style == "Light" else "Light")
        if self.theme_cls.theme_style == "Dark":
            self.console.foreground_color = (1,1,1,1)
        else:
            self.console.foreground_color = (0,0,0,1)
        self.saveAppSettings()
    
    def changePrimaryColor(self, color, *args):
        print(color)
        self.theme_cls.primary_palette = color
        global colormenu
        colormenu.dismiss()
        #sm.get_screen("appearance").ids.colorMenuButton1
        self.saveAppSettings()
    
    def loadAppSettings(self, *args):
        with open(configPath, 'r') as configFile:
            try:
                appConfig = json.load(configFile)
                self.theme_cls.theme_style = appConfig["themeStyle"]
                self.theme_cls.primary_palette = appConfig["themeColor"]
                self.textFieldStyle = appConfig["textFieldStyle"]
            except json.JSONDecodeError:
                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "Yellowgreen"
                self.textFieldStyle = "filled"
                Clock.schedule_once(lambda arg: self.saveAppSettings())
            except Exception as e:
                self.errorHandler(e)
    
    def saveAppSettings(self, *args):
        print("I HAVE BEEN SUMMONED")
        appConfig = {}
        appConfig["themeStyle"] = self.theme_cls.theme_style
        appConfig["themeColor"] = self.theme_cls.primary_palette
        appConfig["textFieldStyle"] = self.textFieldStyle
        
        with open(configPath, 'w') as configFile:
            json.dump(appConfig, configFile, indent=4)
    
    def errorHandler(self, errorStr:str, *args):
        if platform == "android":
            toast("An unexpected error occured. Check the logs.", 4, 80)

if __name__ == "__main__":
    RCONApp().run()