# -*- coding: utf-8 -*-
import json
from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector
from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi


service_controller = DevServiceController("alarmService.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("wynikPredykcjiOutput", InputObjectConnector(service_controller)) #analogicznie jak wyżej dla drugiego interfejsu

#Output zapisuje do pliku wynik.json w celu wykorzystania do wywietlania danych na stronie
wynik = service_controller.get_connection("wynikPredykcjiOutput")
while True: #główna pętla programu
    obj = wynik.read() #odczyt danych z interfejsu wejściowego
    z = json.dumps(obj, indent=1, ensure_ascii=False).encode('utf-8')
    f = open('wynik.json', 'w')
    f.write(z)
    f.close()


