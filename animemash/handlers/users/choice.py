from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, User
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.inline.choice_buttons import answer_choice, rates, keyboard_parameters, start, start_game, refresh, rules
from keyboards.inline.callback_data import anime_choice, gen_anime
from anime.animemash import gener_anime, choose_best_anime, get_new_rates, update_rates, show_rates, random_phrase
from anime.img_dwl import save_image
import mysql.connector
import random

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mikael-love",
    database="anime"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT COUNT(*) FROM animemash")
myresult = mycursor.fetchall()
rows = myresult[0][0]


def user_info(data, user_id, user_name):
    anime_list = random.sample(range(1, rows), 10)
    data['user_id'] = user_id
    data['user_name'] = user_name
    data['anime_list'] = anime_list
    data['final'] = False
    data['round'] = 1
    data['winner_list'] = []
    data['old_list'] = ''
    return data


def anime_media_gen(result_1, result_2):
    media = types.MediaGroup()
    media.attach_photo(types.InputFile(save_image(
        result_1[0][1], result_1[0][3])), result_1[0][1])
    media.attach_photo(types.InputFile(save_image(
        result_2[0][1], result_2[0][3])), result_2[0][1])
    return media


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    user_name = message.from_user.first_name
    async with state.proxy() as data:
        data = user_info(data, message.from_user.id, user_name)
        print(f"Зарегистрирован новый пользователь: {data['user_name']}")
        print(data['user_id'])
        sql = """SELECT * from anime_users WHERE user_id_anime =%s"""
        mycursor.execute(sql, (data['user_id'],))
        myresult = mycursor.fetchall()
        print(myresult)
        if len(myresult) == 0:
            sql = "INSERT INTO anime_users (user_id_anime , user_winner_list) VALUES (%s, %s)"
            mycursor.execute(sql, (data['user_id'], 'Пусто'))
            mydb.commit()
            data["old_list"] = 'Пусто'
        else:
            data["old_list"] = myresult[0][1]

    await message.answer(f"Привет, {user_name} добро пожаловать в AnimeMash!")
    await message.answer_sticker(r'CAACAgEAAxkBAAEBG0tfHq7a9x7k7JLAcBVg0oeBetR3WQACwCIAAnj8xgWCnglbp1nzEhoE')
    await message.answer("Начнем игру или прочитаем правила?", reply_markup=start)


