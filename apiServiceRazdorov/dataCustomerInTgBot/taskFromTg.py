from bitrixTask.classBitrix import Bitrix24DataTgInfoBot

class TaskBitrix:
    def __init__(self, chat_id, nickname, text_themes, text_question, id_group):
        self.chat_id = chat_id
        self.nickname = nickname
        self.text_themes = text_themes
        self.text_question = text_question
        self.id_group = id_group

    def getSupportInGroup(self):
        get = Bitrix24DataTgInfoBot.B.callMethod('user.get', FILTER={"UF_DEPARTMENT": self.id_group})
        for employee in get:
            if employee["UF_USR_1669712148259"] == "23148":
                return {"NAME": employee["NAME"],
                        "LAST_NAME":employee["LAST_NAME"],
                        "ID":employee["ID"],}

            elif employee["UF_USR_1669712148259"] == "23152":
                return {"NAME": employee["NAME"],
                        "LAST_NAME":employee["LAST_NAME"],
                        "ID":employee["ID"],}
        return False