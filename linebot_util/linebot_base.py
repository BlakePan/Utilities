from linebot import LineBotApi
from linebot.models import TextSendMessage


class LineBotBase(object):
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.line_bot_token = 'your token'
        self.user_id_list = ['id for users']
        self.dev_id_list = ['id for dev']
        self.line_bot_api = LineBotApi(self.line_bot_token)

    def get_user_id_list(self, is_debug_msg: bool = False) -> list:
        if self.debug_mode or is_debug_msg:
            return self.dev_id_list
        else:
            return self.user_id_list

    def set_debug_mode(self, debug_mode: bool):
        self.debug_mode = debug_mode

    def push_msg_to_users(self, msg: str, is_debug_msg: bool = False):
        if self.debug_mode or is_debug_msg:
            msg = '[這是演習 別怕]\n' + msg
        self.line_bot_api.multicast(self.get_user_id_list(is_debug_msg=is_debug_msg),
                                    TextSendMessage(text=msg))