@dp.callback_query_handler(gen_anime.filter(action="return"))
@dp.callback_query_handler(gen_anime.filter(action="generate_anime"))
async def generate_anime(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        print(data)
        if data.get('user_id') == None:
            data = user_info(data, call.from_user.id,
                             call.from_user.first_name)
        if data['round'] <= 3 and len(data['anime_list']) == 1:
            sql = 'SELECT * from animemash WHERE anime_id=%s'
            mycursor.execute(sql, (data['anime_list'][0],))
            myresult = mycursor.fetchall()
            winner_name = myresult[0][1]
            await call.message.answer(f"В {data['round']} раунде побеждает {winner_name}!")
            data['winner_list'].append(data['anime_list'][0])
            while True:
                check = True
                data['anime_list'] = random.sample(range(1, rows), 10)
                for item in data['anime_list']:
                    if item in data['winner_list']:
                        check = False
                        break
                if check == True:
                    break
            data['round'] += 1
        if data['round'] == 4 and data['final'] == False:
            await call.message.answer(text="Ого, вы смогли дойти до финального раунда")
            await call.message.answer_sticker(r'CAACAgEAAxkBAAEBG09fHrD61foUyndmqNsraV-E7ktO9AACuiIAAnj8xgXAcxWeRGOe3RoE')
            data['anime_list'] = []
            for item in data['winner_list']:
                data['anime_list'].append(item)
            data['final'] = True
        anime_one, anime_two = gener_anime(
            len(data['anime_list']), data['anime_list'], data['winner_list'])
        result_1, result_2 = choose_best_anime(
            anime_one, anime_two, mycursor)
        media = anime_media_gen(result_1, result_2)
        await call.message.reply_media_group(media=media)
        choice = keyboard_parameters(result_1, result_2)
        await call.message.answer(text="Выберите лучшее из двух аниме", reply_markup=choice)


@dp.callback_query_handler(anime_choice.filter(button='anime_one'))
@dp.callback_query_handler(anime_choice.filter(button='anime_two'))
async def choice_anime_one(call: CallbackQuery, callback_data: dict, state: FSMContext):
    winner = callback_data.get("winner")
    result_1 = callback_data.get("anime_one")
    result_1_rate = callback_data.get("anime_one_rate")
    result_2 = callback_data.get("anime_two")
    result_2_rate = callback_data.get("anime_two_rate")
    new_rate_A, new_rate_B = get_new_rates(
        winner, result_1, result_2, result_1_rate, result_2_rate)
    update_rates(new_rate_A, result_1, new_rate_B, result_2, mycursor, mydb)
    sql = 'SELECT * from animemash WHERE anime_id=%s'
    mycursor.execute(sql, (winner,))
    myresult = mycursor.fetchall()
    winner_name = myresult[0][1]
    async with state.proxy() as data:
        if data.get('user_id') == None:
            data = user_info(data, call.from_user.id,
                             call.from_user.first_name)
        if winner == result_1:
            data['anime_list'].remove(int(result_2))
        else:
            data['anime_list'].remove(int(result_1))

        if data['round'] == 4 and len(data['anime_list']) == 1:
            winner_id = data['anime_list'][0]
            rating = ''
            for item in data['winner_list']:
                sql = 'SELECT * from animemash WHERE anime_id=%s'
                mycursor.execute(sql, (item,))
                myresult = mycursor.fetchall()
                rating += f"— {myresult[0][1]}\n"
            sql = "UPDATE anime_users SET user_winner_list=%s WHERE user_id_anime =%s"
            mycursor.execute(sql, (rating, data['user_id']))
            mydb.commit()
            data['old_list'] = rating
            sql = 'SELECT * from animemash WHERE anime_id=%s'
            mycursor.execute(sql, (winner_id,))
            myresult = mycursor.fetchall()
            winner_name = myresult[0][1]
            await call.message.answer(f"Абсолютный победитель по вашему мнению это:")
            await call.message.answer_photo(myresult[0][3], myresult[0][1] + " !")
            await call.message.answer(f"Чтобы начать игру сначала нажмите /start", reply_markup=refresh)
        else:
            bot_response = winner_name + \
                random_phrase(data['user_name'])+"Продолжим?"
            await call.message.answer(text=bot_response, reply_markup=answer_choice)


@dp.callback_query_handler(gen_anime.filter(action="bye"))
async def generate_anime(call: CallbackQuery):
    await call.message.answer(text="Было весело, прощай!")
    return


@dp.callback_query_handler(gen_anime.filter(action="help"))
async def generate_anime(call: CallbackQuery):
    await call.message.answer(text="Правила:")
    await call.message.answer_sticker(r'CAACAgEAAxkBAAEBH21fIyFGq3tVyIZRLcrDyV-h8i2nlgACviIAAnj8xgXlUHBREO72ZBoE')
    await call.message.answer(text="Этот бот позволяет выбрать лучшее аниме.\nВам даются на выбор 2 аниме, выбирайте то, которое больше всего нравится и так по кругу)\nВам понадобится 5 раундов, чтобы сравнить все аниме, после этого вы выберете абсолютного победителя (для себя).", reply_markup=rules)


@dp.callback_query_handler(gen_anime.filter(action="show_user_rates"))
async def show_anime_rate(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data.get('user_id') == None:
            data = user_info(data, call.from_user.id,
                             call.from_user.first_name)
        if len(data['winner_list']) == 0:
            await call.message.answer(text='Ваш список пока что пуст', reply_markup=rates)
        else:
            winners = data['winner_list']
            index = 0
            rating = ''
            for item in winners:
                sql = 'SELECT * from animemash WHERE anime_id=%s'
                mycursor.execute(sql, (item,))
                myresult = mycursor.fetchall()
                rating += f"— {myresult[0][1]}\n"
            await call.message.answer(text=rating, reply_markup=rates)


@dp.callback_query_handler(gen_anime.filter(action="show_rates"))
async def show_anime_rate(call: CallbackQuery):
    rating = show_rates(mycursor)
    await call.message.answer(text=rating, reply_markup=rates)


@dp.callback_query_handler(gen_anime.filter(action="details"))
async def show_detailed_rules(call: CallbackQuery):
    await call.message.answer(text="Подробные правила:")
    await call.message.answer_sticker(r'CAACAgEAAxkBAAEBH-lfI7tXKzyJTyO9m15RoGpPTVDM5QACvCIAAnj8xgXC3jksMfFEvxoE')
    await call.message.answer(text="Это игра на выбывание!\nБудет всего 5 раундов (у нас много аниме на выбор).\nКаждый раунд будет генерироваться список из 10 аниме.\nИз них будут составляться пары. Аниме, которое вы не выбераете выходит из игры.\nПосле каждого раунда сохраняется победитель.\nВ финальном раунде вы будете выбирать между победителями прошлых раундов.\n\nТермины:\nЛичный список - это аниме, которые победили в каждом раунде\nОбщий рейтинг - вычисляется для каждого аниме по ответам пользователей.\nАбсолютный победитель - аниме-победитель всех раундов лично для пользователя.\nУдачной игры!", reply_markup=start_game)


@dp.callback_query_handler(gen_anime.filter(action="old_list"))
async def show_old_list(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.answer(text=data['old_list'], reply_markup=start_game)
