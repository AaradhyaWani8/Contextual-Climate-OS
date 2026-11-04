from datetime import datetime

class ContextManager:
    """Stores and manages current weather and user context."""

    def __init__(self):
        self.context = {}

    def update(self, city, temperature, humidity, prediction, role="Citizen"):
        self.context = {
            "city": str(city),
            "temperature": float(temperature),
            "humidity": float(humidity),
            "prediction": str(prediction),
            "role": str(role),
            "timestamp": datetime.now().isoformat(timespec="seconds")
        }
        return self.get_context()

    def get_context(self):
        return self.context.copy()

    def is_ready(self):
        return bool(self.context)

    def clear(self):
        self.context = {}
