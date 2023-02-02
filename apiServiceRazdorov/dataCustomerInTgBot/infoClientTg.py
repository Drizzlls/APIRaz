from bitrixTask.classBitrix import Bitrix24DataTgInfoBot


class InfoBotMethods:

    @staticmethod
    def getNickname(nickname,chatId):
        if nickname != 'None' or nickname not in None:
            deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.list', filter={"CATEGORY_ID":24,"UF_CRM_1671012335":nickname}, select=['UF_CRM_1674476382',
                                                                                                                                      'UF_CRM_1672350461848',
                                                                                                                                      'UF_CRM_6059A855ED8BE',])
        else:
            deal = Bitrix24DataTgInfoBot.B.callMethod('crm.deal.list',
                                                      filter={"CATEGORY_ID": 24, "UF_CRM_1671012335": nickname},
                                                      select=['UF_CRM_1674476382',
                                                              'UF_CRM_1672350461848',
                                                              'UF_CRM_6059A855ED8BE',])

"""

До заседания — НЕ ПРИЗНАН
После заседания — ПРИЗНАН

"""
  
