
class RecommendationRanker:

    def rerank(
        self,
        query,
        results
    ):

        query = query.lower()

        scored = []

        for item in results:

            searchable = (
                item["name"] +
                " " +
                item["description"]
            ).lower()

            score = 0

            keywords = [
                "java",
                "python",
                "sql",
                "docker",
                "aws",
                "excel",
                "word",
                "sales",
                "customer"
            ]

            for keyword in keywords:

                if (
                    keyword in query and
                    keyword in searchable
                ):
                    score += 5

            scored.append(
                (score, item)
            )

        scored.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        return [x[1] for x in scored]
