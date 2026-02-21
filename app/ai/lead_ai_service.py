from app.models.enums import AIRecommendation, ColdStage


class LeadAIService:

    @staticmethod
    async def analyze(lead):

        score = 0.2

        if lead.activity_count > 5:
            score += 0.3

        if lead.business_domain:
            score += 0.2

        if lead.stage == ColdStage.qualified:
            score += 0.3

        score = min(score, 1.0)

        recommendation = (
            AIRecommendation.transfer_to_sales
            if score >= 0.6
            else AIRecommendation.keep_nurturing
        )

        if not 0 <= score <= 1:
            raise ValueError("Invalid AI score")

        return {
            "score": score,
            "recommendation": recommendation,
            "reason": "Activity and domain driven scoring",
        }