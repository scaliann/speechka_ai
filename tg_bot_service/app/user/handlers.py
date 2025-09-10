from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import BaseFilter

from app.db.db_helper import get_async_session
from app.keyboards.menu import kbs_menu, kb_terms
from app.user.repositories import UserRepository

router = Router()


class TermsAgreement(StatesGroup):
    waiting_for_agreement = State()


class UserAgreedFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        agreed = await check_user_agreement(message.from_user.id)
        return agreed


@router.message(F.text == "Профиль")
async def show_main_menu(message: Message):
    await message.answer("Ваш профиль: ")


@router.message(F.text == "Согласен с пользовательским соглашением")
async def agree_to_terms(message: Message, state: FSMContext):
    async with get_async_session() as orm_sess:
        repo = UserRepository(orm_sess)
        user = await repo.get_or_create(message.from_user.id)
        user.agreed_to_terms = True
        await orm_sess.commit()

    await state.clear()
    await message.answer(
        "✅ Спасибо! Вы согласились с пользовательским соглашением.\n\n"
        "Теперь вы можете пользоваться всеми функциями бота!",
        reply_markup=kbs_menu,
    )


@router.message(TermsAgreement.waiting_for_agreement)
async def handle_terms_state(message: Message):
    """Обрабатывает все сообщения во время ожидания соглашения"""
    if message.text != "Согласен с пользовательским соглашением":
        await message.answer(
            "⚠️ Для использования бота необходимо принять пользовательское соглашение.\n\n"
            "Пожалуйста, нажмите кнопку «Согласен с пользовательским соглашением».",
            reply_markup=kb_terms,
        )


async def check_user_agreement(tg_id: int) -> bool:
    """Проверяет, согласился ли пользователь с условиями"""
    async with get_async_session() as orm_sess:
        repo = UserRepository(orm_sess)
        user = await repo.get_or_create(tg_id)
        return user.agreed_to_terms


async def show_terms_agreement(message: Message, state: FSMContext):
    """Показывает пользовательское соглашение"""
    terms_text = """
📋 **ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ**

Добро пожаловать в наш сервис записи голоса!

**1. Общие положения**
Данное соглашение регулирует использование нашего Telegram бота для записи и анализа голоса.

**2. Сбор и обработка данных**
- Мы собираем ваши голосовые записи для анализа
- Данные обрабатываются в соответствии с политикой конфиденциальности
- Ваши личные данные защищены и не передаются третьим лицам

**3. Условия использования**
- Используйте сервис только для личных целей
- Не записывайте контент, нарушающий права других лиц
- Соблюдайте правила Telegram

**4. Ограничение ответственности**
Мы не несем ответственности за качество записи и результаты анализа.

**5. Изменения соглашения**
Мы оставляем право изменять данное соглашение с уведомлением пользователей.

Для продолжения использования сервиса необходимо принять условия соглашения.
    """

    await message.answer(terms_text, reply_markup=kb_terms, parse_mode="Markdown")
    await state.set_state(TermsAgreement.waiting_for_agreement)
