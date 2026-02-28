import json
from datetime import datetime, timedelta
from openai import AsyncOpenAI
from app.schemas.ai import AIResponse
from app.core.config import settings


class AIService:

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_lead(self, lead) -> AIResponse:

        system_prompt = """
        You are a CRM AI assistant.

        Decision rules:

        1. If activity_count >= 12 → recommendation MUST be transfer_to_sales.
        2. If activity_count between 5 and 11 → keep_nurturing.
        3. If activity_count < 5 → keep_nurturing.
        4. If analysis_count >= 3 and activity_count < 5 → mark_as_lost.

        Return ONLY raw valid JSON.
        Do NOT wrap JSON in markdown.
        Do NOT add explanations.

        Required fields:
        - score (float between 0 and 1)
        - recommendation (transfer_to_sales, keep_nurturing, mark_as_lost)
        - reason (string)
        """

        user_prompt = json.dumps({
            "source": lead.source,
            "stage": lead.stage,
            "activity_count": lead.activity_count,
            "business_domain": lead.business_domain,
            "previous_score": lead.ai_score,
            "analysis_count": lead.ai_analysis_count
        })

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )

        raw_content = response.choices[0].message.content

        try:
            return AIResponse.model_validate_json(raw_content)

        except Exception as e:
            print("AI RAW RESPONSE:", raw_content)
            print("AI PARSE ERROR:", e)

            return AIResponse(
                score=0.5,
                recommendation="keep_nurturing",
                reason="Fallback due to AI parsing error"
            )