from bitrixTask.classBitrix import Bitrix24DataTgBot as Bitrix24Data

class updateDataBitrix:
    """ Класс занимающийся обновление сущности в Битрикс24 """
    def __init__(self, id, nickname, chatId, date):
        self.nickname = nickname
        self.id = id
        self.chadId = chatId
        self.date = date
        self.fieldLead = {
            'UF_CRM_1673529241': self.nickname,
            'UF_CRM_1673599207' : self.chadId,
            'UF_CRM_1674131222' : self.date,
        }
        self.fieldDeal = {
            'UF_CRM_1671012335': self.nickname,
            'UF_CRM_63C1194BD233D': self.chadId,
            'UF_CRM_63C93A55437A5' : self.date,
        }
        self.essence = ''


    def defineEssence(self) -> str:
        """ Определям сущность по id """
        try:
            get = Bitrix24Data.B.callMethod('crm.deal.get', ID=self.id)
            self.essence = 'deal'
        except:
            get = Bitrix24Data.B.callMethod('crm.lead.get', ID=self.id)
            self.essence = 'lead'
        return self.essence


    def updateDealOrLead(self):
        """ Обновляем сущность """
        try:
            if self.essence == "lead":
                update = Bitrix24Data.B.callMethod(f'crm.{self.essence}.update', ID=self.id,
                                                   fields=self.fieldLead)
            else:
                update = Bitrix24Data.B.callMethod(f'crm.{self.essence}.update', ID=self.id,
                                                   fields=self.fieldDeal)
            return True
        except Exception as e:
            return e

    def __call__(self, *args, **kwargs):
        self.defineEssence()
        self.updateDealOrLead()
        return True

