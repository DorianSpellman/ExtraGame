from aiohttp.client import *
from aiohttp import payload, web
from aiohttp.client import request
from random import choice
import os

HOST_IP = "0.0.0.0"
HOST_PORT = 1288

stories = [] # Рассказы
state = 0  # Состояния


def handler_function(request):
    global state
    global stories
    buttons = []
    end_session = False
    message = ''
    tts = ''
    session = request['session']
    version = request['version']
    request = request['request']
    list_of_request = request['nlu']['tokens']

    if session['new'] or state == 0:
        with open('steps.txt', newline='', encoding="utf-8") as stor:   
            stories = stor.readlines()

### Приветствие

        message = "Привет! Новый год — прекрасная и сказочная пора!" + "\nЖелаете отправиться в путешествие в мир этого праздника и узнать о нём больше?"  
        tts = "^Привет^! Новый год — 'прекрасная, и 'сказочная пора!" + "\n ^Желаете^ отправиться в путешествие в 'мир этого 'праздника и узнать о нём 'больше? — Узнать, что Вас ^ждёт^, Вы можете, задав соответствующий вопрос!" # Закончить путешествие можно в любой момент, сказав заверши путешествие
        buttons = [button('Да!'), button('Что меня ждёт?'), button('Не сейчас')]
        state = 10

### Начало       
    elif state == 10:
        
        if 'ок' in list_of_request or 'окей' in list_of_request or 'да' in list_of_request  or  'давай' in list_of_request  or  'вперёд' in list_of_request or  'вперед' in list_of_request or "поехали" in list_of_request or 'желаю' in list_of_request or 'хорошо' in list_of_request or 'отправиться' in list_of_request:
            message += choice(['Отлично, поехали!', 'Начинаем путешествие!']) + '\n'
            state = 20

        elif 'стоп' in list_of_request or 'нет' in list_of_request or 'выход' in list_of_request or 'не' in list_of_request or 'заверши' in list_of_request or 'завершить' in list_of_request:
            state = 100

        elif 'что' in list_of_request or 'ждёт' in list_of_request or 'ждет' in list_of_request or'ожидает' in list_of_request:
            message += "Мы окунёмся в историю праздника, его традиции, а также построим снеговика и загадаем желание!"
            tts = "Мы окунёмся в ^историю^ праздника, его ^традиции^, \n а также построим снеговика, — и загадаем желание!"
            state = 21
        
        else:
            message = 'Повторите ещё раз'
            tts = message
            buttons = [button('Да!'), button('Не сейчас'), button('Что меня ждёт?')]

    if state == 21:
        buttons = [button('Поехали!'), button('Не сейчас')]
        state = 22
    
    elif state == 22:
        
        if 'да' in list_of_request or 'ок' in list_of_request or 'окей' in list_of_request or 'да' in list_of_request  or  'давай' in list_of_request  or  'вперёд' in list_of_request or  'вперед' in list_of_request or 'поехали' in list_of_request  or 'хорошо' in list_of_request:
            message += choice(['Отлично, поехали!', 'Начинаем путешествие!']) + '\n'
            state = 20

        elif 'нет' in list_of_request or 'выход' in list_of_request or 'не' in list_of_request or 'назад' in list_of_request or 'заверши' in list_of_request or 'завершить' in list_of_request or 'стоп' in list_of_request:
            state = 100



