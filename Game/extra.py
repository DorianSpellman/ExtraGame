from question import *
registred_states = {}

def get_state(state_id):
    return registred_states[state_id]

def get_root_state():
    global root_state_id
    return registred_states[root_state_id]

class Transition: # переходы между состояниями

    def __init__(self, to_id, synonims):
        self.to_id = to_id
        self.synonims = synonims

    def must_go(self, user_text):
        return user_text in self.synonims # ввод пользователя и поиск в списке синонимов
    
    def get_dest_id(self):
        return self.to_id

class State: # состояния

    def __init__(self, id, text, transitions, defoult_transition, is_end = False):
        self.id = id
        self.text = text
        self.transitions = transitions
        self.defoult_transition = defoult_transition
        self.is_end = is_end

    def get_next_state(self, user_input):
        for transition in self.transition:
            if transition.must_go(user_input):
                return get_state(transition.to_id)
        return get_state(self.defoult_transition)

    def register(self):
        global registred_states
        registred_states[self.id] = self

    def get_text(self):
        return self.text

    def get_id(self):
        return self.id

    def is_end_state(self):
        return self.is_end()

       
def init():
    global root_state_id # корневое состяние

    State('100', "Привет! Всё предельно просто: \n на выбор тебе будет дано несколько слов \n – твоя задача, \n выбрать из них лишнее. \n Начнём игру!",
     [Transition('900', ['нет', 'не хочу', 'назад', 'отмена'])], '101').register()

    State('101', "Начинаем",
     [Transition('900', ['нет', 'не хочу', 'назад', 'отмена'])], None, True).register()

    # for QA in que_ans:
    #     a = input(QA.que)
    #     Transition('900', ["стоп", "отмена", "завершить", "заверши игру"])
    #     if a == QA.ans[0] or a == QA.ans[1] or a == QA.ans[2]:
    #          print('Верно! ' + str(QA.explanation))
    #     else:
    #          print("Неверно! " + str(QA.explanation))

    State('900', "До новых встреч!", [], None, True)

    root_state_id ='100'

init()

