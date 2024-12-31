import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.dispatcher.router import Router
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import asyncio

API_TOKEN = "7979219338:AAHYbOKMph4-5vFPXCK8yVXtiysasQtjNh8"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

heroes = [
    "Тетерєва Аліса",
    "Сифіліс Радіка",
    "Планокур",
    "Квадробер імпотент",
    "Ухилянт",
    "Лобкова блоха пса патрона",
    "Пакетик з травою",
    "Барига на інвалідній колясці",
    "Узбек скінхед"
]

TPH = [
    "Чубукін",
    "Ільгам",
    "Злобний ваговод",
    "Тоха",
    "Накурений циган на електросамокаті",
    "Таксист Мурат",
    "Тіп в костюмі піци",
    "Чорнобильський голуб",
    "Сухопутний окунь",
    "Мать одиночка"
]

places = [
    "8 общага ХНУРЕ",
    "Гадяч",
    "Шиза Дані",
    "Полтавська область",
    "Гольф ільгама",
    "Синагога",
    "Гараж отчима"
]

events = [
    "тебе зловив бусик ТЦК",
    "перед тобою чорна камрі уебалась в гараж",
    "під припаркованою бмв не оказалось калюжі масла",
    "хтось насрав тобі на балкон 8 етажа",
    "утренній кофе оказався без віскаря"
]

actions = [
    "покурити",
    "насрати в кувшин",
    "написати в інсті заметку про права женщин",
    "визвать на Радіка мусоров",
    "в'їбати стопарік Єгеря",
    "Усиновити маленького цигана",
    "визвати шлюху по оголошенню з газети",
    "обрізати шкільному автобусу тормозний шланг",
    "положить мотор на гольфові",
    "зігонути біля посольства ізраїля",
    "здати карлика в детдом",
    "настругать в гель для душа",
    "здати бомжа в налогову за незадекларовані доходи",
    "дати кенту вместо віагри проносне",
    "підкинути кенту в підвал 3 дітей і заложити його мусорам"
]

TPHactions = [
    "начав опускать водний",
    "достав з барсетки чіхуахуа і кинув в тебе",
    "набрав братву шоб дать тобі пизди",
    "зняв штани перед дитиною з дцп",
    "прийняв іслам",
    "попросив не пиздити його сина інваліда",
    "осідлав коня і поїхав в Румунію",
    "зарядив вставну челюсть бабулі на Фьюрі",
    "положив на пол фальшиву сотку шоб бомж нагнувся і його пробили",
    "поставив пам'ятник Бандері в центрі Варшави",
    "сказав охранніку в атб шо школьник уносить літр джека в воровському кармані",
    "зайшов в церкву в костюмі бетмена"
]

active_games = {}


def start_story(user_id):
    return {
        "step": 0,
        "hero": random.choice(heroes),
        "place": random.choice(places),
        "event": random.choice(events),
        "history": []
    }


def generate_keyboard(options):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=option)] for option in options],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def generate_next_step(game_state):
    step = game_state["step"]
    if step == 0:
        return (
            f"Ти {game_state['hero']}, живеш у {game_state['place']}. Одного дня {game_state['event']}. "
            f"Що ти робиш?",
            random.sample(actions, 3)
        )
    elif step == 1:
        return (
            f"Твоя дія призвела до неочікуваного! {random.choice(TPH)} {random.choice(TPHactions)}. "
            f"Що далі?",
            random.sample(actions, 3)
        )
    elif step == 2:
        return (
            f"Після цього він викликав на тебе ТЦК, вони сказали що єдиний твій шанс не поїхати штурмувати посадки це потрапити в дурку. "
            f"Твої дії?",
            random.sample(actions, 3)
        )
    elif step == 3:
        return (
            f"Поки ти намагався с'їбати від ТЦК з {random.choice(places)} вийшли {random.choice(heroes)} та {random.choice(TPH)}. "
            f"Поки перший {random.choice(TPHactions)} біля ТЦК, другий підкрався до тебе ззаду та {random.choice(TPHactions)} "
            f"Що робитимеш?",
            random.sample(actions, 3)
        )
    elif step == 4:
        return (
            f"Нормальний варіант, але тепер треба тікати від циган які побачили у тебе шайбу з насваєм. "
            f"Ти біжиш на зупинку та сідаєш в автобус. Цигани позаду, проте водій впізнає тебе та питає чи то не ти вчора {random.choice(TPHactions)} "
            f"Що тепер?",
            random.sample(actions, 3)
        )
    elif step == 5:
        return (
            f"Ото ти видав! "
            f"За таке бабки виганяють тебе з автобуса на ходу та ти ідеш пішки по трасі в сторону Белгорода "
            f"Твої дії?",
            random.sample(actions, 3)
        )
    else:
        return (
            "Воно б то все заїбісь, але тебе збила чорна камрі. Хочеш почати знову? тисни /game",
            []
        )


@router.message(Command(commands=["game", "start"]))
async def start(update: types.Message):
    user_id = update.from_user.id
    active_games[user_id] = start_story(user_id)
    game_state = active_games[user_id]

    step_text, options = generate_next_step(game_state)

    keyboard = generate_keyboard(options)

    await update.answer(step_text, reply_markup=keyboard)


@router.message()
async def handle_response(update: types.Message):
    user_id = update.from_user.id
    if user_id not in active_games:
        await update.answer("Напиши /game, щоб почати нову гру!")
        return

    game_state = active_games[user_id]

    if update.text not in actions:
        await update.answer("Вибери дію із запропонованих варіантів.")
        return

    game_state["step"] += 1

    step_text, options = generate_next_step(game_state)
    keyboard = generate_keyboard(options)

    await update.answer(step_text, reply_markup=keyboard)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
