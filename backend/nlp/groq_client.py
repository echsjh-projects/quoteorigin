"""
nlp/groq_client.py
------------------
Sends gathered source snippets to Groq's LLaMA 3.3 70B model and asks it
to reason about the quote's true origin, speaker, and earliest date.

Why Groq instead of Anthropic?
  Groq's free tier offers ~14,400 requests/day with very fast inference
  (they use custom LPU hardware). Perfect for a CV project.
"""

import json
import re
from groq import AsyncGroq
from config import get_settings

settings = get_settings()
client = AsyncGroq(api_key=settings.groq_api_key)

# The model to use — LLaMA 3.3 70B is Groq's best free-tier model
GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a quotation provenance expert and historian. 
Your task is to determine the true origin of a quote: who first said it, 
when, and in what exact original wording. You are rigorous, cite evidence, 
and acknowledge uncertainty honestly. You never fabricate attributions."""

EXTRACTION_PROMPT = """A user wants to know the provenance of this quote:
"{quote}"

I have gathered the following source snippets from the web:

{context}

Based on these sources and your knowledge, determine:
1. The most likely original speaker or author
2. The earliest known date (be specific if possible: year, or year-month, or full date)
3. The likely original phrasing (before it was paraphrased/misquoted)
4. Your confidence level (0.0 to 1.0)
5. A brief explanation of your reasoning (2-4 sentences)

Respond ONLY with valid JSON, no markdown, no commentary:
{{
  "speaker": "Full name or 'Unknown'",
  "earliest_date": "e.g. 1940, or 1940-06-18, or 'circa 1850', or null",
  "original_phrasing": "The earliest known exact wording",
  "confidence": 0.85,
  "reasoning": "Brief explanation..."
}}"""


async def extract_provenance(quote: str, context_snippets: list[dict]) -> dict:
    """
    Given a quote and a list of source dicts (each with 'snippet', 'platform', 'url'),
    asks Groq to reason about the provenance and returns a structured dict.
    """
    # Build context string from top sources
    context_parts = []
    for i, s in enumerate(context_snippets[:8], 1):
        platform = s.get("platform", "web")
        snippet = s.get("snippet", "").strip()
        date = s.get("mentioned_date", "")
        speaker = s.get("speaker_mentioned", "")
        line = f"[Source {i} — {platform}]"
        if date:
            line += f" Date: {date}"
        if speaker:
            line += f" | Speaker mentioned: {speaker}"
        line += f"\n{snippet}"
        context_parts.append(line)

    context = "\n\n".join(context_parts) if context_parts else "No sources found."

    prompt = EXTRACTION_PROMPT.format(quote=quote, context=context)

    try:
        response = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,   # low temperature = more factual, less creative
            max_tokens=600,
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown code fences if the model added them despite instructions
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"```$", "", raw).strip()

        return json.loads(raw)

    except json.JSONDecodeError:
        # Fallback if the model returns malformed JSON
        return {
            "speaker": "Unknown",
            "earliest_date": None,
            "original_phrasing": quote,
            "confidence": 0.0,
            "reasoning": "Could not parse LLM response. Please try again.",
        }
    except Exception as e:
        return {
            "speaker": "Error",
            "earliest_date": None,
            "original_phrasing": quote,
            "confidence": 0.0,
            "reasoning": f"LLM error: {str(e)}",
        }
