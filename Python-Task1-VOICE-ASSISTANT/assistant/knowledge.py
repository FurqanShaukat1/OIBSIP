import requests


class KnowledgeService:

    SEARCH_URL = "https://en.wikipedia.org/w/api.php"

    def ask(self, question: str):
        if not question:
            return "Please tell me what you would like to know."

        params = {
            "action": "query",
            "list": "search",
            "srsearch": question,
            "format": "json",
            "utf8": 1,
            "srlimit": 1
        }

        try:
            response = requests.get(
                self.SEARCH_URL,
                params=params,
                timeout=10,
                headers={
                    "User-Agent": "VoiceAssistant/1.0"
                }
            )

            response.raise_for_status()

            data = response.json()

            results = data.get("query", {}).get("search", [])

            if not results:
                return "I couldn't find an answer to that question."

            title = results[0]["title"]

            summary_url = (
                "https://en.wikipedia.org/api/rest_v1/page/summary/"
                + requests.utils.quote(title)
            )

            summary_response = requests.get(
                summary_url,
                timeout=10,
                headers={
                    "User-Agent": "VoiceAssistant/1.0"
                }
            )

            summary_response.raise_for_status()

            summary_data = summary_response.json()

            answer = summary_data.get("extract")

            if not answer:
                return "I found the topic, but I couldn't retrieve a useful answer."

            # Keep voice responses reasonably short
            if len(answer) > 500:
                answer = answer[:500].rsplit(".", 1)[0] + "."

            return answer

        except requests.exceptions.Timeout:
            return "The knowledge service took too long to respond."

        except requests.exceptions.ConnectionError:
            return "I couldn't connect to the knowledge service."

        except requests.exceptions.RequestException:
            return "The knowledge service returned an error."

        except (ValueError, KeyError, TypeError):
            return "I received an unexpected response from the knowledge service."