from aiogram.types import  KeyboardButton, ReplyKeyboardMarkup
from texts import start_action_button, first_part_button, second_part_button


def get_start_keyboard():
    kb = [
        [KeyboardButton(text=f"{first_part_button}"), KeyboardButton(text=f"{second_part_button}")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери, что хочешь порешать"
    )
    return keyboard


def first_part_keyboard():
    kb = [
        [KeyboardButton(text=f"Задание {x + 1}") for x in range(4)],
        [KeyboardButton(text=f"Задание {x + 1}") for x in range(4, 8)],
        [KeyboardButton(text=f"Задание {x + 1}") for x in range(8, 12)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери, что хочешь порешать"
    )
    return keyboard


def second_part_keyboard():
    kb = [
        [KeyboardButton(text=f"Задание {x + 1}") for x in range(13,16)],
        [KeyboardButton(text=f"Задание {x + 1}") for x in range(16,19)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери, что хочешь порешать"
    )
    return keyboard


def go():
    kb = [
        [KeyboardButton(text=f"{start_action_button}")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_task_keyboard(task):
    if task == 'рандомное задание':
        kb = [
            [KeyboardButton(text=f"Еще {task}"), KeyboardButton(text=f"Нет, пойду отдыхать ☺️")],
            [KeyboardButton(text=f"Меню")]
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Напиши ответ")
    else:
        kb = [
            [KeyboardButton(text=f"Еще задание {task}"), KeyboardButton(text=f"Нет, пойду отдыхать ☺️")],
            [KeyboardButton(text=f"Меню")]
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Напиши ответ")
    return keyboard


def yes_no():
    kb = [
        [KeyboardButton(text=f"Да"), KeyboardButton(text=f"Пока нет")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="как поступим?"
    )
    return keyboard


def send_or_not():
    kb = [
        [KeyboardButton(text=f"Отправляем рассылку, все хорошо"),
         KeyboardButton(text=f"Поменять сообщение"),
         KeyboardButton(text=f"Выйти")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="как поступим?"
    )
    return keyboard