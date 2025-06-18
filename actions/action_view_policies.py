from rasa_sdk import Action
import pandas as pd
import asyncio

class ActionViewPolicies(Action):
    def name(self):
        return "action_view_policies"

    async def run(self, dispatcher, tracker, domain):
        #Load CSV file
        file_path = "db/policies.csv"  # get information from your DBs
        df = pd.read_csv(file_path)
        customer_id = tracker.get_slot("customer_id")

        # Filter data for the given customer ID
        customer_info = df[df["customer_id"] == int(customer_id)]
        policies = customer_info['policy_type']
        expiration_dates = customer_info['expiration_date']
        premiums = customer_info['premium']
        limits = customer_info['limit']
        await asyncio.sleep(2) #Wait to load results

        if policies.empty:
            response = "No policies found."
        else:
            response = f"Here are all your available policies:\n"
            for policy, expiration_date, premium, limit in zip(policies, expiration_dates, premiums, limits):
                response += (f'\n🏠' if policy=='Homeowner' else f'\n🚗') + f" {policy}:\n - Expires on: {expiration_date}.\n - Premium: ${premium}, limit: ${limit}"
        
        dispatcher.utter_message(response)
        
        return []