### История праздника
    if state == 20 and stories:
        story = stories[0] # запоминаем первый рассказ
        stories.pop(0) # удаляем из списка
        message += story + '\n' # воспроизведение истории
        tts = "Отлично! Тогда начинаем путешествие! \n Вернёмся в прошлое. <speaker audio=marusia-sounds/things-cuckoo-clock-1> \n История ^празднования^ Нового Года уходит в Месопотамию, где зародилась традиция отмечать весеннее пробуждение природы. \n Праисходило это в марте. \n Уже ^тогда^ веселье длилось ^двенадцать^ дней.\n Никто в эти дни не раб`отал, люди ходили на гуляния и ^маскарады^! \n Позжэ, обычай встречать Новый Год, перен`яли греки — затем египтяне и римляне." 
        tts += "\n В России Новый Год не всегда отмечали в ночь, с тридцать первого декабря, на первое января. \n Сначала его праздновали первого марта, затем — первого сентября. \n Но в тысяча шестьсот девяносто девятом году, царь — Петр Первый — издал указ, о праздновании Нового Года ` первого января.\n С тех пор праздник не менял свою дату. \n Готовы узнать ещё больше?"

        story = stories[0] 
        stories.pop(0)
        message += story

        story = stories[0] 
        stories.pop(0)
        message += story

        buttons = [button('Готов!'), button('Завершить путешествие')]
        state = 25

    elif state == 25:

        ### перепрыгивание на следующее
        if 'да' in list_of_request or 'ок' in list_of_request or 'окей' in list_of_request or 'готов' in list_of_request or 'готовы' in list_of_request or 'ага' in list_of_request or 'давай' in list_of_request or 'следующее' in list_of_request or 'дальше' in list_of_request  or 'вперёд' in list_of_request or 'вперед' in list_of_request  or 'хорошо' in list_of_request:
            state = 30

        ### завершение путешествия
        elif 'завершить' in list_of_request or 'заверши'in list_of_request or 'закончи' in list_of_request  or 'хватит' in list_of_request:
            state = 80

        elif 'стоп' in list_of_request or 'выход' in list_of_request:
            state = 110
            
        else:
            message = 'Повторите ещё раз'
            tts = message
            buttons = [button('Готов!'), button('Завершить путешествие')]


### Символ года

    if state == 30 and stories:
        story = stories[0]
        message += story 
        stories.pop(0)
        tts += "Дальше я расскажу о символе года по восточному календарю! \n Символом наступающего две тысячи двадцать второго года является голубой, водяной тигр. <speaker audio=marusia-sounds/animals-lion-1> \n Он считается целеустремленным и активным животным, поэтому этот период будет плодотворным для ^многих^. \n Этот год обещает развитие и повышение по карьерной лестнице — так что ^всё^ в ваших руках! Кстати, по китайскому календарю год начнется первого февраля, а закончится двадцать первого января две тысячи двадцать третьего года. Ну что, путешественник, ^продолжим^ наш путь?"

        buttons = [button('Вперёд!'), button('Завершить путешествие')]
        state = 35 

    elif state == 35:
        ### перепрыгивание на следующее
        if 'да' in list_of_request or 'ок' in list_of_request or 'окей' in list_of_request or 'ага' in list_of_request or 'да' in list_of_request or'давай' in list_of_request or 'следующее' in list_of_request or 'дальше' in list_of_request or 'вперёд' in list_of_request or 'вперед' in list_of_request  or 'хорошо' in list_of_request:
            state = 40

        ### завершение путешествия
        elif 'завершить' in list_of_request or 'заверши'in list_of_request or 'закончи' in list_of_request  or 'хватит' in list_of_request:
            state = 80
        
        elif 'стоп' in list_of_request or 'выход' in list_of_request:
            state = 110

        else:
            message = 'Повторите ещё раз'
            tts = message
            buttons = [button('Вперёд!'), button('Завершить путешествие')]


