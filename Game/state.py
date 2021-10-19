
class UserState: # хранение пользовательских состояний

    def __init__(self, request):
        self.session_state = request['state']['session']

    def get_session_state(self):
        return self.session_state

    def save_session_state(self, response):
        response['session_state'] = self.session_state


def get_state(request):
    return UserState