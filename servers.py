from kivy.uix.accordion import StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemSupportingText
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp

from util import savedServers, saveServers, loadSavedServers, svListPath
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
        
        savedServers = loadSavedServers(svListPath)
        if isinstance(savedServers, dict):
            for server in savedServers:
                if server in loadedServers:
                    print("Server already loaded:", server)
                    continue
                sv_btn = ServerListSVButton()
                
                sv_text = MDListItemSupportingText()
                sv_text.text = server
                sv_btn.add_widget(sv_text)
                
                sv_del = MDIconButton()
                sv_del.icon = "delete"
                sv_del.on_release = lambda x=server, y=sv_btn: self.delServer(x,y)
                sv_btn.add_widget(sv_del)
                
                sv_btn.svIP = savedServers[server].get("ip")
                sv_btn.svRPass = savedServers[server].get("rcon_pass")
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
        except Exception as e:
            print(e)
            app = MDApp.get_running_app()
            app.errorHandler(e)
    
    def delServer(self, name, widget):
        savedServers.pop(name)
        saveServers(svListPath, savedServers)
        for _widget in loadedSVwidgets:
            if widget == _widget:
                self.ids.serverList.remove_widget(widget)
                break
        for server in loadedServers:
            if name == server:
                loadedServers.remove(name)