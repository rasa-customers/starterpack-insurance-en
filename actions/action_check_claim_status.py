from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

import pandas as pd
import datetime
import asyncio

class ActionListPolicies(Action):
    def name(self):
        return "action_check_claim_status"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        #Load CSV file
        file_path = "db/claims.csv"  # get information from your DBs
        df = pd.read_csv(file_path)
        customer_id = tracker.get_slot("customer_id")
        claim_id = tracker.get_slot("claim_number")

        # Check if required slots are available
        if customer_id is None:
            dispatcher.utter_message("Customer ID is required to check claim status")
            return [SlotSet("claim_status", 5)]
        if claim_id is None:
            dispatcher.utter_message("Claim number is required to check claim status")
            return [SlotSet("claim_status", 5)]

        # Filter data for the given customer ID
        claim_info = df[(df["customer_id"] == int(customer_id)) & (df["claim_id"] == claim_id)]

        await asyncio.sleep(2) #Wait to send results

        if claim_info.empty:
            claim_status = 5 #We use a different claim status for non-existing claims
            dispatcher.utter_message("No claim could be found with the provided claim number")
            return [SlotSet("claim_status", claim_status)]
        else:
            claim_status = int(claim_info.iloc[0]['claim_status'])
            claim_date = datetime.datetime.strptime(claim_info.iloc[0]['claim_date'], "%m/%d/%Y")
            adjustor_date = claim_date + datetime.timedelta(days=10)
            return [SlotSet("claim_status", claim_status),SlotSet("adjustor_date", adjustor_date.strftime('%m/%d/%Y'))]