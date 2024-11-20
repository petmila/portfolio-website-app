from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_pagination_keyboard(items: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for item in items:
        row = []
        for key, value in item.items():
            row.append(
                InlineKeyboardButton(
                    text=key,
                    callback_data=value))
        rows.append(row)
    markup = InlineKeyboardMarkup(inline_keyboard=rows, resize_keyboard=True)
    return markup

