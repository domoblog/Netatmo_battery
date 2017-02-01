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
           'password': "MotDePasse",
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

batteries = {}

try:
    response = requests.post("https://api.netatmo.com/api/getstationsdata", params = params)
    response.raise_for_status()
    data = response.json()["body"]
# Fin du code fourni par Netatmo
################################

# Recuperation du pourcentage restant de la batterie des differents modules de la station
    for mod in data[u'devices'][0][u'modules']:
		assert(u'battery_percent' in mod)
		percent = mod[u'battery_percent']
		mod_name = mod[u'module_name']
		batteries[mod_name] = percent
		print(mod_name)
		print(batteries[mod_name])

except requests.exceptions.HTTPError as error:
    print(error.response.status_code, error.response.text)

# Creation de la structure XML 
ext = etree.Element("Ext")
battery = etree.SubElement(ext, "Battery")

for mod_name in batteries:
	value = etree.SubElement(battery, mod_name)
	value.text = str(batteries[mod_name])

fichier = etree.ElementTree(ext)
fichier.write("stationmeteo_battery.xml")
