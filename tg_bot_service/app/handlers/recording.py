from __future__ import annotations
import logging
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.db.db_helper import get_async_session
from app.keyboards.menu import kbs_menu, kb_menu
from app.recording.service import RecordingService
from app.user.handlers import check_user_agreement, show_terms_agreement

router = Router()
logger = logging.getLogger(__name__)


class Recording(StatesGroup):
    waiting_voice = State()


@router.message(F.text == "Начать запись")
async def start_diagnose(
    msg: Message,
    state: FSMContext,
):
    service = RecordingService(msg, state)

    agreed = await check_user_agreement(msg.from_user.id)

    if not agreed:
        await show_terms_agreement(msg, state)
        return

    async with get_async_session() as orm_sess:
        service = RecordingService(orm_sess)
        user, sess, words = await service.start_session(msg.from_user.id)

    await state.update_data(
        session_id=sess.id,
        word_ids=[w.id for w in words],
        words=[w.text for w in words],
        idx=0,
        user_id=user.id,
    )

    await msg.answer(
        f"🗝️ Сессия №{sess.session_number} открыта!\n\n🎯 Квест-предложение 1 из {len(words)}: <b>«{words[0].text}»</b>.\nНажми запись и произнеси его громко-смело, чтобы зарядить свой магический кристалл голоса! 🎙️",
        reply_markup=kb_menu,
        parse_mode="HTML",
    )
    await state.set_state(Recording.waiting_voice)


@router.message(Recording.waiting_voice, F.text == "Меню")
async def return_to_menu(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "🔙 Возвращаемся в главное меню! Запись прервана.", reply_markup=kbs_menu
    )


@router.message(Recording.waiting_voice, F.voice)
async def handle_voice(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data["idx"]
    word_ids = data["word_ids"]
    words_txt = data["words"]
    user_id = data["user_id"]
    sess_id = data["session_id"]

    async with get_async_session() as orm_sess:
        service = RecordingService(orm_sess)
        finished = await service.save_recording(
            bot=msg.bot,
            voice=msg.voice,
            sess_id=sess_id,
            user_id=user_id,
            word_id=word_ids[idx],
            tg_id=msg.from_user.id,
            total_words=len(word_ids),
        )
        logger.info("saved rec — session=%s word=%s", sess_id, word_ids[idx])

    if finished:
        await msg.answer(
            "🎉 Ура, герой! Ты собрал все волшебные кристаллы звуков — твой рюкзак сияет ярче радуги!🌈\nПерейди в раздел Диагностики, чтобы Хранитель Звуков отнес их в Звёздную лабораторию и приготовил для тебя тайный отчёт и новые задания. Спасибо за смелость и внимание! ✨",
            reply_markup=kbs_menu,
        )
        await state.clear()
        return

    idx += 1
    await state.update_data(idx=idx)
    await msg.answer(
        f"✅ Супер! Кристалл <b>{words_txt[idx - 1]}</b> пойман — он уже сияет в твоей коллекции. "
        f"Готов отправиться к следующему звуковому испытанию?\n\n"
        f"🎯 Квест-предложение {idx + 1} из {len(word_ids)}: «<b>{words_txt[idx]}</b>».\n"
        f"Нажми запись и произнеси его громко-смело, чтобы зарядить свой магический кристалл голоса! 🎙️",
        parse_mode="HTML",
        reply_markup=kb_menu,
    )


@router.message(Recording.waiting_voice)
async def handle_not_voice(msg: Message):
    await msg.answer(
        "Пожалуйста, пришли именно *голосовое сообщение*.", reply_markup=kb_menu
    )
