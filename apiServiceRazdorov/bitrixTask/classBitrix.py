from bitrix24 import *


class Bitrix24Data:
    WEBHOOK = "https://novoedelo.bitrix24.ru/rest/16/1afcxi0dvbixto70/"
    """ Тестовый """
    # WEBHOOK = "https://novoedelo.bitrix24.ru/rest/16/cpr67qfdl69mk1db/"
    B = Bitrix24(WEBHOOK)

class Bitrix24DataTgBot:
    WEBHOOK = "https://novoedelo.bitrix24.ru/rest/16/rvwbud31d1uqh6hg/"
    B = Bitrix24(WEBHOOK)

class Bitrix24DataTgInfoBot:
    WEBHOOK = "https://novoedelo.bitrix24.ru/rest/16/3y25ftb31s7262ka/"
    B = Bitrix24(WEBHOOK)