from __future__ import annotations

import html
from io import BytesIO

from aiogram import Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, FSInputFile, Message

from src.keyboards.user_keyboards import (
    get_example_controls_kb,
    get_language_kb,
    get_menu_kb,
    get_template_kb,
)
from src.rendering.template_renderer import (
    FIELD_ORDER,
    LANGUAGE_CHOICES,
    TEMPLATE_LAYOUTS,
    get_example_path,
    get_template_path,
    read_example_text,
    render_template_image_with_overrides,
    split_paragraphs,
)


router = Router()

LANGUAGE_LABELS = {
    "de": "Deutsch",
    "en": "English",
    "ru": "Русский",
}

STATUS_COLORS = {
    "blue": (0, 126, 255, 255),
    "yellow": (239, 151, 41, 255),
    "red": (235, 73, 63, 255),
    "green": (56, 163, 84, 255),
}

STATUS_ORDER = ("blue", "yellow", "red", "green")
STATUS_EMOJIS = {
    "blue": "🔵",
    "yellow": "🟡",
    "red": "🔴",
    "green": "🟢",
}


class BotFlow(StatesGroup):
    choosing_language = State()
    choosing_template = State()
    waiting_text = State()


def next_status_color(current: str) -> str:
    if current not in STATUS_ORDER:
        return STATUS_ORDER[0]
    index = (STATUS_ORDER.index(current) + 1) % len(STATUS_ORDER)
    return STATUS_ORDER[index]


def build_example_block(example_text: str) -> str:
    return f"Пример:\n<pre><code>{html.escape(example_text)}</code></pre>"


def build_instruction_text(language: str, template_number: int) -> str:
    template_path = get_template_path(language, template_number)
    example_text = read_example_text(language, template_number)
    if not example_text:
        example_text = (
            "Пример для этого шаблона еще не добавлен.\n"
            f"Положи файл {template_path.stem}_example.txt рядом с шаблоном."
        )

    return (
        "Введи текст построчно.\n"
        "Каждый абзац отделяй пустой строкой.\n"
        f"{build_example_block(example_text)}"
    )


def build_values_from_text(text: str) -> dict[int, str]:
    paragraphs = split_paragraphs(text)
    values: dict[int, str] = {}
    for index, field_number in enumerate(FIELD_ORDER):
        values[field_number] = paragraphs[index] if index < len(paragraphs) else ""
    return values


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(BotFlow.choosing_language)
    await message.answer("Выбери язык:", reply_markup=get_language_kb())


@router.callback_query(BotFlow.choosing_language, F.data.startswith("lang:"))
async def language_callback_handler(callback: CallbackQuery, state: FSMContext):
    language = callback.data.split(":", 1)[1]
    if language not in LANGUAGE_CHOICES:
        await callback.answer("Unknown language", show_alert=True)
        return

    await state.update_data(language=language)
    await state.set_state(BotFlow.choosing_template)

    await callback.message.edit_text(
        f"Язык выбран: {LANGUAGE_LABELS.get(language, language)}\nТеперь выбери темплейт:",
        reply_markup=get_template_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu:home")
async def menu_callback_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(BotFlow.choosing_language)
    await callback.message.edit_text("Выбери язык:", reply_markup=get_language_kb())
    await callback.answer()


@router.callback_query(BotFlow.choosing_template, F.data.startswith("template:"))
async def template_callback_handler(callback: CallbackQuery, state: FSMContext):
    template_number = int(callback.data.split(":", 1)[1])
    if template_number not in TEMPLATE_LAYOUTS:
        await callback.answer("Template not found", show_alert=True)
        return

    data = await state.get_data()
    language = data.get("language")
    if not language:
        await state.clear()
        await callback.message.edit_text("Нажми /start, чтобы начать.")
        await callback.answer()
        return

    await state.update_data(template_number=template_number, status_color="blue")
    await state.set_state(BotFlow.waiting_text)

    example_path = get_example_path(language, template_number)
    if example_path:
        await callback.message.answer_photo(
            photo=FSInputFile(str(example_path)),
            caption=build_instruction_text(language, template_number),
            reply_markup=get_example_controls_kb("blue"),
        )
    else:
        await callback.message.answer(
            build_instruction_text(language, template_number),
            reply_markup=get_example_controls_kb("blue"),
        )
    await callback.answer()


@router.callback_query(F.data == "status_color:cycle")
async def status_color_cycle_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("language")
    template_number = data.get("template_number")
    if not language or not template_number:
        await callback.answer("Сначала выбери язык и шаблон", show_alert=True)
        return

    current_color = data.get("status_color", "blue")
    new_color = next_status_color(current_color)
    await state.update_data(status_color=new_color)

    caption = build_instruction_text(language, template_number)
    await callback.message.edit_caption(
        caption=caption,
        reply_markup=get_example_controls_kb(new_color),
    )
    await callback.answer(f"Цвет: {STATUS_EMOJIS[new_color]}")


@router.message(BotFlow.waiting_text, F.text)
async def text_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language")
    template_number = data.get("template_number")
    status_color = data.get("status_color", "blue")

    if not language or not template_number:
        await state.clear()
        await message.answer("Начни заново через /start")
        return

    values = build_values_from_text(message.text or "")
    image = render_template_image_with_overrides(
        language,
        template_number,
        values,
        fill_overrides={6: STATUS_COLORS.get(status_color, STATUS_COLORS["blue"])},
    )

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    file_name = f"{language}_template{template_number}.png"
    result = BufferedInputFile(buffer.getvalue(), filename=file_name)

    await message.answer_photo(
        photo=result,
        caption="Готово",
        reply_markup=get_menu_kb(),
    )
    await state.clear()


@router.message()
async def fallback_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == BotFlow.waiting_text.state:
        await message.answer(
            "Пришли текст одним сообщением. Абзацы разделяй пустой строкой.",
            reply_markup=get_menu_kb(),
        )
        return

    await message.answer("Нажми /start, чтобы начать.", reply_markup=get_menu_kb())


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(router)
