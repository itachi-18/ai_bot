from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .db import get_faq_answer
from .gpt_service import ask_gpt
import requests
import os


class ActionHandleQuery(Action):
    def name(self) -> Text:
        return "action_handle_query"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message["intent"].get("name")
        user_msg = tracker.latest_message.get("text")

        if intent == "ask_faq":
            answer = get_faq_answer(user_msg)
            response = answer if answer else ask_gpt(user_msg)

        elif intent == "ask_weather":
            city = next(tracker.get_latest_entity_values("city"), "London")
            api_key = os.getenv("OPENWEATHER_API_KEY")
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            data = requests.get(url).json()
            if data.get("main"):
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                response = f"The weather in {city} is {temp}°C with {desc}."
            else:
                response = "I couldn't find weather for that location."

        else:  # Default to GPT
            response = ask_gpt(user_msg)

        dispatcher.utter_message(text=response)
        return []
