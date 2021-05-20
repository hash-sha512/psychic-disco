from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet

import requests
import json
import os
import re


class ActionForSamePincode(Action):
    def name(self):
        return "action_for_same_pincode"

    def run(self, dispatcher, tracker, domain):
        same_pincode = tracker.get_latest_entity_values('same_pincode')
        if(same_pincode == 'yes'):
            pincode = tracker.get_slot('pincode')
            return [SlotSet("pincode", pincode)]
        else:
            return [SlotSet("pincode", None)]


class ActionForSameCategory(Action):
    def name(self):
        return "action_for_same_category"

    def run(self, dispatcher, tracker, domain):
        same_category = tracker.get_latest_entity_values('same_category')
        if(same_category == 'yes'):
            category = tracker.get_slot('category')
            return [SlotSet("category", category)]
        else:
            return [SlotSet("category", None)]



    
def api_call_for_city(pincode):
    url=f"https://api.postalpincode.in/pincode/{pincode}"
    city = None
    try:
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
        if(response[0]['Status'] == 'Success'):
            city = response[0]['PostOffice'][0]['District']
    except requests.exceptions.HTTPError as err:
         raise SystemExit(err)
    return city
    
def api_call_for_resource(city, category):
    url=f"http://ec2-3-23-130-174.us-east-2.compute.amazonaws.com:8000/resource?city={city}&category={'%20'.join(category.split())}"
    data = None
    try:
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
 
        data = json.dumps(response)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return data
    print(response.status_code)


class pincodeCategoryForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "pincode_category_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["pincode", "category"]

    @staticmethod
    def category_list() -> List[Text]:
        """Database of supported resources"""

        return [
            "CoVID-19 Testing Lab",
            "Free Food",
            "Fundraisers",
            "Hospitals and Centers",
            "Delivery [Vegetables, Fruits, Groceries, Medicines, etc.]",
            "Police",
            "Government Helpline",
            "Other",
            "Mental well being and Emotional Support",
            "Accommodation and Shelter Homes",
            "Senior Citizen Support",
            "Transportation",
            "Community Kitchen",
            "Ambulance",
            "Fire Brigade",
            "Quarantine Facility",
            "Helpline for Cyclone Amphan",
            "Fever Clinic"
        ]

    def validate_pincode(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate pincode value."""

        if re.search("^[0-9]{6}$", value):
            return {"pincode": value}
        else:
            dispatcher.utter_message(template="utter_ask_pincode")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"pincode": None}

        return city
        print(response.status_code)

    def validate_category(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate category value."""

        if value in pincodeCategoryForm.category_list():
            # validation succeeded, set the value of the "category" slot to value
            return {"category": value}
        else:
            dispatcher.utter_message(template="utter_ask_category")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"category": None}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        pincode = tracker.get_slot('pincode')
        category = '%20'.join(tracker.get_slot('category').split())
        city = api_call_for_city(pincode)  
        #data is in json.dumps format
        data = api_call_for_resource(city, category)      
        dispatcher.utter_message("There ya go. {1} in {0} \n {2}".format(city, ' '.join(category.split('%20')), data))
        print(pincode, ' '.join(category.split('%20')))
        return []