### Дед мороз в других странах

    if state == 40 and stories:
        story = stories[0] 
        stories.pop(0) 
        message += story
        tts += "Вы наверняка слышали, что почти в каждой стране есть свой Дед мороз. Но самым ^популярным^ из иностранных новогодних волшебников, считается Санта Клаус. \n В отличие от Деда Мороза, он носит совсем короткую красную шубу, подпоясанную черным ремнем, и забавный колпак на голове. \n Живет дедушка в Америке, летает в санях, запряженных оленями, и попадает в дом`а через каминную трубу, через которую и оставляет свои первые подарки. Да и приходит Санта Клаус не в Новый год, а на Рождество, которое в Америке отмечают 25 декабря. \n Хотите узнать о традициях других стран?"

        buttons = [button('Хочу!'), button('Завершить путешествие')]
        state = 45

    elif state == 45:
        ### перепрыгивание на следующее
        if 'хочу' in list_of_request or 'да' in list_of_request or 'ок' in list_of_request or 'окей' in list_of_request or 'ага' in list_of_request or 'давай' in list_of_request or 'следующее' in list_of_request or 'дальше' in list_of_request or 'вперёд' in list_of_request or 'вперед' in list_of_request  or 'хорошо' in list_of_request or 'да' in list_of_request:
            state = 50

        ### завершение путешествия
        elif 'завершить' in list_of_request or 'заверши'in list_of_request or 'закончи' in list_of_request  or 'хватит' in list_of_request:
            state = 80

        elif 'стоп' in list_of_request or 'выход' in list_of_request:
            state = 110

        else:
            message = 'Повторите ещё раз'
            tts = message
            buttons = [button('Только вперёд!'), button('Завершить путешествие')]

### Новый год в других странах

    if state == 50 and stories:
        story = stories[0] 
        stories.pop(0) 
        message += story
        tts += "Перейдём к новогодним традициям разных стран! <speaker audio=marusia-sounds/things-bell-1>\n У жителей Италии в канун Нового года принято выбрасывать всё ненужное. \n Причем избавляются они и от одежды, и мебели, и старой сантехники. \n Правда ^то^, что выкидывают они эти вещи из `окон – всего лишь красивая сказка. \n У японцев вместо боя курантов ровно 108 раз звенят колокола. \n А в Китае по всей стране проходят массовые запуски небесных фонариков! \n Движемся ^дальше^?"

        buttons = [button('Давай дальше!'), button('Завершить путешествие')]
        state = 55

    elif state == 55:
        ### перепрыгивание на следующее
        if 'да' in list_of_request or'ок' in list_of_request or 'окей' in list_of_request or 'ага' in list_of_request or 'давай' in list_of_request or 'следующее' in list_of_request or 'дальше' in list_of_request or 'вперёд' in list_of_request or 'вперед' in list_of_request  or 'хорошо' in list_of_request:
            state = 60

        ### завершение путешествия
        elif 'завершить' in list_of_request or 'заверши'in list_of_request or 'закончи' in list_of_request  or 'хватит' in list_of_request:
            state = 80

        elif 'стоп' in list_of_request or 'выход' in list_of_request:
            state = 110

        else:
            message = 'Повторите ещё раз'
            tts = message
            buttons = [button('Давай дальше!'), button('Завершить путешествие')]


### Новый год в России

    if state == 60 and stories:
        story = stories[0] 
        stories.pop(0) 
        message += story + '\n'
        tts += "О других странах поговорили. А что насчёт русских традиций?\n Большинство стран празднует Новый Год двадцать пятого декабря, в Рождество. Все наши новогодние традиции – вроде ёлки и вкусного ужина – присущи именно Рождеству. А мы больше любим Новый ^год^. \n Тогда почему мы не встречаем его седьмого января? Виной тому реформа большевиков, которым не нравилась религиозная подоплёка праздника.\n Рождество осталось у нас седьмого января, а не в конце декабря, потому, что власти приняли новый календарь, а у церкви остался старый – разница с которым составляет 13 дней. \n Кстати, хотите узнать, почему в России отмечают Старый и Новый год?"

        story = stories[0] 
        stories.pop(0)
        message += story

        buttons = [button('Да!'), button('Завершить путешествие')]
        state = 65

    elif state == 65:
        ### перепрыгивание на следующее
        if 'да' in list_of_request or 'ок' in list_of_request or 'окей' in list_of_request or 'ага' in list_of_request or 'давай' in list_of_request or 'хочу' in list_of_request or 'хотим' in list_of_request or 'вперёд' in list_of_request or 'вперед' in list_of_request or 'хорошо' in list_of_request:
            state = 70

        ### завершение путешествия
        elif 'завершить' in list_of_request or 'заверши'in list_of_request or 'закончи' in list_of_request  or 'хватит' in list_of_request:
            state = 80

        elif 'стоп' in list_of_request or 'выход' in list_of_request:
            state = 110
        
        else:
            message = 'Повторите ещё раз'
            tts = message
            buttons = [button('Да!'), button('Завершить путешествие')]


