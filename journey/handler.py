import json
from random import  choice


def webhook(event, context):
    request_message = json.loads(event['body'])
    response = handler_function(request_message)
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }

stories = [] # Рассказы
state = 0  # Состояния

def handler_function(request):
    global state
    global stories
    buttons = []
    end_session = False
    message = ''
    session = request['session']
    request = request['request']
    list_of_request = request['nlu']['tokens']

    if session['new'] or state == 0:
        with open('steps.txt') as fin:   
            stories = fin.readlines()

### Приветствие
        message = "Привет! \n Новый год - чудесное время года! \n Хотите отправиться в путешествие по этому празднику и узнать о нём больше?"   
        buttons = [button('Да!'), button('Не сейчас')]
        state = 1

### Начало       
    elif state == 1:
        if 'да' in list_of_request or 'хочу' in list_of_request or 'давай' in list_of_request:
            message = choice(['Отлично, поехали!', 'Начинаем путешествие!']) + '\n'
            state = 2

        elif 'не сейчас' in list_of_request or 'нет' in list_of_request or 'не хочу' in list_of_request:
            message = choice(["До новых встреч!", "Пока!", "Рада была встрече!"]) + "\n Проведите день чудесно!"
            end_session = True
            
        else:
            message = 'Поробуйте повторить еще раз'
            buttons = [button('Да!'), button('Не сейчас')]

### Если состояние следующее и путешествие не окончено

### История праздника
    if state == 2 and stories:
        story = stories[0] # запоминаем первый рассказ
        stories.pop(0) # извлекаем его
        message += story # воспроизведение истории
        buttons = [button('Вперёд!'), button('Завершить путешествие')]
        state = 3
        ### перепрыгивание на следующее
        if 'следующее' in list_of_request or 'дальше' in list_of_request or 'вперёд' in list_of_request:
            state = 3
        ### повтор рассказа
        elif 'назад' in list_of_request or 'повтори' in list_of_request or 'ещё раз' in list_of_request:
            state = 2
        ### завершение путешествия
        else:
            state = 8

### Символ года

    elif state == 3 and stories:
        story = stories[0] # запоминаем следующий рассказ
        stories.pop(0) # извлекаем его
        message += story # воспроизведение истории
        buttons = [button('Вперёд!'), button('Завершить путешествие')]
        state = 4 
        ### перепрыгивание на следующее
        if 'следующее' in list_of_request or 'дальше' in list_of_request or 'вперёд' in list_of_request:
            state = 4
        ### повтор рассказа
        elif 'назад' in list_of_request or 'повтори' in list_of_request or 'ещё раз' in list_of_request:
            state = 3
        ### завершение путешествия
        else:
            state = 8

### Новый год в разных странах

    elif state == 4 and stories:
        story = stories[0] # запоминаем следующий рассказ
        stories.pop(0) # извлекаем его
        message += story # воспроизведение истории
        buttons = [button('Вперёд!'), button('Завершить путешествие')]
        state = 4 
        ### перепрыгивание на следующее
        if 'следующее' in list_of_request or 'дальше' in list_of_request or 'вперёд' in list_of_request:
            state = 5
        ### повтор рассказа
        elif 'назад' in list_of_request or 'повтори' in list_of_request or 'ещё раз' in list_of_request:
            state = 4
        ### завершение путешествия
        else:
            state = 8
### 


   

### Конец

    elif state == 8:
        message = 'Наше путешествие в мир праздника подошло к концу. Хотите загадать желание вместе со мной?'
        buttons = [button('Да!'), button('Не сейчас')]
        state = 9
    
    elif state == 9:
        if 'да' in list_of_request or 'хочу' in list_of_request or 'давай' in list_of_request:
            message = 'Отлично, тогда приготовьте бумажку и ручку! \n Можете позвать своих друзей или родных. \n Всё что вам нужно - это написать ваши желания и цели на следующий год. По окончанию соберите ваши желания и запечатайте в конверт до следующего года!'
            buttons = [button('Готово!'), button('Не сейчас')]
            state = 10

        elif 'не сейчас' in list_of_request or 'нет' in list_of_request or 'не хочу' in list_of_request:
            message = choice(["До новых встреч!", "Пока!", "Рада была встрече!"]) + "\n Проведите день чудесно!"
            end_session = True
            
        else:
            message = 'Поробуйте повторить еще раз'
            buttons = [button('Да!'), button('Не сейчас')]


### Прощание
    elif state == 10 or not stories:
        message += '\n'+choice(['До новых встреч!', "Пока!", "Рада была встрече!"]) + "\n Проведите день чудесно!"
        end_session = True

### Обработка ответов
    response_message = {
        "response": 
        {
            "text": message,
            "tts": message,
            "buttons": buttons,
            "end_session": end_session
        },
        "session": 
        {
            derived_key: request['session'][derived_key] for derived_key 
            in ['session_id', 'user_id', 'message_id']
        },
            "version": request['version']
    }
    return response_message

### кнопка
def button(title):
    return {"title": title}

