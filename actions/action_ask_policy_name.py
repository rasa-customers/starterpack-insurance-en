from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import pandas as pd

class ActionAskPolicyName(Action):
    def name(self):
        return "action_ask_policy_name"

    def run(self, dispatcher, tracker, domain):
        #Load CSV file
        file_path = "db/policies.csv"  # get information from your DBs
        df = pd.read_csv(file_path)
        customer_id = tracker.get_slot("customer_id")

        # Filter data for the given customer ID
        customer_info = df[df["customer_id"] == int(customer_id)]
        policies = customer_info['policy_type']
        policy_nums = customer_info['policy_num']

        if policies.empty:
            dispatcher.utter_message(text="No policies found.")
        else:
            buttons = []
            for policy,policy_num in zip(policies,policy_nums):
                print(policy, policy_num)
                buttons.append(
                    {
                        "title": policy,
                        "payload": f"/SetSlots(policy_name={policy}, policy_num={str(policy_num)})"
                    }
                )
            dispatcher.utter_message(response="utter_select_policy_name", buttons=buttons)
        return []