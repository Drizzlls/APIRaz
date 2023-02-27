import pprint
from datetime import datetime
from bitrixTask.classBitrix import Bitrix24DataTgInfoBot


class GetMoney:
    def __init__(self, nickname, chatId):
        self.nickname = nickname
        self.chatId = chatId

    def getUser(self):

        findForChatId = self.getForChatId()
        if findForChatId != False:
            return findForChatId

        findForNickname = self.getForNickname()
        if findForNickname != False:
            return findForNickname

        return 'Ваш аккаунт не идентифицирован в системе. Обратитесь к своему менеджеру для регистрации'
    def getForChatId(self):
        deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.list',
                                                  filter={"CATEGORY_ID": 24, "UF_CRM_63C1194BD233D": self.chatId},
                                                  select=['ID',
                                                          'UF_CRM_1673863435606',
                                                          'UF_CRM_1673863688405',
                                                          'UF_CRM_1674592190066',
                                                          'UF_CRM_63C1194BD233D',
                                                          'UF_CRM_1675757918862'
                                                          ])

        if len(deal) > 0:
            for chat in deal:
                if int(chat['UF_CRM_63C1194BD233D']) == int(self.chatId):
                    if chat['UF_CRM_1675757918862'] == '26016' or chat.get('UF_CRM_1675757918862', None) is None: # Процесс завершен или не заполнен
                        if chat.get('UF_CRM_1673863435606', None) == '25990':  # ФУ
                            updateDeal = deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.update', ID=chat['ID'],
                                                                                   fields={
                                                                                       'UF_CRM_1673863688405': datetime.now().date()
                                                                                   })
                            return 'Ok'
                        elif chat.get('UF_CRM_1673863435606', None) == '25992': # Должник
                            updateDeal = deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.update', ID=chat['ID'],
                                                                                   fields={
                                                                                       'UF_CRM_1674592190066': datetime.now().date()
                                                                                   })
                            return 'Ok'
                        elif chat.get('UF_CRM_1673863435606', None) == '26096': # Нет официального дохода
                            return 'Ошибка запроса , обратитесь к своему сопровождающему'
                        else:
                            return 'Невозможно запросить снятие из-за нехватки данных , обратитесь пожалуйста к Вашему сопровождающему'
                    else:
                        return 'Прошлый процесс снятия не закрыт , обратитесь к своему сопровождающему'
        return False

    def getForNickname(self):
        deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.list',
                                                  filter={"CATEGORY_ID": 24, "UF_CRM_1671012335": self.nickname},
                                                  select=['ID',
                                                      'UF_CRM_1673863435606',
                                                      'UF_CRM_1673863688405',
                                                      'UF_CRM_1674592190066',
                                                      'UF_CRM_1671012335',
                                                      'UF_CRM_1675757918862'
                                                          ])

        if len(deal) > 0:
            for nick in deal:
                if nick.get('UF_CRM_1671012335', None) == self.nickname and self.nickname != 'None':
                    if nick['UF_CRM_1675757918862'] == '26016' or nick.get('UF_CRM_1675757918862', None) is None:  # Процесс завершен
                        if nick.get('UF_CRM_1673863435606', None) == '25990':  # ФУ
                            updateDeal = deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.update', ID=nick['ID'],
                                                                                   fields={
                                                                                       'UF_CRM_1673863688405': datetime.now().date()
                                                                                   })
                            return 'Ok'
                        elif nick.get('UF_CRM_1673863435606', None) == '25992':  # Должник
                            updateDeal = deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.update', ID=nick['ID'],
                                                                                   fields={
                                                                                       'UF_CRM_1674592190066': datetime.now().date()
                                                                                   })
                            return 'Ok'
                        elif nick.get('UF_CRM_1673863435606', None) == '26096': # Нет официального дохода
                            return 'Ошибка запроса , обратитесь к своему сопровождающему'
                        else:
                            return 'Невозможно запросить снятие из-за нехватки данных , обратитесь пожалуйста к Вашему сопровождающему'

                    return 'Прошлый процесс снятия не закрыт , обратитесь к своему сопровождающему'

        return False

