<?php

/*
 * Nom du Script:
 * netatmo_battery.php
 *
 * Description:
 * Script pour afficher le pourcentage des batteries 
 * des modules de la station météo Netatmo
 *
 * Version du script:
 * V 1.0 du 30/01/2017
 *
 * Autheur du Script:
 * Seb iDomo
 * 
 */

$output = exec('python ./stationmeteo_battery.py');
$fichier = 'stationmeteo_battery.xml';

$xml = simplexml_load_file($fichier);

header("Content-type: text/xml");
echo $xml->asXML();

?>
