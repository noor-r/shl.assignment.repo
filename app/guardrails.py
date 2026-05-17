
OFF_TOPIC_KEYWORDS = [
    "lawsuit",
    "legal advice",
    "religion",
    "politics",
    "investment advice",
    "medical diagnosis"
]


class Guardrails:

    @staticmethod
    def is_off_topic(text: str):

        text = text.lower()

        for keyword in OFF_TOPIC_KEYWORDS:
            if keyword in text:
                return True

        return False
