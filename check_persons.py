import simplejson as json
import csv
from datetime import datetime

idRFID = 0

with open('persons.json') as file:
    json_data = json.load(file)

def nbPersonnes(tmp):
    for personne in json_data['Personnes']:
        ID = personne['ID']

        if ID == tmp:

            if personne['nb_personnes'] == '1':
                return 1
            elif personne['nb_personnes'] == '2':
                return 2
            elif personne['nb_personnes'] == '3':
                return 3

    return False


