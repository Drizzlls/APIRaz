import pprint
from datetime import datetime
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
        # ID Стадии : Поле со временем
        self.stageTime = {
            'C24:NEW':'UF_CRM_1670399665',
            "C24:PREPARATION": "UF_CRM_1670399693",
            "C24:PREPAYMENT_INVOIC": "UF_CRM_1670399713",
            "C24:EXECUTING": "UF_CRM_1670399774",
            "C24:FINAL_INVOICE": "UF_CRM_1670399843",
            "C24:UC_F2L1SR": "UF_CRM_1670399820",
            "C24:UC_NKXZUI": "UF_CRM_1670399839",
            "C24:UC_ISRMKZ": "UF_CRM_1670399868",
            "C24:UC_C5N1HC": "UF_CRM_1670399888",
            "C24:UC_S0SWZ1": "UF_CRM_1670399907",
            "C24:UC_QTVVI8": "UF_CRM_1670400084",
            "C24:UC_F4Z4L7": "UF_CRM_1670400575",
            "C24:UC_NTWW9M": "UF_CRM_1676540354",
            "C24:UC_E87W9B": "UF_CRM_1676540459",
            "C24:2": "UF_CRM_1676540501",
            "C24:3": "UF_CRM_1676540582",
            "C24:4": "UF_CRM_1676541162",
            "C24:5": "UF_CRM_1676541291",
            "C24:6": "UF_CRM_1676541316",
            "C24:7": "UF_CRM_1676541349",
            "C24:UC_6ZM2T2": "UF_CRM_1676541384",
            "C24:UC_SR23DP": "UF_CRM_1676541413",
            "C24:UC_RHCPBY": "UF_CRM_1676541441",
            "C24:WON": "UF_CRM_1670400958",

        }
        # Признанные
        self.recognized = ["C24:UC_NTWW9M","C24:UC_E87W9B","C24:2","C24:3","C24:4","C24:5","C24:6","C24:7", "C24:UC_6ZM2T2", "C24:WON"]
        self.financeManager = {
            '54': 'Суслов',
            '56': 'Барабаш',
            '58': 'Попов',
            '698': 'Проноза',
            '786': 'Микуцкий',
            '23936': 'Ковалев/Бубенцова',
            '23938': 'Суховерхов',
            '23940': 'Кавокин',
            '26048': 'Шаронова',
            '26050': 'Усова',
            '26052': 'Самойлов',
            '26054': 'Савлучинский',
            '26056': 'Холостова',
            '26058': 'Ильин',
            '26060': 'Терентьев',
            '26062': 'Асаинов',
            '':'',
            None: ''
        }

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
                                                          'UF_CRM_63C1194BD233D',
                                                          'ASSIGNED_BY_ID',
                                                          'UF_CRM_1671012335',
                                                          'UF_CRM_1670399797',
                                                          *self.stageTime.values(),
                                                          'TITLE',
                                                          'UF_CRM_1560419829978'
                                                          ])
        if len(deal) > 0:
            for chat in deal:
                if int(chat['UF_CRM_63C1194BD233D']) == int(self.chatId):
                    manager = self.getUser(deal[0]['ASSIGNED_BY_ID'])
                    leader = self.getUser(deal[0]['UF_CRM_1669542261'])
                    support = self.getUser(deal[0]['UF_CRM_1668595139'])
                    return {
                            "ФИО": deal[0]['TITLE'],
                            "Дата заседания" : deal[0]["UF_CRM_1672350461848"] if deal[0]["UF_CRM_1672350461848"] else 'Пока нет',
                            "Дата признания банкротом" : deal[0]["UF_CRM_1674476382"] if deal[0]["UF_CRM_1674476382"] else 'Пока нет',
                            "№ дела" : deal[0]["UF_CRM_6059A855ED8BE"] if deal[0]["UF_CRM_6059A855ED8BE"] else 'Пока нет',
                            "Стадия дела" : self.stage.get(deal[0]["STAGE_ID"], 'В работе'),
                        'Дней нахождения в стадии': (datetime.strptime(str(datetime.now().date()),
                                                                       "%Y-%m-%d") - datetime.strptime(
                            deal[0][self.timeInStage(deal[0]["STAGE_ID"])][0:10], "%Y-%m-%d")).days + 1 if deal[0][self.timeInStage(deal[0]["STAGE_ID"])][0:10] != '' else '0',

                        "Признание банкротом" : 'Да' if deal[0]["STAGE_ID"] in self.recognized else 'Нет',
                            "Руководитель группы": f'{leader["name"]} {leader["last_name"]}',
                            "Рабочий номер руководителя": leader["phone"],
                            "Ответственный менеджер" : f'{manager["name"]} {manager["last_name"]}',
                            "Рабочий номер менеджера" : manager["phone"],
                            "Сотрудник поддержки": f'{support["name"]} {support["last_name"]}',
                            "Рабочий номер поддержки": support["phone"],
                            "Операционный директор": 'Бабаков Данил Алексеевич',
                            "Рабочий номер Операционного директора": "89604616785",
                        'Финансовый управляющий': self.financeManager[deal[0]["UF_CRM_1560419829978"]]
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
                                                          'UF_CRM_63C1194BD233D',
                                                          'ASSIGNED_BY_ID',
                                                          'UF_CRM_1671012335',
                                                          'UF_CRM_1670399797',
                                                          *self.stageTime.values(),
                                                          'TITLE',
                                                          'UF_CRM_1560419829978'
                                                          ])

        # print(deal)
        if len(deal) > 0:
            for nick in deal:
                if nick.get('UF_CRM_1671012335',None) == self.nickname and self.nickname != 'None':
                    manager = self.getUser(deal[0]['ASSIGNED_BY_ID'])
                    leader = self.getUser(deal[0]['UF_CRM_1669542261'])
                    support = self.getUser(deal[0]['UF_CRM_1668595139'])
                    return {
                        "ФИО": deal[0]['TITLE'],
                        "Дата заседания": deal[0]["UF_CRM_1672350461848"] if deal[0]["UF_CRM_1672350461848"] else 'Пока нет',
                        "Дата признания банкротом": deal[0]["UF_CRM_1674476382"] if deal[0]["UF_CRM_1674476382"] else 'Пока нет',
                        "№ дела": deal[0]["UF_CRM_6059A855ED8BE"] if deal[0]["UF_CRM_6059A855ED8BE"] else 'Пока нет',
                        "Стадия дела": self.stage.get(deal[0]["STAGE_ID"], 'В работе'),
                        'Дней нахождения в стадии': (datetime.strptime(str(datetime.now().date()),
                                                                       "%Y-%m-%d") - datetime.strptime(
                            deal[0][self.timeInStage(deal[0]["STAGE_ID"])][0:10], "%Y-%m-%d")).days + 1 if deal[0][self.timeInStage(deal[0]["STAGE_ID"])][0:10] != '' else '0',

                        "Признание банкротом": 'Да' if deal[0]["STAGE_ID"] in self.recognized else 'Нет',
                        "Руководитель группы": f'{leader["name"]} {leader["last_name"]}',
                        "Рабочий номер руководителя": leader["phone"],
                        "Ответственный менеджер": f'{manager["name"]} {manager["last_name"]}',
                        "Рабочий номер менеджера": manager["phone"],
                        "Сотрудник поддержки": f'{support["name"]} {support["last_name"]}',
                        "Рабочий номер поддержки": support["phone"],
                        "Операционный директор": 'Бабаков Данил Алексеевич',
                        "Рабочий номер Операционного директора": "89604616785",
                        'Финансовый управляющий': self.financeManager[deal[0]["UF_CRM_1560419829978"]]
                    }

        return 'Ваш аккаунт не идентифицирован в системе. Обратитесь к своему менеджеру для регистрации'

    def getUser(self, idManager):
        user = Bitrix24DataTgInfoBot.B.callMethod('user.get', ID=idManager)
        if user == []:
            return {
                'phone': '',
                'name': '',
                'last_name': ''
            }
        return {
            'phone': user[0]['WORK_PHONE'],
            'name' : user[0]['NAME'],
            'last_name' : user[0]['LAST_NAME']
        }

    def timeInStage(self, id):
        return self.stageTime.get(id , None)

    def getLinkEducation(self):
        deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.list',
                                                  filter={"CATEGORY_ID": 24, "UF_CRM_63C1194BD233D": self.chatId},
                                                  select=['UF_CRM_1666347597'])

        if len(deal) > 0:

            return {'Персональная ссылка на обучение': deal[0]["UF_CRM_1666347597"]}

        deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.list',
                                                  filter={"CATEGORY_ID": 24, "UF_CRM_1671012335": self.nickname},
                                                  select=['UF_CRM_1666347597'])
        if len(deal) > 0:

            return {'Персональная ссылка на обучение': deal[0]["UF_CRM_1666347597"]}

        return 'Ваш аккаунт не идентифицирован в системе. Обратитесь к своему менеджеру для регистрации'
