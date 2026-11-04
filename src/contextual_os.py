from concurrent.futures import ThreadPoolExecutor
from context_manager import ContextManager
from slm_client import SLMClient


class ContextualOS:
    """
    Contextual OS application layer.
    Manages context, detects user intent and routes tasks to the SLM.
    """

    def __init__(self):
        self.context_manager = ContextManager()
        self.slm = SLMClient()
        self.executor = ThreadPoolExecutor(max_workers=3)

    def set_context(self, city, temperature, humidity,
                    prediction, role="Citizen"):

        return self.context_manager.update(
            city, temperature, humidity, prediction, role
        )

    def identify_intent(self, question, role="Citizen"):
        question = question.lower()
        role = role.lower()

        if role == "farmer" or any(word in question for word in
                ["farmer", "farming", "crop", "agriculture"]):
            return "agriculture_advisory"

        if role == "outdoor worker" or any(word in question for word in
                ["worker", "labour", "labor", "outdoor"]):
            return "worker_advisory"

        if role == "health worker" or any(word in question for word in
                ["hospital", "patient", "health"]):
            return "health_advisory"

        if role == "local authority" or any(word in question for word in
                ["authority", "municipal", "government"]):
            return "authority_advisory"

        if any(word in question for word in
                ["precaution", "protect", "safety"]):
            return "safety_advisory"

        if any(word in question for word in
                ["explain", "why", "meaning"]):
            return "explanation"

        return "general_weather_query"

    def build_prompt(self, question, context, intent):
        return f"""
You are the contextual AI assistant of a Climate Intelligence System.

CURRENT WEATHER CONTEXT:
City: {context['city']}
Temperature: {context['temperature']} degrees Celsius
Humidity: {context['humidity']} percent
Machine Learning Prediction: {context['prediction']}
User Role: {context['role']}
Timestamp: {context['timestamp']}

DETECTED USER INTENT:
{intent}

USER QUESTION:
{question}

INSTRUCTIONS:
1. Personalise your answer using the supplied weather context.
2. Give advice relevant to the user's role.
3. Do not invent weather measurements or forecasts.
4. Do not claim this prototype prediction is an official IMD warning.
5. Give practical, easy-to-understand information in 4-5 concise bullet points.
6. Use complete sentences and finish your answer.
7. If information is missing, acknowledge it.
8. Recommend following official local heat-health and disaster-management advisories.
"""

    def ask(self, question):
        context = self.context_manager.get_context()

        if not context:
            return {
                "intent": "missing_context",
                "context": {},
                "answer": "Please provide weather information first."
            }

        intent = self.identify_intent(
            question,
            context.get("role", "Citizen")
        )

        prompt = self.build_prompt(question, context, intent)
        future = self.executor.submit(self.slm.generate, prompt)
        answer = future.result()

        return {
            "intent": intent,
            "context": context,
            "answer": answer
        }

    def close(self):
        self.executor.shutdown(wait=False)
