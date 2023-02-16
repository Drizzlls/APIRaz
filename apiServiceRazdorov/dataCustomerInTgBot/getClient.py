from bitrixTask.classBitrix import Bitrix24DataTgBot as Bitrix24Data
import pprint
from .models import AllManagers, SourceDeal, SourceLead


"""
1) ФИО
2) Номер телефона
3) Менеджер
4) Группа
5) Дата заключения - UF_CRM_62DAB2BE1B9C0
6) Номер дела
7) Источник
"""
class GetClientClass:
    def __init__(self, nickname):
        self.nickname = nickname
        self.sourceId = {
            ""
        }
        # Стадии
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
        self.recognized = ["C24:UC_NTWW9M", "C24:UC_E87W9B", "C24:2", "C24:3", "C24:4", "C24:5", "C24:6", "C24:7",
                           "C24:UC_6ZM2T2", "C24:WON"]


    def defineEntity(self):
        deal = Bitrix24Data.B.callMethod('crm.deal.list',filter={"UF_CRM_1671012335": self.nickname}, select=['CONTACT_ID','ASSIGNED_BY_ID','UF_CRM_62DAB2BE1B9C0','UF_CRM_6059A855ED8BE','UF_CRM_5F3BE0484AC8C','STAGE_ID','UF_CRM_1671012335','CATEGORY_ID','UF_CRM_1674476382','UF_CRM_1669542261','STAGE_ID'])
        if deal != []:
            return self.getDeal(deal),
        lead = Bitrix24Data.B.callMethod('crm.lead.list',filter={"UF_CRM_1673529241": self.nickname},select=['ID','ASSIGNED_BY_ID','UF_CRM_1597759307071','NAME','LAST_NAME','SECOND_NAME'])
        if lead != []:
            return self.getLead(lead)
        return 'Такого никнейма нет в Битриксе'


    def getLead(self,data):
        """ Получаем лид """
        return {
            'Тип сущности': 'Лид',
            'ID': data[0]['ID'],
            'Ответственный': self.getManager(data[0]['ASSIGNED_BY_ID']),
            'Группа': self.getGroup(id=data[0]['ASSIGNED_BY_ID']),
            'Источник': self.getSource(data[0]['UF_CRM_1597759307071'],entity='lead'),
            'Имя клиента': data[0]['NAME'],
            'Фамилия клиента': data[0]['LAST_NAME'],
            'Отчество клиента': data[0]['SECOND_NAME'],
                }

    def getDeal(self, data):
        """ Получаем сделку """
        if len(data) > 1:
            for deal in data:
                if deal["UF_CRM_1671012335"] != self.nickname:
                    data.remove(deal)
                    continue
                if deal['STAGE_ID'] == 'C14:WON' or deal['CATEGORY_ID'] == '0':
                    data.remove(deal)
        contact = self.getContact(data[0]['CONTACT_ID'])
        return {
            'Тип': 'Сделка',
            'ID': data[0]['ID'],
            'Ответственный': self.getManager(data[0]['ASSIGNED_BY_ID']),
            'Группа': self.getGroup(data[0]['UF_CRM_1669542261']) if data[0]['UF_CRM_1669542261'] else 'Руководитель не заполнен',
            'Дата заключения договора':data[0]['UF_CRM_62DAB2BE1B9C0'][:-15] if data[0]['UF_CRM_62DAB2BE1B9C0'] else 'Нет',
            'Номер дела':data[0]['UF_CRM_6059A855ED8BE'] if data[0]['UF_CRM_6059A855ED8BE'] else 'Нет',
            'Источник': self.getSource(id=data[0]['UF_CRM_5F3BE0484AC8C'],entity='deal'),
            'Имя клиента':contact['NAME'],
            'Фамилия клиента':contact['LAST_NAME'],
            'Отчество клиента':contact['SECOND_NAME'],
            'Признан': 'Да' if data[0]["STAGE_ID"] in self.recognized else 'Нет',
            'Номер телефона клиента': contact['PHONE'][0]['VALUE'],
            'Стадия' : self.stage.get(data[0]["STAGE_ID"], 'Стадии нет в базе'),

            }


    def getContact(self, id):
        """ Получаем контакт """
        contact = Bitrix24Data.B.callMethod('crm.contact.get', id=id)
        return {'NAME': contact['NAME'] if contact.get('NAME', None) is not None else '',
                'LAST_NAME':contact['LAST_NAME'] if contact.get('LAST_NAME', None) is not None else '',
                'SECOND_NAME':contact['SECOND_NAME'] if contact.get('SECOND_NAME', None) is not None else '',
                'PHONE':contact['PHONE'] if contact.get('PHONE', None) is not None else ''}

    def getManager(self, id):
        try:
            manager = AllManagers.objects.get(idManager=id).name
            return manager
        except:
            return id

    def getSource(self, id, entity):
        """ Определяем источник в сущности """
        if entity == 'lead':
            try:
                source = SourceLead.objects.get(idFromBitrix=id).title
                return source
            except:
                return id
        else:
            try:
                source = SourceDeal.objects.get(idFromBitrix=id).title
                return source
            except:
                return id

    def getGroup(self, id):
        """ Определяем группу """
        departamentManager = Bitrix24Data.B.callMethod('user.get', id=id)
        dictGroup = {
            80: 'Носуля',
            82: 'Власенко',
            84: 'Саркисян',
            88: 'Арсеньев',
            90: 'Шмелев'
        }
        for group in departamentManager[0]['UF_DEPARTMENT']:
            if group in dictGroup.keys():
                return dictGroup[group]
        return 'Сотрудник вне рабочей группы'
