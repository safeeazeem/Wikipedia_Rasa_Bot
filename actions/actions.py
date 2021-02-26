# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions




from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json, requests, random



class ActioResetAllSlots(Action): 
    def name(self):
        return 'action_reset_all_slots'

    def run(self, dispatcher,tracker, domain): 
            return[AllSlotsReset()]

class ActionWikipedaiaResults(Action):

    def name(self) -> Text:
        return "action_give_results"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        search_Term = tracker.get_slot('search_query')
        # more_article = tracker.get_slot('more_article')
        # search_Term = 'skyscraper'

        Api_URL = 'https://en.wikipedia.org/w/api.php?action=opensearch&namespace=0&format=json&search='  
        full_URL = Api_URL + search_Term

        search = requests.get(full_URL)
        json_data = json.loads(search.text)

        print(search_Term)
        length = len(json_data[1])
        if len(json_data[1])>0:
        
            links = {}
            for x in range(len(json_data[1])):
                links[json_data[1][x]]=json_data[3][x]

            # chosing random key
            r_choice= random.choice(list(links.values()))  

            dispatcher.utter_message(f'{links[search_Term.capitalize()]}')
            # SlotSet('more_article', r_choice)

            print(links)
            return[SlotSet('more_article', r_choice)]
        else: 
            print(search_Term)
            dispatcher.utter_message(f"I didn't find '{search_Term}' in Wikipedia. ")

        # return[SlotSet('more_article', r_choice)]

        
