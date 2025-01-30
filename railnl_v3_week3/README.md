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
  - **/code/algorithms**: bevat de code voor de algoritmes.
  - **/code/classes**: bevat de verschillende classes die gebruikt worden voor dit project
- **/data**: bevat de verschillende databestanden die nodig zijn om de stations en verbindingen te plotten.
- **/output**: bevat alle verkregen bestanden bij het runnen van de experimenten.

### Algoritmes

Voor dit project zijn er verschillende algoritmes gebruikt om de optimale manier van lijnvoering te vinden.

## Random

Het random algoritme gebruikt een random start station en elk volgende station wordt ook weer random gekozen. Dit proces herhaalt zichzelf tot de maximale tijd van het traject is bereikt.

## Greedy

Het greedy algoritme gebruikt de heuristieken van de TrajectAnalyzer. Deze heuristieken zorgen ervoor dat de stations die maar één verbinding hebben, dus doodlopende stations, voorkeur stations zijn om vanaf te starten. Wanneer alle doodlopende stations bereden zijn. Krijgen stations met een oneven aantal verbindingen prioriteit. Wanneer al deze verbindingen ook bereden zijn, wordt het volgende start station random gekozen.
Het greedy algoritme werkt samen met deze heuristieken en kiest bij elke stap de volgende verbinding die de hoogste kwaliteit op levert.

## GreedyLookahead

Het greedylookahead algoritme is een child class van het greedy algoritme. Het verschil tussen beide algoritmes is dat de GreedyLookahead gebruikmaakt van een lookahead depth. Met deze lookahead depth worden er vanaf het start station meerdere stappen gesimuleerd om zo te berekenen welke route de hoogste kwaliteit oplevert. De hoeveelheid van de stappen die gesimuleerd worden is afhankelijk van de lookahead depth. Op basis van deze simulatie wordt de volgende stap gekozen en vervolgens herhaalt het proces zich. Zo wordt er telkens een stap gezet die de hoogste kwaliteit score oplevert.
In tegenstelling tot het greedy algoritme wat telkens slechts één stap vooruit simuleert, kijkt de greedylookahead meerdere stappen vooruit, wat kan leiden tot een betere beslissing op langer termijn.
Het start station van de GreedyLookahead kan de heuristieken van de TrajectAnalyzer gebruiken of kan een willekeurig start station kiezen door gebruik te maken van het random algoritme.

## Hillclimber

Het algoritme van de hillclimber optimaliseert de kwaliteits score door iteratief willekeurig het begin of het einde van een lijnvoering te vervangen met een nieuwe verbinding. Wanneer deze nieuwe verbinding zorgt voor een hogere kwaliteits score, zal deze verbinding behouden worden. Vervolgens herhaalt dit proces zich om zo de beste lijnvoering te vinden met de hoogste kwaliteits score.

## SimulatedAnnealing

Het algoritme van de SimulatedAnnealing werkt ongeveer hetzelfde als de HillClimber. Maar het algoritme kan in tegenstelling tot de HillClimber ook verbindingen accepteren die leiden tot een slechtere kwaliteits score.

## Depthfirst

De depthfirst is gebruikt voor het berekenen van de state space.

## Auteurs
- Marijn de Gans
- Lester Moumen
- Soesja van der Hilst
