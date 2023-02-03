from bitrixTask.classBitrix import Bitrix24DataTgBot as Bitrix24Data
from random import randint
import pprint


class CurrentClient:
    """ Класс занимающийся обработкой данных """
    def __init__(self, idDeal, idManager, nickname, chatId):
        self.idDeal = idDeal
        self.idManager = idManager
        self.nickname = nickname
        self.chatId = chatId
        self.allUsersData = self.allUsers()
        self.dictDepartament = [80, 82, 84, 88, 90]

    def allUsers(self):
        """ Получаем все данные сотрудников """
        getAllUsers = Bitrix24Data.B.callMethod('user.search')
        return getAllUsers

    def getLinkTelegramManager(self):
        """ Получаем Рабочий Telegram канал сотрудника """
        for user in self.allUsersData:
            if int(user['ID']) == int(self.idManager):
                if user.get('UF_USR_1672311069106',None):
                    return user['UF_USR_1672311069106']
        return self.getLinkTelegramSubdivision()

    def getSubdivisionManager(self):
        """ Получаем подрозделение сотрудника """
        truesubdivision = ''
        for user in self.allUsersData:
            if user['ID'] == str(self.idManager):
                if self.trueDepartament(user['UF_DEPARTMENT']) in self.dictDepartament:
                    return self.trueDepartament(user['UF_DEPARTMENT'])
        return self.randLink()

    def getLinkTelegramSubdivision(self):
        """ Получаем ссылку на тг канал, если у ответственного менеджера своего канала нет """
        division = self.getSubdivisionManager()
        if isinstance(division, int):
            for user in self.allUsersData:
                if division in user['UF_DEPARTMENT']:
                    if user['UF_USR_1672311069106']:
                        return user['UF_USR_1672311069106']
        else:
            return division

    def trueDepartament(self, listDepartament: list):
        """ Определяем нужный департамент """
        for departament in listDepartament:
            if departament in self.dictDepartament:
                return departament
        return False

    def randLink(self):
        """ Получаем рандомные ссылки """
        allLink = []
        for link in self.allUsersData:
            if link['UF_USR_1672311069106']:
                allLink.append(link['UF_USR_1672311069106'])
        return allLink[randint(0, len(allLink)-1)]



