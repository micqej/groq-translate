from groq import Groq

LANG_NAMES = {
    "auto": "detected language",
    "sk": "Slovak", "cs": "Czech", "en": "English",
    "de": "German", "fr": "French", "es": "Spanish",
    "it": "Italian", "pl": "Polish", "hu": "Hungarian",
    "uk": "Ukrainian", "ru": "Russian", "zh": "Chinese",
    "ja": "Japanese", "ko": "Korean", "pt": "Portuguese",
    "nl": "Dutch", "tr": "Turkish", "ar": "Arabic",
}


def translate_text(text: str, source_lang: str, target_lang: str, api_key: str):
    if not text.strip():
        return None
    try:
        client = Groq(api_key=api_key)
        tgt = LANG_NAMES.get(target_lang, target_lang)
        src = LANG_NAMES.get(source_lang, source_lang)

        if source_lang == "auto":
            prompt = f"Translate to {tgt}. Return ONLY the translation:\n\n{text}"
        else:
            prompt = f"Translate from {src} to {tgt}. Return ONLY the translation:\n\n{text}"

        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a translator. Return only the translated text, nothing else."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=2048,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Chyba: {e}"
