import json
import urllib.request
import urllib.error


class SLMClient:
    """Connects the application to a locally running Ollama SLM."""

    def __init__(self, model="qwen2.5:1.5b"):
        self.model = model
        self.endpoint = "http://127.0.0.1:11434/api/generate"

    def generate(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 350
            }
        }

        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "").strip()

        except urllib.error.URLError as error:
            return f"Connection error: {error}"

        except Exception as error:
            return f"SLM error: {error}"
