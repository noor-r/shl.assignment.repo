
class ConversationAnalyzer:

    def extract_context(self, messages):

        full_text = " ".join(
            [m["content"] for m in messages]
        ).lower()

        context = {
            "role": None,
            "seniority": None,
            "skills": [],
            "personality_required": False
        }

        roles = [
            "developer",
            "engineer",
            "analyst",
            "manager",
            "admin",
            "sales",
            "customer service",
            "contact center"
        ]

        seniority_levels = [
            "graduate",
            "entry",
            "mid",
            "senior",
            "director",
            "executive",
            "cxo"
        ]

        skills = [
            "java",
            "python",
            "sql",
            "docker",
            "aws",
            "spring",
            "angular",
            "excel",
            "word",
            "networking"
        ]

        for role in roles:
            if role in full_text:
                context["role"] = role

        for level in seniority_levels:
            if level in full_text:
                context["seniority"] = level

        for skill in skills:
            if skill in full_text:
                context["skills"].append(skill)

        if "personality" in full_text:
            context["personality_required"] = True

        return context

    def needs_clarification(self, context):

        return context["role"] is None

    def is_comparison_query(self, text):

        text = text.lower()

        comparison_words = [
            "difference",
            "compare",
            "vs",
            "versus"
        ]

        return any(
            word in text
            for word in comparison_words
        )
