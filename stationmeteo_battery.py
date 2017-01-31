# Nom du Script:
# stationmeteo_battery.py
#
# Description du script:
# Script qui recupere le pourcentage des batteries
# des modules de la station meteo Netatmo
#
# Version du Script:
# V 1.0 du 30/01/2017
#
# Auteur du script:
# Seb iDomo 
#

import requests
import json
from lxml import etree
from pprint import pprint

################################
# Debut du code fourni par Netatmo
payload = {'grant_type': 'password',
           'username': "IDENTIFIANT Netatmo",
           'password': "MotDePasse du compte",
           'client_id':"ID correspondant à une application créée sur le site de développement Netatmo",
           'client_secret': "MotDePasse correspondant à l'application créée sur le site de développement Netatmo",
           'scope': 'read_station'}
try:
    response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
    response.raise_for_status()
    access_token=response.json()["access_token"]
    scope=response.json()["scope"]
except requests.exceptions.HTTPError as error:
    print(error.response.status_code, error.response.text)

params = {
    'access_token': access_token,
    'device_id': 'Adresse MAC de la station météo'
}

try:
    response = requests.post("https://api.netatmo.com/api/getstationsdata", params = params)
    response.raise_for_status()
    data = response.json()["body"]
# Fin du code fourni par Netatmo
################################

# Recuperation du pourcentage restant de la batterie des differents modules
# Pour permettre le fonctionnement du script avec seulement le module exterieur
# chaque variable est mise avec la valeur du module par defaut
    #pprint(data)

# Module temperature exterieur
    assert(u'battery_percent' in data[u'devices'][0][u'modules'][0])
    percent_ext = data[u'devices'][0][u'modules'][0][u'battery_percent']
# Module anenometre
    assert(u'battery_percent' in data[u'devices'][0][u'modules'][0])
    percent_ano = data[u'devices'][0][u'modules'][0][u'battery_percent']
# Module pluviometre
    assert(u'battery_percent' in data[u'devices'][0][u'modules'][0])
    percent_pluv = data[u'devices'][0][u'modules'][0][u'battery_percent']
# Module complementaire interieur
    assert(u'battery_percent' in data[u'devices'][0][u'modules'][0])
    percent_int = data[u'devices'][0][u'modules'][0][u'battery_percent']
except requests.exceptions.HTTPError as error:
    print(error.response.status_code, error.response.text)

# creation de la structure XML 
ext = etree.Element("EXT")
battery = etree.SubElement(ext, "BATTERY")
# Module exterieur
value1 = etree.SubElement(battery, "VALUE1")
value1.text = str(percent_ext)
# Module anenometre
value2 = etree.SubElement(battery, "VALUE2")
value2.text = str(percent_ano)
# Module pluviometre
value3 = etree.SubElement(battery, "VALUE3")
value3.text = str(percent_pluv)
# Module interieur
value4 = etree.SubElement(battery, "VALUE4")
value4.text = str(percent_int)

fichier = etree.ElementTree(ext)
fichier.write("stationmeteo_battery.xml")

