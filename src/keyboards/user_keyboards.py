from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_language_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Deutsch", callback_data="lang:de")]]
    )


def get_template_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1", callback_data="template:1"),
                InlineKeyboardButton(text="2", callback_data="template:2"),
                InlineKeyboardButton(text="3", callback_data="template:3"),
            ],
            [InlineKeyboardButton(text="🔙 Menu", callback_data="menu:home")],
        ]
    )


def get_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Menu", callback_data="menu:home")]]
    )


def get_example_controls_kb(selected_color: str) -> InlineKeyboardMarkup:
    emoji_map = {
        "blue": "🔵",
        "yellow": "🟡",
        "red": "🔴",
        "green": "🟢",
    }
    emoji = emoji_map.get(selected_color, "🔵")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{emoji} Сменить цвет {emoji}",
                    callback_data="status_color:cycle",
                )
            ],
            [InlineKeyboardButton(text="🔙 Menu", callback_data="menu:home")],
        ]
    )


def get_result_kb(language: str, template_number: int, status_color: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="↻ Повторить",
                    callback_data=f"repeat:{language}:{template_number}:{status_color}",
                )
            ],
            [InlineKeyboardButton(text="🔙 Menu", callback_data="menu:home")],
        ]
    )
