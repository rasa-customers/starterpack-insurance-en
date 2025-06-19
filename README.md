# starterpack-insurance-en

## Rasa Starter Pack: US Insurance use case
<p align="center">
  <img src="images/Insurance_illustration.png" alt="Alt Text">
</p>

Rasa has created a starterpack for building AI assistants focussed in the insurance industry. The assistant focuses on auto and home insurance. This assistant leverages Rasa's CALM framework.
This repository contains a Rasa chatbot designed to assist customers with filing a claim, checking the status of an existing claim and FAQs. The assistant contains two primary flows:

- Filing a claim
  - The user is guided through the steps to file a claim
  - They can file a claim under any of their active insurance policies
  - The flow differs from home insurance and auto insurance claims
- Checking a claim's status
  - Custom actions are used to retrieve existing claims from a DB
  - Status is provided to the user
  - User has the option to be connected to a human agent

  This can be used as a starting point to create your own insurance assistant or get aideas on the features you may want to implement. It's free for you to copy and use locally.

# Recommendations
Before leveraging this assistant it is recommended you are familiar with Rasa's CALM framework. 
 - [Here](https://learning.rasa.com/rasa-pro/) you will find an introductory course to Rasa CALM.
 - [Here](https://www.classmarker.com/online-test/start/?quiz=bqd664cbca515357) you will find a developer certificatione exam.

# Project Structure
Here's a brief description of the directories and files in the project root:
  - **README.md**: The file you're currently reading!
  - **actions:** Contains Python scripts defining custom actions for the Rasa assistant.
  - **db:** Contains csv files that are used to mimic the behavior of connecting to a database to get customer information.
  - **data:** Contains flow definitions for the assistant. If needed, flows can be triggered by some intents by adding the nlu file with examples for intents.
  - **docs:** Contains sample documents for Enterprise Search.
  - **domain:** Contains domain files for the assistant.
  - **prompts**: Contains Jinja2 template files for generating prompts.
  - **tests:** Contains end-to-end test scenarios for the assistant where each subdirectory reflects a suite of tests (i.e. happy path).
  - **Config:** Contains multiple configuration components for the assistant (i.e. different language models and settings). If Intents are needed then we need the NLU pipeline for it(tokennizer, featurizer, intent classifier ..) and **NLUCommandAdaptor** will be the component that will start a flow based on the intent prediction.
  - **Credentials**: Contains credentials for various services used by the Rasa assistant (i.e. Chat Widget)
  - **Endpoints**: Contains endpoint configurations for the Rasa assistant. 
    - How to run the action server is added
    - How to call NLG server
    - How to define the model group
# Conversation example
##  **First example**:<br>Filing an auto insurance claim
  - **Bot**: Hey Serena 👋
        I'm Poly, your AI assistant at Universal Insurance 🔐
        I can help you start a claim and check its status.
        What would you like to do?
  - **User**: I want to file a claim
  - **Bot**: Here are all your available policies:
        🏠 Homeowner (9738812)
        Expires on: 01/01/2020
        🚗 Car (9738813)
        Expires on: 01/01/2026
        Which policy would you like to file a claim under?
  - **User**: Car
  - **Bot**: Could you please describe what happened and what caused the damage?
  - **User**: Someone hit my car in a traffic light
  - **Bot**: What was the exact date of the incident? Please use mm/dd/yyyy format.
  - **User**: 12/24/2024
  - **Bot**: What was the exact time of the incident?
  - **User**: 3pm
  - **Bot**: Where did the incident happen?
  - **User**: Times square
  - **Bot**: Please write the contact details of any witnesses and the number of police report if available.
  - **User**: Contact: John John +1 100200300
  - **Bot**: Here is a summary of your claim:
        Policy # 9738813
        Car insurance
        Description: Someone hit my car in a traffic light
        Date: 12/24/2024
        Time: 3pm
        Location: Times square
        Additional information: Contact: John John +1 100200300
        Does everything look correct?
  - **User**: Yes
  - **Bot**: Thank you. Shall I submit this claim for you?
  - **User**: Yes
  - **Bot**: I have submitted your claim number 12345.
        An adjuster will be assigned to your claim

##  **Second example**:<br>Intervening and asking a knowledge base question
  - **Bot**: Hey Serena 👋
        I'm Poly, your AI assistant at Universal Insurance 🔐
        I can help you start a claim and check its status.
        What would you like to do?
  - **User**: I want to file a claim
  - **Bot**: Here are all your available policies:
        🏠 Homeowner (9738812)
        Expires on: 01/01/2020
        🚗 Car (9738813)
        Expires on: 01/01/2026
        Which policy would you like to file a claim under?
  - **User**: Car
  - **Bot**: Could you please describe what happened and what caused the damage?
  - **User**: Someone hit my car in a traffic light
  - **Bot**: What was the exact date of the incident? Please use mm/dd/yyyy format.
  - **User**: What happens if the other driver didn't have insurance?
  - **Bot**: If the other driver is uninsured, your Uninsured Motorist (UM) coverage will be crucial. It can cover your medical expenses and, in some states, vehicle repairs. If you have Collision coverage, it will pay for your car's repairs (minus your deductible) regardless of the other driver's insurance status.
  - **Bot**: What was the exact date of the incident? Please use mm/dd/yyyy format.
  - **User**: 12/24/2024
  - **Bot**: What was the exact time of the incident?
  - **User**: 3pm
  - **Bot**: Where did the incident happen?
  - **User**: Times square
  - **Bot**: Please write the contact details of any witnesses and the number of police report if available.
  - **User**: Contact: John John +1 100200300
  - **Bot**: Here is a summary of your claim:
        Policy # 9738813
        Car insurance
        Description: Someone hit my car in a traffic light
        Date: 12/24/2024
        Time: 3pm
        Location: Times square
        Additional information: Contact: John John +1 100200300
        Does everything look correct?
  - **User**: Yes
  - **Bot**: Thank you. Shall I submit this claim for you?
  - **User**: Yes
  - **Bot**: I have submitted your claim number 12345.
        An adjuster will be assigned to your claim

##  **Third example**:<br>Correcting input
  - **Bot**: Hey Serena 👋
        I'm Poly, your AI assistant at Universal Insurance 🔐
        I can help you start a claim and check its status.
        What would you like to do?
  - **User**: I want to check a claim status
  - **Bot**: Could you please write the claim number?
  - **User**: CLAIM1234
  - **Bot**: Thank you. I will check the claim status for you. One moment please.
      We are assigning an adjustor to your case, it normally takes 24-48 h since submitting the claim.
      The adjustor will be assigned by 01/11/2025.
      Let me know if you would like to check your claim status or file a claim. I'll be here ready to help! 😊
  - **User**: Sorry I meant CLAIM1236
  - **Bot**: Thank you. I will check the claim status for you. One moment please.
      We are in the process of scheduling an inspection to see your damages.
      Would you like to submit dates and times for the inspection appointment?
  - **User**: No

##  **Third example**:<br> List policies & Enterprise Search
  - **Bot**: Hey Serena 👋
        I'm Poly, your AI assistant at Universal Insurance 🔐
        I can help you start a claim and check its status.
        What would you like to do?
  - **User**: list my available policies
  - **Bot**: Let me retrieve your policy information, just a moment please.
        Here are all your available policies:
        🏠 Homeowner:
        Expires on: 01/01/2020.
        Premium: $10000, limit: $500000
        🚗 Car:
        Expires on: 01/01/2026.
        Premium: $2000, limit: $80000
  - **User**: What is a premium
  - **Bot**: A premium is the amount you pay for your insurance policy, typically on a monthly, semi-annual, or annual basis, to maintain your coverage. For example, your car insurance premium is $2,000, and your homeowner's insurance premium is $10,000.

# Features and bot content explanation
In this project you will find:
 - **Actions** : custom actions, mimic getting information from a DB, either adding it to the session start or afterwards in the conversation. They are also used to generate dynamic buttons based on the content in the DB. This behaviour is done using 3 CSVs in the DB folder.
 - **RAG** :through Rasa's enterprise search policy to answer informational question from the user based on the docs in the docs folder.
 - **Data**
    - **Flows** : are built to handle transactional user queries. This assistant had two main flows: "file a claim" and "check claim status" which are divided in sub-flows. Different features are used : calling or linking a flow, branching on a slot value, etc.
    - **Patterns** : Rasa assistants use patterns (pre-built flow templates) to handle conversation repair and some system behaviour. In this assistant we override some patterns, to change the standard behavior. When editing patterns make sure you keep the same pattern name.
 - **Documents** : have general information on the two policy types covered. These will be used by enterprise search to provide RAG based answers.
 - **Domain** : contains all bot responses, slot definitions and custom actions
  - **Responses** : There are responses that contain buttons, images as well as standard responses.
  - **Slots** : different slot type and mapping
    - **type** : Float, text, bool and categorical
    - **mappings** : from_llm, and controlled
    - **validation**: carry out validation to ensure slot value matches required format
 - **Images** : These images are used in the README
 - **Prompts** : This is an edited verion of the standard rephraser prompt. You can edit this to change the personality of the assistant.
 - **Tests** : this is a good way to test the bot's capabilities and ensure the same behavior when doing changes and updates. With Assertions we can track commands and when slots are set. Results of the current tests are available in the tests folder to illustrate how e2e testing works. You can mimic the results by running the command `rasa test e2e tests/e2e_test_cases -o` 
 - **Config**: We have two sections, the pipeline and the policies
     - the pipeline we have `CompactLLMCommandGenerator` that will convert user messages into commands, we add the LLM we want to use here
     - the policies: two policies are used in this assistant the `FlowPolicy` and the `EnterpriseSearchPolicy`

# Installation
You can find [here](https://learning.rasa.com/pre-requisites/pre-requisites/) our Rasa enablement and step by step guide on how to install Rasa. <BR>
Our docs provide an [Installation Overview](https://rasa.com/docs/pro/installation/overview/).

## Prerequisites
- Rasa licence for 3.12 +
- Python 3.10 +
- Point to the LLM provider in the endpoint.yml and config.yml 
  it can be open AI, finetuned model or any other LLM provider see [here](https://rasa.com/docs/rasa-pro/concepts/components/llm-configuration-from-3-11)

## Set up 
- Clone the repository:

  ```shell
  git clone <rasa-customers/starterpack-insurance-en.git>
  cd <rasa-customers/starterpack-insurance-en>
  ```

- Create and activate a virtual environment, you can use `venv` (built-in Python virtual environment) or any other virtual environment manager.

```shell
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```
  Make sure this environment is always active when you are testing or building the assistant.

- Train the Rasa model: `rasa train -d domain`

# Running the Bot
- To run the bot you can use `rasa inspect --debug`
- After any changes made to your data, domain folder or config file you need to retrain the bot running `rasa train -d domain` and if changes are made in the custom actions just re-run `rasa inspect --debug`
- After adding changes, make sure to add `e2e test cases`, to do so
  - Set `RASA_PRO_BETA_E2E_ASSERTIONS=true` environment variable before
running the command.
  - Install `pip install mlflow` when you use an LLM to generate the answer with enterprise search.
  - Run `rasa test e2e <add path to the test folder> -o` to see how the bot is performing, `-o` to get the results.
    For this project it will be `rasa test e2e tests/e2e_test_cases -o` in the tests folder you will then have two files
      - `e2e_results_failed.yml` and `e2e_results_passed.yml`

# Tips
- Check our docs to understand all [Rasa primitives](https://rasa.com/docs/reference/primitives/)
  - Get familiar with all flow properties, patterns, responses
- Start writing e2e test cases right when you start writing your flows, you can start by copying what we have in **inspector view** in the **end-2-end test** section.
- When you are trying to debug look for these sections in your logs.
  - Always review the prompt in the logs to make sure the right flows and slots are available and check the conversation history to better understand the bot's behavior.
  - Search for `action_list` to see the command that was predicted by CALM, this will help you debug.
    For instance, it can be `action_list=StartFlow(file_claim)` or `action_list=SetSlot(customer_id, 123)`
  - Search for `commands=` 
    For instance `commands=[StartFlowCommand(flow='file_claim')]`
  - Check the **tracker state** in the **inspector view**
  - Add `logging.info` to you custom actions to get more visibility.


# Next Steps
- You can extend the assistant's skills:
  - It can be improving the existing two skills or adding new ones.
    Examples:
    - Add new claims to the claims DB when they are submitted
    - Edit the `action_list_policies` and `flow_file_claim` to allow for more than one policy of the same type
    - Create a flow to get an insurance quote
- Create diagrams that illustrates the conversation flow. A conversation designer will be a perfect expert to rely on to accomplish this step. You can use Rasa Studio to do this.
- Start building the flows and adding e2e test cases
- Share the first versions with your colleague to test and provide feedback.
- Improve, test, re-share 🔁

# Contributing
Feel free to fork this repo and submit pull requests. Suggestions and improvements are always welcome!

# License
- This project is licensed under the Apache 2.0 License, allowing modification, distribution, and usage with proper attribution.