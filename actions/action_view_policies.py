from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import pandas as pd
import asyncio

class ActionViewPolicies(Action):
    def name(self):
        return "action_view_policies"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        #Load CSV file
        file_path = "db/policies.csv"  # get information from your DBs
        df = pd.read_csv(file_path)
        customer_id = tracker.get_slot("customer_id")
        # Check if customer_id is valid
        if customer_id is None:
            dispatcher.utter_message("I don't have your customer ID. Please provide your customer ID to view your policies.")
            return []
        # Filter data for the given customer ID
        customer_info = df[df["customer_id"] == int(customer_id)]
        await asyncio.sleep(2) #Wait to load results

        if customer_info.empty:
            response = "No policies found."
        else:
            response = f"Here are all your available policies:\n"
            for _, row in customer_info.iterrows():
                policy = row['policy_type']
                expiration_date = row['expiration_date']
                premium = row['premium']
                limit = row['limit']
                response += (f'\n🏠' if policy=='Homeowner' else f'\n🚗') + f" {policy}:\n - Expires on: {expiration_date}.\n - Premium: ${premium}, limit: ${limit}"

        dispatcher.utter_message(response)
        return []