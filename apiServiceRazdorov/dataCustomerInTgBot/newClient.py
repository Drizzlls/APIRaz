import pprint
from bitrixTask.classBitrix import Bitrix24DataTgBot as Bitrix24Data
from .currentСlient import CurrentClient
import time
import datetime


class AddNewClient:
    def __init__(self, nickname, chatId, phone, idGroup, last_name, first_name, utm):
        self.nickname = nickname
        self.chatId = chatId
        self.phone = phone
        self.idGroup = idGroup
        self.allUserInGroup = self.allUserInGroup()
        self.link = ''
        self.idManager = ''
        self.last_name = last_name
        self.first_name = first_name
        self.utm = utm

    def findNickname(self):
        """ Осуществляем поиск по никнейму """
        deal = self.findNicknameInDeal()
        if len(deal) > 0:
            client = CurrentClient(idDeal=deal[0]['ID'], idManager=deal[0]['ASSIGNED_BY_ID'], nickname=self.nickname,
                                   chatId=self.chatId)
            return client.getLinkTelegramManager()

        time.sleep(1)
        lead = self.findNicknameInLead()
        if len(lead) > 0:
            client = CurrentClient(idDeal=lead[0]['ID'], idManager=lead[0]['ASSIGNED_BY_ID'], nickname=self.nickname, chatId=self.chatId)
            return client.getLinkTelegramManager()

        else:
            return False

    def findNicknameInDeal(self):
        """ Поиск в сделках """
        print('Смотрю в сделках')
        findDeal = Bitrix24Data.B.callMethod('crm.deal.list',
                                                     filter={'UF_CRM_63C1194BD233D': self.chatId})
        pprint.pprint(f"Сделки — {findDeal}")
        return findDeal

    def findNicknameInLead(self):
        """ Поиск в лидах """
        print('Смотрю в лидах')
        findLead = Bitrix24Data.B.callMethod('crm.lead.list',filter={'UF_CRM_1673599207':self.chatId})
        pprint.pprint(f"Лиды — {findLead}")
        return findLead

    def getLinkGroup(self):
        """ Получаем ссылку сотрудника из группы """
        for user in self.allUserInGroup:
            print(user["LAST_NAME"])
            if user["UF_USR_1672311069106"]:
                self.link = user["UF_USR_1672311069106"]
                self.idManager = user["ID"]
                return {"link": self.link, "idManager": self.idManager}
        return False

    def allUserInGroup(self):
        """ Получаем список сотрудников в рабочей группе """
        allUsers = Bitrix24Data.B.callMethod('user.search',FILTER={"UF_DEPARTMENT":self.idGroup})
        return allUsers

    def addLead(self):
        """ Создаем новый лид """
        add = Bitrix24Data.B.callMethod('crm.lead.add', fields = {
            "TITLE" : "Новый подписчик в чате",
            "PHONE": [{"VALUE": self.phone, "VALUE_TYPE": "WORK"}],
            "UF_CRM_1673529241" : self.nickname,
            "UF_CRM_1673599207": self.chatId,
            "ASSIGNED_BY_ID" : self.idManager,
            "NAME": self.first_name,
            "LAST_NAME" : self.last_name,
            "UF_CRM_1674131222": datetime.datetime.now(),
            "UTM_SOURCE": self.utm,
        })
        return True

    def __call__(self, *args, **kwargs):
        self.getLinkGroup()
        self.addLead()
        return True


