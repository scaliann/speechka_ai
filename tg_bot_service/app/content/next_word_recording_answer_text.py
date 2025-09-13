def get_next_word_recording_answer_text(
    previous_word: str,
    next_word: str,
    current_word_number: int,
    total_words_length: int,
) -> str:
    text = f"""
✅ Супер! Кристалл <b>{previous_word}</b> пойман — он уже сияет в твоей коллекции. 
Готов отправиться к следующему звуковому испытанию?"

🎯 Квест-предложение {current_word_number} из {total_words_length}: «<b>{next_word}</b>»."
Нажми запись и произнеси его громко-смело, чтобы зарядить свой магический кристалл голоса! 🎙️
"""
    return text
