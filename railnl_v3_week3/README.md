# RailNL

De NS wilt de lijnvoering van intercitytreinen door Nederland verbeteren. Voor een optimale lijnvoering moet elke verbinding tussen de stations bereden zijn door minimaal één trein. Verder mag elk trein traject maximaal 180 minuten duren en mogen er maximaal 20 trein trajecten gebruikt worden.

## Aan de slag

### Vereisten

Deze codebase is volledig geschreven in python 3.10.8. In de requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze packages zijn te installeren door middel van pip  of conda met de volgende instructies:

'''
pip install -r requirements.txt

conda install --file requirements.txt
'''

### Gebruik

Om de code te runnen kan het volgende commant gebruikt worden:

'''
python main.py
'''

Door dit commant te gebruiken kunnen worden er verschillende algoritmes gerund.


### Structuur

Dit project is opgedeeld in verschillende mappen;

- **/code**: bevat alle code van dit project
  - **/code/algorithms**: bevat de code voor de algoritmes. De depthfirst is alleen gebruikt voor de berekening van de state space
  - **/code/classes**: bevat de verschillende classes die gebruikt worden voor dit project
- **/data**: bevat de verschillende databestanden die nodig zijn om de stations en verbindingen te plotten.
- **/output**: bevat alle verkregen bestanden bij het runnen van de experimenten.

### Algoritmes

Voor dit project zijn er verschillende algoritmes gebruikt om zo naar de beste manier van lijnvoering te vinden.

## Random

Het random algoritme gebruikt een random start station en elk volgende station wordt ook weer random gekozen. Dit proces
herhaald zichzelf tot de maximale tijd van het traject is bereikt.

## Greedy

Het greedy algoritme gebruikt de heuristieken van de TrajectAnalyzer. Deze heuristieken zorgen ervoor dat de stations die maar 1 verbinding hebben, dus doodlopende stations, voorkeur stations zijn om vanaf te starten. Wanneer alle doodlopende stations bereden zijn. Krijgen stations met een oneven aantal verbindingen prioriteit. Wanneer al deze verbindingen ook bereden zijn, wordt het volgende start station random gekozen.
Het greedy algoritme werkt samen met deze heuristieken en kiest bij elke stap de volgende verbinding die de hoogste kwaliteit op levert.

## GreedyLookahead

Het greedylookahead algoritme gebruikt de heuristieken van de TrajectAnalyzer of de randomise als start station.



## Auteurs
- Marijn de Gans
- Lester Moumen
- Soesja van der Hilst
