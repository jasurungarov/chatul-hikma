import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def answer_question(question: str, lang: str = "uz") -> str:
    prompt = {
        "uz": "Siz faqat Qur'on va sahih hadis asosida javob beradigan islomiy yordamchisiz.",
        "en": "You are an Islamic assistant who answers only using the Quran and authentic Hadith.",
        "ru": "Вы исламский помощник, который отвечает только на основе Корана и достоверных хадисов.",
        "kg": "Сиз Куран жана сахих хадистерге гана таянып жооп берген ислам жардамчысысыз."
    }

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt.get(lang, prompt['uz'])},
            {"role": "user", "content": question}
        ],
        max_tokens=500,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
