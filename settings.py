from kivy.uix.accordion import ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from os import path, listdir
from os import remove as rmfile

from util import currentdir

class SettingsScreen(MDScreen):
    def on_enter(self, *args):
        print("Settings Screen")
        
        self.ids.purgeText.text = f"Purge Logs ({len(listdir(path.join(currentdir, 'logs')))})"
    
    def purgeLogs(self):
        for filename in listdir(path.join(currentdir, "logs")):
            file_path = path.join(path.join(currentdir, "logs"), filename)
            try:
                if path.isfile(file_path) or path.islink(file_path):
                    print(filename)
                    rmfile(file_path)
            except Exception as e:
                print(e)
                app = MDApp.get_running_app()
                app.errorHandler(e)
        
        self.ids.purgeText.text = f"Purge Logs ({len(listdir(path.join(currentdir, 'logs')))})"

class AppearanceSettings(MDScreen):
    colorSets = ListProperty()
    """
    List of 4 color sets that make up the valid theme colors in kivymd.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        colorSets = kwargs.get("colorSets", None)
        
        self.colorSet1 = colorSets[0]
        self.colorSet2 = colorSets[1]
        self.colorSet3 = colorSets[2]
        self.colorSet4 = colorSets[3]
    
    def on_enter(self, *args):
        print("Appearance Settings")
    
    def colorMenu(self, set, *args):
        if set == 1:
            menu_items = self.colorSet1
            _caller = self.ids.colorMenuButton1
        elif set == 2:
            menu_items = self.colorSet2
            _caller = self.ids.colorMenuButton2
        elif set == 3:
            menu_items = self.colorSet3
            _caller = self.ids.colorMenuButton3
        else:
            menu_items = self.colorSet4
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
        app = MDApp.get_running_app()
        app.show_alert_dialog(icon="information", headline="Not Implemented...yet.")

class AboutScreen(MDScreen):
    def on_enter(self, *args):
        print("About Screen")
        self.ids.WolfPackLogo.source = path.join(currentdir, "icons/wolfpack.png")
        self.ids.GHLogo.source = path.join(currentdir, "icons/github-mark.png")
        self.ids.kivyMDLogo.source = path.join(currentdir, "icons/kivymd_logo_blue.png")
