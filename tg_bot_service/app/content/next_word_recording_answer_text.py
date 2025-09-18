def get_next_word_recording_answer_text(
    previous_word: str,
    next_word: str,
    current_word_number: int,
    total_words_length: int,
) -> str:
    text = f"""
✅ Молодец! Мы сохранили твой ответ!

🎯 Следующее предложение {current_word_number} из {total_words_length}: «<b>{next_word}</b>».
Нажми запись и произнеси его, чтобы зарядить свой магический кристалл голоса!
"""
    return text
