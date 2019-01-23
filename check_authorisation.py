import simplejson as json
import csv
from datetime import datetime

idRFID = 0
temperature = -1

with open('autorisations.json') as file:
    json_data = json.load(file)
    #print(json_data)
    #print(json.dumps(json_data, sort_keys=True, indent=4 * ' '))

def ecrireLog(id, prenom, nom, autorisation):
    with open('log.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now().strftime('%d/%m/%Y-%H:%M:%S'),temperature, id, prenom, nom, autorisation])

def ecrireLogInconnu():
    ecrireLog('inconnu', 'inconnu', 'inconnu', 'inconnu')

def nbPersonnes():
    for personne in json_data['Personnes']:
        ID = personne['ID']

        if ID == idRFID:
            ecrireLog(idRFID, personne['prenom'], personne['nom'], personne['autorisation'])

            if personne['nb_personnes'] == '1':
                return 1
            else if personne['nb_personnes'] == '2':
                return 2
            else if personne['nb_personnes'] == '3':
                return 3

    #Le TAG ne correspond à aucune personnes du fichier JSON
    ecrireLogInconnu()
    return False


