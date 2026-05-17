from app.guardrails import Guardrails
from app.conversation import ConversationAnalyzer
from app.ranking import RecommendationRanker


class SHLAgent:

    def __init__(self, retriever):

        self.retriever = retriever
        self.guardrails = Guardrails()
        self.analyzer = ConversationAnalyzer()
        self.ranker = RecommendationRanker()

    def generate_recommendations(
        self,
        ranked
    ):

        recommendations = []

        for item in ranked[:5]:

            recommendations.append({
                "name": item["name"],
                "url": item["url"]
            })

        return recommendations

    def chat(
        self,
        messages
    ):

        latest_message = messages[-1]["content"]

        if self.guardrails.is_off_topic(
            latest_message
        ):

            return {
                "reply": (
                    "I can only help with SHL "
                    "assessment recommendations."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        context = self.analyzer.extract_context(
            messages
        )

        if self.analyzer.needs_clarification(
            context
        ):

            return {
                "reply": (
                    "What role are you hiring for?"
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # Build an enriched query from the full context so retrieval uses
        # role, seniority and skills — not just the latest message alone
        query_parts = [latest_message]

        if context["role"]:
            query_parts.append(context["role"])

        if context["seniority"]:
            query_parts.append(context["seniority"])

        if context["skills"]:
            query_parts.extend(context["skills"])

        enriched_query = " ".join(query_parts)

        retrieved = self.retriever.search(
            enriched_query
        )

        ranked = self.ranker.rerank(
            latest_message,
            retrieved
        )

        recommendations = (
            self.generate_recommendations(
                ranked
            )
        )

        return {
            "reply": (
                "Here are recommended SHL "
                "assessments for your "
                "requirements."
            ),
            "recommendations": recommendations,
            "end_of_conversation": False
        }
