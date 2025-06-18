from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import pandas as pd

class ActionClaimSummary(Action):
    def name(self):
        return "action_claim_summary"

    def run(self, dispatcher, tracker, domain):
        #Get claim information
        policy_num = tracker.get_slot("policy_num")
        policy_name = tracker.get_slot("policy_name")
        description = tracker.get_slot("claim_description")
        date = tracker.get_slot("incident_date")
        time = tracker.get_slot("incident_time")
        location = tracker.get_slot("incident_location")
        additional_info = tracker.get_slot("additional_claim_info")

        response = f"Here is a summary of your claim:\n- Policy # {policy_num}\n- {policy_name} insurance\n- Description: {description}\n - Date: {date}\n - Time: {time}\n - Location: {location}\n- Additional information: {additional_info} "
        
        dispatcher.utter_message(response)
        
        return []