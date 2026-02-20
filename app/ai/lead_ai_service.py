from typing import Dict


class LeadAIService:
    async def analyze_lead(self, lead) -> Dict:

        activity = lead.activity_count or 0
        domain = lead.business_domain

        score = 0.3 + min(activity * 0.1, 0.6)

        recommendation = (
            "transfer_to_sales"
            if score >= 0.6 and domain
            else "keep_in_cold"
        )

        return {
            "score": round(score, 2),
            "recommendation": recommendation,
            "reason": f"activity={activity}, domain={'set' if domain else 'not set'}"
        }