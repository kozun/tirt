#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import json
from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector, OutputObjectConnector #import modułów konektora object_connector
from ComssServiceDevelopment.service import Service, ServiceController #import modułów klasy bazowej Service oraz kontrolera usługi


class AlarmService(Service): #klasa usługi musi dziedziczyć po ComssServiceDevelopment.service.Service
    def __init__(self): #"nie"konstruktor, inicjalizator obiektu usługi
        super(AlarmService, self).__init__() #wywołanie metody inicjalizatora klasy nadrzędnej
        self.obj = {} #zmienna do przechowywania wartości parametru
        self.obj_lock = threading.RLock() #obiekt pozwalający na blokadę wątku

    def declare_outputs(self): #deklaracja wyjść
        self.declare_output("wynikPredykcjiOutput", OutputObjectConnector(self)) #deklaracja wyjścia "filtersOnOutput" będącego interfejsem wyjściowym konektora object_connector

    def declare_inputs(self):
        self.declare_input("czujnikOpadowInput", InputObjectConnector(self)) #deklaracja wejścia "filtersOnInput" będącego interfejsem wyjściowym konektora object_connector


    def run(self): #główna metoda usługi


        obj_input = self.get_input("czujnikOpadowInput") #obiekt interfejsu wejściowego
        wynik_output = self.get_output("wynikPredykcjiOutput") #obiekt interfejsu wyjściowego

        while self.running(): #pętla główna usługi (wątku głównego obsługującego strumień wideo)
            czujnikOpadow = obj_input.read() #odebranie danych z interfejsu wejściowego
            with self.obj_lock: #blokada wątku
                self.obj = czujnikOpadow #pobranie aktualnej wartości opadow
            f = open('stany.json', 'r+')
            baza = json.load(f, encoding='utf-8')
            wynik = {}


            #Test działania inputu, czy generowane wartosci opadow sa mniejsze niz 10
            for o, w in self.obj.iteritems():
                print baza[unicode(o)]["stan_alarmowy"]
                wynik[unicode(o)] = {}
                wynik[unicode(o)][u"stan_początkowy"] = baza[unicode(o)][u"stan_początkowy"]
                wynik[unicode(o)][u"stan_alarmowy"] = baza[unicode(o)][u"stan_alarmowy"]
                wynik[unicode(o)][u"stan_krytyczny"] = baza[unicode(o)][u"stan_krytyczny"]
                wynik[unicode(o)][u"opady"] = round(w, 2)

                predykcja = (w/100)*12 + baza[unicode(o)][u"stan_początkowy"]
                wynik[unicode(o)][u"przewidywany_poziom"] = round(predykcja, 2)
                if predykcja > baza[unicode(o)][u"stan_krytyczny"]:
                    wynik[unicode(o)][u"klasyfikacja"] = 3
                elif predykcja > baza[unicode(o)][u"stan_alarmowy"]:
                    wynik[unicode(o)][u"klasyfikacja"] = 2
                else:
                    wynik[unicode(o)][u"klasyfikacja"] = 1

            wynik_output.send(wynik) #przesłanie ramki za pomocą interfejsu wyjściowego

if __name__=="__main__":
    sc = ServiceController(AlarmService, "alarmService.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi
