from groq import Groq

LANG_NAMES = {
    "auto": "the detected language",
    "sk": "Slovak",
    "cs": "Czech",
    "en": "English",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "pl": "Polish",
    "hu": "Hungarian",
    "uk": "Ukrainian",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
    "nl": "Dutch",
    "tr": "Turkish",
    "ar": "Arabic",
}


def translate_text(text: str, source_lang: str, target_lang: str, api_key: str) -> str | None:
    if not text.strip():
        return None
    try:
        client = Groq(api_key=api_key)
        src = LANG_NAMES.get(source_lang, source_lang)
        tgt = LANG_NAMES.get(target_lang, target_lang)

        if source_lang == "auto":
            prompt = f"Translate the following text to {tgt}. Return ONLY the translation, nothing else:\n\n{text}"
        else:
            prompt = f"Translate the following text from {src} to {tgt}. Return ONLY the translation, nothing else:\n\n{text}"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translator. Translate accurately and naturally. Return only the translated text, no explanations.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Chyba: {str(e)}"
