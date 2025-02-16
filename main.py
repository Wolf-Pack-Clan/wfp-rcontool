################ Imports ##################
from kivy.config import Config

Config.set('graphics', 'dpi', 'auto')
Config.set('graphics', 'maxfps', '60')
Config.set('graphics', 'fbo', 'force-hardware')


from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.transition import MDFadeSlideTransition

from kivy.clock import Clock
from kivy.core.window import Window

from kivy.utils import hex_colormap
from kivy import platform
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText

from settings import SettingsScreen, AppearanceSettings, AboutScreen
from servers import ServerScreen

from os import path

if platform == "android":
    #from android.permissions import request_permissions, Permission # type: ignore
    from kivymd.toast import toast

from time import sleep
import threading
import json
from typing import Optional

from util import rcon_command, monotone, saveServers, valid_colors
from util import svListPath, configPath, logFile
import util
###########################################

if not path.isfile(svListPath):
    open(svListPath, 'w').close()

if not path.isfile(configPath):
    open(configPath, 'w').close()

if not path.isfile(logFile):
    open(logFile, 'w').close()

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
        ip = util.currentIP
        port = util.currentPort
        rpass = util.currentPass
        cmd = self.cmdInput.text
        
        print(ip, port, rpass)
        app = MDApp.get_running_app()
        
        self.cmdInput.focus = False
        Clock.schedule_once(lambda arg: app.settext(self.cmdInput, ""))
        
        threading.Thread(target=self.returnFocus).start()
        print(cmd)
        if cmd == "clear":
            Clock.schedule_once(lambda arg: app.settext(self.console, ""))
            return
        result = rcon_command(server_ip=ip, server_port=port, rcon_password=rpass, command=cmd)
        print(result)
        Clock.schedule_once(lambda arg: app.settext(self.console, f"{self.console.text}\n{result}"))
    
    def returnFocus(self):
        sleep(0.5)
        self.cmdInput.focused = True
    
    def clear_selection(self, instance, touch):
        if self.console.collide_point(*touch.pos):
            self.console.cancel_selection()

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
        util.savedServers[name] = {
            "ip": ip_port,
            "rcon_pass": rcon_pass
        }
        print(util.savedServers)
        saveServers(svListPath, util.savedServers)
        global sm
        sm.current = "servers"

class RCONApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.loadAppSettings()
        
        self.title = "RCON Tool"
        
        # Populating color sets
        #global colorSet1, colorSet2, colorSet3, colorSet4
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
        
        global sm
        sm = MDScreenManager()
        sm.transition = MDFadeSlideTransition()
        sm.add_widget(MainScreen(name="main"))
        
        # Settings
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(AppearanceSettings(name="appearance", colorSets=[colorSet1, colorSet2, colorSet3, colorSet4]))
        sm.add_widget(AboutScreen(name="about"))
        # Servers
        sm.add_widget(ServerScreen(name="servers"))
        sm.add_widget(AddServerScreen(name="addserver"))
        
        sm.current = "main"
        
        Clock.schedule_once(lambda x: Window.bind(on_keyboard=self.onKeyboard))
        
        return sm
    
    def on_start(self):
        #self.fps_monitor_start()
        
        #print(len(colorSet2), len(colorSet1), len(colorSet3), len(colorSet4))
        if not self.whatsold:
            changelog = """
            Basic RCON functionality. See demo video in the github readme.
            Error Handling system.
            A ''Purge Logs'' option in settings.
            This popup only shows once now :D
            (Not tested on android yet.)
            """
            self.show_alert_dialog(icon="information", headline="What's new?", text=changelog)
            self.whatsold = True
        
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
        from settings import colormenu
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
                self.whatsold = appConfig["whatsold"]
            except json.JSONDecodeError:
                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "Yellowgreen"
                self.textFieldStyle = "filled"
                self.whatsold = False
                Clock.schedule_once(lambda arg: self.saveAppSettings())
            except Exception as e:
                self.errorHandler(e)
    
    def saveAppSettings(self, *args):
        print("I HAVE BEEN SUMMONED")
        appConfig = {}
        appConfig["themeStyle"] = self.theme_cls.theme_style
        appConfig["themeColor"] = self.theme_cls.primary_palette
        appConfig["textFieldStyle"] = self.textFieldStyle
        appConfig["whatsold"] = self.whatsold
        
        with open(configPath, 'w') as configFile:
            json.dump(appConfig, configFile, indent=4)
    
    def errorHandler(self, errorStr:str):
        userText = "An unexpected error occured. Check the logs and notify developer."
        if platform == "android":
            toast(userText, 4, 80)
        else:
            self.show_alert_dialog(icon="skull", headline="ERROR!", text=userText)
        with open(logFile, 'a') as f:
            f.write(errorStr + "\n")
            f.close()
            

if __name__ == "__main__":
    RCONApp().run()