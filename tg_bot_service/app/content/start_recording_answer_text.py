from app.models.words import Word


def get_recording_answer_text(
    recording_session_number: int,
    words: list[Word],
    word: str,
) -> str:
    text = f"""
🗝️ Сессия №{recording_session_number} открыта!

🎯 Квест-предложение 1 из {len(words)}: <b>«{word}»</b>.
Нажми запись и произнеси его громко-смело, чтобы зарядить свой магический кристалл голоса! 🎙️
"""
    return text
