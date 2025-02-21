from kivy.uix.accordion import StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemSupportingText, MDListItemLeadingIcon
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp

from util import saveServers, loadSavedServers, svListPath
import util

loadedServers = []
loadedSVwidgets = []

class ServerListSVButton(MDListItem):
    svIP = StringProperty("1.1.1.1:28960")
    svRPass = StringProperty("password")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ServerScreen(MDScreen):
    def on_enter(self, *args):
        print("Servers Screen")
        
        util.savedServers = loadSavedServers(svListPath)
        if isinstance(util.savedServers, dict):
            for server in util.savedServers:
                if server in loadedServers:
                    print("Server already loaded:", server)
                    continue
                sv_btn = ServerListSVButton()
                
                sv_text = MDListItemSupportingText()
                sv_text.text = server
                sv_btn.add_widget(sv_text)
                sv_btn_icon = MDListItemLeadingIcon()
                sv_btn_icon.icon = "server-outline"
                sv_btn.add_widget(sv_btn_icon)
                
                sv_del = MDIconButton()
                sv_del.icon = "delete"
                sv_del.on_release = lambda x=server, y=sv_btn: self.delServer(x,y)
                sv_btn.add_widget(sv_del)
                
                sv_btn.svIP = util.savedServers[server].get("ip")
                sv_btn.svRPass = util.savedServers[server].get("rcon_pass")
                sv_btn.on_release = lambda z=sv_btn: self.activateServer(z)
                
                self.ids.serverList.add_widget(sv_btn)
                loadedServers.append(server)
                loadedSVwidgets.append(sv_btn)
    
    def activateServer(self, svWidget:ServerListSVButton):
        ip_port = svWidget.svIP
        password = svWidget.svRPass
        print(ip_port, password)
        print("activateServer")
        try:
            tmp = ip_port.split(":")
            util.currentIP = tmp[0].strip()
            util.currentPort = int(tmp[1].strip())
            util.currentPass = password
            print(util.currentIP, util.currentPort, util.currentPass)
            self.manager.current = "main"
        except Exception as e:
            print(e)
            app = MDApp.get_running_app()
            app.errorHandler(e, "activateServer")
    
    def delServer(self, name, widget):
        util.savedServers.pop(name)
        saveServers(svListPath, util.savedServers)
        for _widget in loadedSVwidgets:
            if widget == _widget:
                self.ids.serverList.remove_widget(widget)
                break
        for server in loadedServers:
            if name == server:
                loadedServers.remove(name)

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
        self.manager.current = "servers"