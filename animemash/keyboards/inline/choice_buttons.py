from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import anime_choice, gen_anime


def keyboard_parameters(result_1, result_2):
    choice = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=result_1[0][1], callback_data=anime_choice.new(button="anime_one", winner=result_1[0][0],
                                                                                         anime_one=result_1[0][0], anime_one_rate=result_1[0][2], anime_two=result_2[0][0], anime_two_rate=result_2[0][2])),

                InlineKeyboardButton(text=result_2[0][1], callback_data=anime_choice.new(button='anime_two', winner=result_2[0][0],
                                                                                         anime_one=result_1[0][0], anime_one_rate=result_1[0][2], anime_two=result_2[0][0], anime_two_rate=result_2[0][2]))
            ],
            [
                InlineKeyboardButton(
                    text="Показать общий рейтинг", callback_data=gen_anime.new(action="show_rates"))
            ],
            [
                InlineKeyboardButton(
                    text="Показать личный список", callback_data=gen_anime.new(action="show_user_rates"))
            ]
        ]
    )
    return choice


answer_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да",
                                 callback_data=gen_anime.new(action="generate_anime")),
            InlineKeyboardButton(text="Нет",
                                 callback_data=gen_anime.new(action="bye"))
        ]
    ]
)
start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Играть",
                                 callback_data=gen_anime.new(action="generate_anime")),
            InlineKeyboardButton(text="Правила",
                                 callback_data=gen_anime.new(action="help")),
        ],
        [
            InlineKeyboardButton(text="Предыдущий список",
                                 callback_data=gen_anime.new(action="old_list"))
        ]
    ]
)

rates = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад",
                                 callback_data=gen_anime.new(action="return"))
        ]
    ]
)

rules = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подробнее",
                                 callback_data=gen_anime.new(action="details"))
        ],
        [
            InlineKeyboardButton(text="Начать игру",
                                 callback_data=gen_anime.new(action="return"))
        ]
    ]
)
start_game = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Начать игру",
                                 callback_data=gen_anime.new(action="return"))
        ]
    ]
)
refresh = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Закончить",
                                 callback_data=gen_anime.new(action="bye"))
        ]
    ]
)