### Новый и Старый годы

    if state == 70 and stories:
        story = stories[0] 
        stories.pop(0) 
        message += story
        tts += "\n Ещё одна особенность, присущая только ^России^ и странам эсэнгэ –\nСтарый, Новый год! \n Эта удивительная традиция появилась из-за различий в двух календарях. Церковь отмечает новый год по старому стилю. А в России праздники любят. Так что после указа Петра первого, русские с радостью начали отмечать оба праздника, чтобы уж точно соблюсти все традиции. И прижилось. Вот уже 300 лет мы отмечаем оба праздника. \n Мы уже близки к интересному концу! Поднажмём немного?"

        buttons = [button('Вперёд!'), button('Завершить путешествие')]
        state = 75

    elif state == 75:
        ### перепрыгивание на следующее
        if 'да' in list_of_request or 'ок' in list_of_request or 'окей' in list_of_request or 'ага' in list_of_request or 'давай' in list_of_request or 'вперёд' in list_of_request or 'вперед' in list_of_request or 'хорошо' in list_of_request:
            state = 78

        ### завершение путешествия
        elif 'завершить' in list_of_request or 'заверши'in list_of_request or 'закончи' in list_of_request  or 'хватит' in list_of_request:
            state = 80

        elif 'стоп' in list_of_request or 'выход' in list_of_request:
            state = 110
        
        else:
            message = 'Повторите ещё раз'
            tts = message
            buttons = [button('Вперёд!'), button('Завершить путешествие')]
    

### Как строить снеговика

    if state == 78 and stories:
        story = stories[0] 
        stories.pop(0) 
        message += story + '\n'
        tts = "Новый год – это еще и повод вспомнить детство. Если в новогоднюю ночь шёл снег, возможно, сегодня отличный день для того, чтобы слепить снеговика! В свободное время предлагаю пойти на улицу и возвести белого друга! Можно собрать команду – так будет веселее и интереснее. А сейчас держи инструкцию. <speaker audio=marusia-sounds/human-walking-snow-1>  – Шаг первый. \n Для начала нужно дождаться правильного снега. Идеальный снег — влажный, не слишком мокрый и без ледяной корки. Просто скатайте снежок – если он получится крепким и ровным – он нам подходит! \nВторой шаг. Выберите достаточно просторную снежную поляну. Снеговика хорошо бы поставить где-нибудь в теньке. \nШаг третий. Катайте шары, а не цилиндры. Вовремя останавливайте себя — иначе не сможете поднять второй шар на первый, а третий — на второй.  \nИ наконец – четвёртый шаг! Укрепите снеговика пригоршнями снега. \n Верю, что у Вас всё получится! Желаю удачи!"
        # Пегвый шаг
        story = stories[0] 
        stories.pop(0) 
        message += story 
        # Второй шаг
        story = stories[0] 
        stories.pop(0) 
        message += story 
        # Третий шаг
        story = stories[0] 
        stories.pop(0) 
        message += story 
        # Четвёртый шаг
        story = stories[0] 
        stories.pop(0) 
        message += story 

        buttons = [button('Спасибо! Вперёд!'), button('Завершить путешествие')]
        state = 79

    elif state == 79:
        ### перепрыгивание на следующее
        if 'спасибо' in list_of_request or 'ок' in list_of_request or 'окей' in list_of_request or 'ага' in list_of_request or 'давай' in list_of_request or 'следующее' in list_of_request or 'дальше' in list_of_request or 'вперёд' in list_of_request or 'вперед' in list_of_request  or 'хорошо' in list_of_request:
            state = 80

        ### завершение путешествия
        elif 'завершить' in list_of_request or 'заверши'in list_of_request or 'закончи' in list_of_request  or 'хватит' in list_of_request:
            state = 80

        elif 'стоп' in list_of_request or 'выход' in list_of_request:
            state = 110

        else:
            message = 'Повторите ещё раз'
            tts = message
            buttons = [button('Спасибо! Вперёд!'), button('Завершить путешествие')]


