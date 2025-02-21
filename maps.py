#from kivy.uix.accordion import StringProperty
from kivy.uix.actionbar import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivy.clock import Clock
import urllib.request
from os import path
import threading

import util

stockMaps = ["mp_arnhem", "mp_berlin", "mp_bocage", "mp_brecourt", "mp_carentan", "mp_cassino",
             "mp_dawnville", "mp_chateau", "mp_depot", "mp_foy", "mp_harbor", "mp_hurtgen",
             "mp_italy", "mp_kharkov", "mp_kursk", "mp_pavlov", "mp_neuville", "mp_peaks",
             "mp_ponyri", "mp_powcamp", "mp_railyard", "mp_rhinevalley", "mp_rocket", "mp_ship",
             "mp_sicily", "mp_stalingrad", "mp_streets", "mp_tigertown", "mp_uo_harbor", "mp_uo_stanjel"]

class MapScreen(MDScreen):
    def on_enter(self):
        print("Maps Screen")
    
    def on_pre_enter(self):
        Clock.schedule_once(self.genMapCards)
    
    def genMapCards(self, instance):
        Clock.schedule_once(self.execDLTask)
        self.ids.map_list.data = []
        for map in util.svMaps:
            self.ids.map_list.data.extend(
                [{
                    "text": map,
                    "image_url": "https://cod.pm/mp_maps/cod1+coduo/custom/zh_king.png",
                }]
            )
    
    def execDLTask(self, instance):
        threading.Thread(target=lambda x="": self.downloadMapImages()).start()
    
    def downloadMapImages(self):
        for map in util.svMaps:
            try:
                if map in stockMaps:
                    url = f"https://cod.pm/mp_maps/cod1+coduo/stock/{map}.png"
                else:
                    url = f"https://cod.pm/mp_maps/cod1+coduo/custom/{map}.png"
                
                urllib.request.urlretrieve(url, path.join(util.imagesPath, f"{map}.png"))
            except Exception as e:
                print(e)
                print(url)

class MapCard(BoxLayout):
    text = StringProperty()
    image_url = StringProperty()