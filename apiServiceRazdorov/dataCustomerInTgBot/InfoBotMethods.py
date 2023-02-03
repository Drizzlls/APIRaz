from bitrixTask.classBitrix import Bitrix24DataTgInfoBot


class InfoBotMethods:
    def __init__(self, nickname, chatId):
        self.nickname = nickname
        self.chatId = chatId
        self.stage = {
        "C24:NEW": "Знакомство",
        "C24:PREPARATION": "Первый пакет",
        "C24:PREPAYMENT_INVOIC": "Проверка",
        "C24:EXECUTING": "Возвращен на доработку",
        "C24:FINAL_INVOICE": "Взят в работу юристами",
        "C24:UC_F2L1SR": "Передать на сбор",
        "C24:UC_NKXZUI": "Сбор",
        "C24:UC_ISRMKZ": "Получить депозит",
        "C24:UC_C5N1HC": "Написание искового",
        "C24:UC_S0SWZ1": "Отправить в суд",
        "C24:UC_QTVVI8": "Назначение даты",
        "C24:UC_F4Z4L7": "Заседание",
        "C24:UC_NTWW9M": "Реструктуризация долгов",
        "C24:UC_E87W9B": "Получение документов",
        "C24:2": "Собрание кредиторов",
        "C24:3": "Судебное заседание",
        "C24:4": "Реализация имущества",
        "C24:5": "Получение документов",
        "C24:6": "Торги",
        "C24:7": "Судебное заседание",
        "C24:UC_6ZM2T2": "Завершение",
        "C24:UC_SR23DP": "Заморозка",
        "C24:UC_RHCPBY": "Анализ",
        "C24:APOLOGY": "Анализ причины провала",
        "C24:1": "Расторжение",
        "C24:WON": "Сделка успешна",
    }
        # Признанные
        self.recognized = ["C24:UC_NTWW9M","C24:UC_E87W9B","C24:2","C24:3","C24:4","C24:5","C24:6","C24:7", "C24:UC_6ZM2T2", "C24:WON"]

    def getNickname(self):
        deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.list',
                                                  filter={"CATEGORY_ID": 24, "UF_CRM_63C1194BD233D": self.chatId},
                                                  select=['UF_CRM_1672350461848',
                                                          'UF_CRM_1674476382',
                                                          'UF_CRM_6059A855ED8BE',
                                                          'STAGE_ID',
                                                          'UF_CRM_1669542261',
                                                          'ASSIGNED_BY_ID',
                                                          'UF_CRM_1668595139',
                                                          ])
        if len(deal) > 0:
            manager = self.getUser(deal[0]['ASSIGNED_BY_ID'])
            leader = self.getUser(deal[0]['UF_CRM_1669542261'])
            support = self.getUser(deal[0]['UF_CRM_1668595139'])
            return {
                    "Дата заседания" : deal[0]["UF_CRM_1672350461848"] if deal[0]["UF_CRM_1672350461848"] else 'Пока нет',
                    "Дата признания банкротом" : deal[0]["UF_CRM_1674476382"] if deal[0]["UF_CRM_1674476382"] else 'Пока нет',
                    "№ дела" : deal[0]["UF_CRM_6059A855ED8BE"] if deal[0]["UF_CRM_6059A855ED8BE"] else 'Пока нет',
                    "Стадия дела" : self.stage.get(deal[0]["STAGE_ID"],'В работе'),
                    "Признание банкротом" : 'Да' if deal[0]["STAGE_ID"] in self.recognized else 'Нет',
                    "Руководитель группы": f'{leader["name"]} {leader["last_name"]}',
                    "Рабочий номер руководителя": leader["phone"],
                    "Ответственный менеджер" : f'{manager["name"]} {manager["last_name"]}',
                    "Рабочий номер менеджера" : manager["phone"],
                    "Сотрудник поддержки": f'{support["name"]} {support["last_name"]}',
                    "Рабочий номер поддержки": support["phone"]
            }

        deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.list',
                                                  filter={"CATEGORY_ID": 24, "UF_CRM_1671012335": self.nickname},
                                                  select=['UF_CRM_1672350461848',
                                                          'UF_CRM_1674476382',
                                                          'UF_CRM_6059A855ED8BE',
                                                          'STAGE_ID',
                                                          'UF_CRM_1669542261',
                                                          'ASSIGNED_BY_ID',
                                                          'UF_CRM_1668595139',
                                                          ])
        if len(deal) > 0:
            manager = self.getUser(deal[0]['ASSIGNED_BY_ID'])
            leader = self.getUser(deal[0]['UF_CRM_1669542261'])
            support = self.getUser(deal[0]['UF_CRM_1668595139'])
            return {
                "Дата заседания": deal[0]["UF_CRM_1672350461848"] if deal[0]["UF_CRM_1672350461848"] else 'Пока нет',
                "Дата признания банкротом": deal[0]["UF_CRM_1674476382"] if deal[0]["UF_CRM_1674476382"] else 'Пока нет',
                "№ дела": deal[0]["UF_CRM_6059A855ED8BE"] if deal[0]["UF_CRM_6059A855ED8BE"] else 'Пока нет',
                "Стадия дела": self.stage.get(deal[0]["STAGE_ID"], 'В работе'),
                "Признание банкротом": 'Да' if deal[0]["STAGE_ID"] in self.recognized else 'Нет',
                "Руководитель группы": f'{leader["name"]} {leader["last_name"]}',
                "Рабочий номер руководителя": leader["phone"],
                "Ответственный менеджер": f'{manager["name"]} {manager["last_name"]}',
                "Рабочий номер менеджера": manager["phone"],
                "Сотрудник поддержки": f'{support["name"]} {support["last_name"]}',
                "Рабочий номер поддержки": support["phone"]
            }

        return 'Ваш аккаунт не идентифицирован в системе. Обратитесь к своему менеджеру для регистрации'

    def getUser(self, idManager):
        user = Bitrix24DataTgInfoBot.B.callMethod('user.get',ID=idManager)
        return {
            'phone': user[0]['WORK_PHONE'],
            'name' : user[0]['NAME'],
            'last_name' : user[0]['LAST_NAME']
        }