### Конец

    if state == 80:
        message = 'Наше путешествие в мир праздника подошло к концу. Хотите загадать желание вместе со мной?'
        tts = '<speaker audio=marusia-sounds/game-win-3> Наше путешествие в мир праздника, подошло к концу. — Хотите загадать ^желание^ вместе со мной?'
        buttons = [button('Да!'), button('Не сейчас')]
        state = 90
    
    elif state == 90:

        if 'ок' in list_of_request or 'окей' in list_of_request or 'ага' in list_of_request or 'да' in list_of_request or 'давай' in list_of_request  or 'хорошо' in list_of_request:
            message = 'Отлично! Тогда приготовьте бумажку и ручку! Можете позвать своих друзей или родных. \nВсё, что вам нужно — это написать желания и цели на следующий год. По окончании соберите ваши желания и запечатайте в конверт до следующего Нового года!'
            tts = "Отлично, \n тогда приготовьте бумажку и ручку! \n Можете позвать своих друзей, или родных. \n Всё, что вам нужно \n это написать желания и цели на 'следующий год. \n По окончании, соберите ваши желания, и запечатайте в конверт до 'следующего нового года!"
            buttons = [button('Готово!'), button('Не сейчас')]
            state = 95
    
        elif 'не' in list_of_request or 'нет' in list_of_request or 'завершить' in list_of_request or 'закончи' in list_of_request or 'закончить' in list_of_request or 'заверши' in list_of_request:
            state = 110

        else:
            message = 'Повторите ещё раз'
            tts = message            
            buttons = [button('Да!'), button('Не сейчас')]
                
    if state == 95:
        if 'написал' in list_of_request or 'написала' in list_of_request or 'написали' in list_of_request or 'готово' in list_of_request or 'сделал' in list_of_request or 'загадал' in list_of_request or 'загадала' in list_of_request or 'загадали' in list_of_request  or 'сделала' in list_of_request or 'сделали' in list_of_request or 'стоп' in list_of_request:
            state = 110 

### Прощание

    if state == 100:
        message = choice(['До новых встреч!', "Рада была встрече!"]) + "\n Проведите день чудесно!"
        tts = message
        end_session = True

### Прощание, если пользователь прочитал хотя бы одну историю

    if state == 110:
        message += choice(["Теперь Вы знаете о празднике немного больше.", "Надеюсь, вам понравилось путешествие.", "Мне было приятно быть Вашим проводником в этом путешествии."]) + choice([' До новых встреч!', " Рада была встрече!"]) + "\nПроведите день чудесно!"
        tts = message
        end_session = True

### Обработка ответов

    response_message = {
        "response": 
        {
            "text": message,
            "tts": tts,
            "buttons": buttons,
            "end_session": end_session
        },
        "session": 
        {
            derived_key: session[derived_key] for derived_key 
            in ['session_id', 'user_id', 'message_id']
        },
            "version": version
    }
    return response_message

### кнопка

def button(title):
    return {"title": title}

async def skill_newyear_journey(request_obj):
    request_message = await request_obj.json()
    response = handler_function(request_message)

    return web.json_response(response)

def init():
    app = web.Application() # создаём приложение и кладём в новую переменную
    app.router.add_post("/skill_newyear_journey", skill_newyear_journey)
    web.run_app(app, host = HOST_IP, port = os.getenv('PORT', 5000))

if __name__ == "__main__":
    init()
