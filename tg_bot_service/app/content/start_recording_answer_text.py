from app.models.words import Word


def get_recording_answer_text(
    recording_session_number: int,
    words: list[Word],
    word: str,
) -> str:
    text = f"""
🗝️ Сессия №{recording_session_number} открыта!

🎙Запиши все {len(words)} предложений в голосовых сообщениях, чтобы мы могли исследовать твой голос.

🎯 Предложение 1 из {len(words)}: <b>«{word}»</b>.
Нажми запись и произнеси его, чтобы зарядить свой магический кристалл голоса!
"""
    return text
