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

Vervolgens worden er verschillende algoritmes gerunt en zal dit verschillende uitkomsten geven.

'''
voorbeeld van output toevoegen
'''

### Structuur

Dit project is opgedeeld in verschillende mappen;

- **/code**: bevat alle code van dit project
  - **/code/algorithms**: bevat de code voor de algoritmes. De depthfirst is alleen gebruikt voor de berekening van de state space  --> run_experiments/experiment verplaatsen naar classes
  - **/code/classes**: bevat de verschillende classes die gebruikt worden voor dit project
- **/data**: bevat de verschillende databestanden die nodig zijn om de stations en verbindingen te plotten.

## Auteurs
- Marijn de Gans
- Lester Moumen
- Soesja van der Hilst 
