# -*- coding: utf-8 -*-


from ComssServiceDevelopment.connectors.tcp.object_connector import OutputObjectConnector
from ComssServiceDevelopment.development import DevServiceController
import random
import json


import time


service_controller = DevServiceController("alarmService.json")
service_controller.declare_connection("czujnikOpadowInput", OutputObjectConnector(service_controller))

stacje = ['Bardo', 'Boboszów', 'Bystrzyca', 'Darnków', 'Duszniki', 'Gorzuchów', 'Kłodzko', 'Krosnowice', 'Kudowa Zdr.',
          'Lądek Zdr.']
obj={}

#Generowanie wartości opadów
def update_all():
    obj.clear()
    for s in stacje:
        wartosc = random.random()*200-100
        obj[s] = wartosc
    # return obj
    service_controller.get_connection("czujnikOpadowInput").send(obj) #wysłanie wartości parametrow z czujnika


while True:
    z = update_all()
    # print json.dumps(z, indent=1, ensure_ascii=False)
    time.sleep(25)