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
                                                          'UF_CRM_1675757918862',
                                                          'UF_CRM_1677314961482',
                                                          'UF_CRM_1677314971866'
                                                          ])

        if len(deal) > 0:
            for chat in deal:
                if int(chat['UF_CRM_63C1194BD233D']) == int(self.chatId):
                    if chat['UF_CRM_1675757918862'] not in [None, '26016']:
                        return 'Прошлый процесс снятия не закрыт , обратитесь к своему сопровождающему' # Процесс завершен или не заполнен
                    if self.getRequisites(chat): # Процесс завершен или не заполнен
                        if chat.get('UF_CRM_1673863435606', None) == '25990':  # ФУ
                            updateDeal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.update', ID=chat['ID'],
                                                                                       fields={
                                                                                           'UF_CRM_1673863688405': datetime.now().date()
                                                                                       })
                            startProcess = self.startBusinessProcess(chat['ID'])

                            return 'Ok'
                        elif chat.get('UF_CRM_1673863435606', None) == '25992': # Должник
                            updateDeal = deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.update', ID=chat['ID'],
                                                                                       fields={
                                                                                           'UF_CRM_1674592190066': datetime.now().date()
                                                                                       })
                            startProcess = self.startBusinessProcess(chat['ID'])

                            return 'Ok'
                        elif chat.get('UF_CRM_1673863435606', None) == '26096': # Нет официального дохода
                            return 'Ошибка запроса , обратитесь к своему сопровождающему'
                        else:
                            return 'Невозможно запросить снятие из-за нехватки данных, обратитесь, пожалуйста, к Вашему сопровождающему'
                    else:
                        return 'Невозможно запросить снятие из-за нехватки данных, обратитесь, пожалуйста, к Вашему сопровождающему'  # Процесс завершен или не заполнен
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
                                                          'UF_CRM_63C1194BD233D',
                                                          'UF_CRM_1675757918862',
                                                          'UF_CRM_1677314961482',
                                                          'UF_CRM_1677314971866'
                                                          ])

        if len(deal) > 0:
            for nick in deal:
                if int(nick['UF_CRM_63C1194BD233D']) == int(self.nick):
                    if nick['UF_CRM_1675757918862'] not in [None, '26016']:
                        return 'Прошлый процесс снятия не закрыт , обратитесь к своему сопровождающему' # Процесс завершен или не заполнен
                    if self.getRequisites(nick): # Процесс завершен или не заполнен
                        if nick.get('UF_CRM_1673863435606', None) == '25990':  # ФУ
                            updateDeal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.update', ID=nick['ID'],
                                                                                       fields={
                                                                                           'UF_CRM_1673863688405': datetime.now().date()
                                                                                       })
                            startProcess = self.startBusinessProcess(chat['ID'])

                            return 'Ok'
                        elif nick.get('UF_CRM_1673863435606', None) == '25992': # Должник
                            updateDeal = deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.update', ID=nick['ID'],
                                                                                       fields={
                                                                                           'UF_CRM_1674592190066': datetime.now().date()
                                                                                       })
                            startProcess = self.startBusinessProcess(nick['ID'])

                            return 'Ok'
                        elif nick.get('UF_CRM_1673863435606', None) == '26096': # Нет официального дохода
                            return 'Ошибка запроса , обратитесь к своему сопровождающему'
                        else:
                            return 'Невозможно запросить снятие из-за нехватки данных, обратитесь, пожалуйста, к Вашему сопровождающему'
                    else:
                        return 'Невозможно запросить снятие из-за нехватки данных, обратитесь, пожалуйста, к Вашему сопровождающему'  # Процесс завершен или не заполнен
                else:
                    return 'Прошлый процесс снятия не закрыт , обратитесь к своему сопровождающему'
        return False


    def startBusinessProcess(self, id):
        start = Bitrix24DataTgInfoBot.B.callMethod('bizproc.workflow.start', TEMPLATE_ID=1056,
                                                   DOCUMENT_ID=['crm', 'CCrmDocumentDeal', id])
        return 'Процесс выполнен'

    def getRequisites(self, data):
        print(data['UF_CRM_1677314961482'])
        print(data['UF_CRM_1677314971866'])
        print(data['UF_CRM_1675757918862'])
        if data.get('UF_CRM_1677314961482', None) or data.get('UF_CRM_1677314971866', None)!=[]:
            return True
        else:
            return False