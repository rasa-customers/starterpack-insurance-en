from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import pandas as pd

class ActionAskPolicyNum(Action):
    def name(self):
        return "action_ask_policy_num"

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

        # Filter data for the given customer ID
        # Check if customer_id is valid
        if customer_id is None:
            dispatcher.utter_message("I don't have your customer ID. Please provide your customer ID to view your policies.")
            return []
        customer_info = df[df["customer_id"] == int(customer_id)]
        policies = customer_info['policy_type']
        policy_nums = customer_info['policy_num']

        if len(policies) == 0:
            dispatcher.utter_message(text="No policies found.")
        else:
            buttons = []
            for policy,policy_num in zip(policies,policy_nums):
                print(policy, policy_num)
                buttons.append(
                    {
                        "title": f"{policy} ({policy_num})",
                        "payload": f"/SetSlots(policy_name={policy}, policy_num={str(policy_num)})"
                    }
                )
            dispatcher.utter_message(response="utter_select_policy_name", buttons=buttons)
        return []