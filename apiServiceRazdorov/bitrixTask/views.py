import pprint
from datetime import datetime, timedelta, timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .classBitrix import Bitrix24Data
import json
from .serializers import TgBotDataSerializer
from pytz import timezone



class TaskAPIView(APIView):

    def post(self,request):
        serializer = TgBotDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Определение менеджера
        manager = TreatmentData.getIdManager(id=request.data['idManager'])
        if manager == False:
            return Response({'Ошибка':'Такого менеджера нет в битриксе!'})

        # Определение департамента
        subdivision = TreatmentData.getSubdivision(manager)
        if subdivision == False:
            return Response({'Ошибка' : 'Департамент не найден!'})

        # Определение саппорта
        support = TreatmentData.getSupport(subdivision)
        if support == False:
            return Response({'Ошибка' : 'Саппорт не найден!'})

        # Определение старшего группы
        groupLeader = TreatmentData.getGroupLeader(subdivision)

        #Постановка задачи
        task = TreatmentData.addTask(idSupport=support, idCategory=request.data["category"], message=request.data["message"],client=request.data["nickname"],groupLeader=groupLeader)
        return Response({'ok':'ok!'})



class TreatmentData:
    dictDepartament = [80, 82, 84, 88, 90]
    @staticmethod
    def getIdManager(id):
        """ Получаем ID сотрудника """
        get = Bitrix24Data.B.callMethod('user.get',ID=id)
        return False if get == [] else get

    @staticmethod
    def getSubdivision(id: int) -> list:
        """ Получаем департамент сотрудника и проверяем его на наличие в списке департаментов групп"""
        subdivision = id[0]['UF_DEPARTMENT']
        truesubdivision = []
        for division in subdivision:
            if division in TreatmentData.dictDepartament:
                truesubdivision.append(division)
                return truesubdivision
        return False

    @staticmethod
    def getGroupLeader(id: int) -> int:
        """ Получаем ID Старшего группы """
        get = Bitrix24Data.B.callMethod('user.get', FILTER={"UF_DEPARTMENT": id})
        for employee in get:
            if employee["UF_USR_1669712148259"] == "23152":
                return employee["ID"]
        return False

    @staticmethod
    def getSupport(id: int):
        """ Получаем ID саппорта """
        get = Bitrix24Data.B.callMethod('user.get', FILTER={"UF_DEPARTMENT":id})
        for employee in get:
            if employee["UF_USR_1669712148259"] == "23148":
                return employee["ID"]
        return False

    @staticmethod
    def getCategory(id: int):
        """ Определение категории обращения """
        idCategory = {
            1 : "Жалоба",
            2 : "Обращение",
            3 : "Отзыв"
         }
        return idCategory.get(id,"Неизвестная категория")

    @staticmethod
    def addTask(idSupport: int, idCategory: int, message: str, client: str, groupLeader: int):
        """Ставим задачу саппорту"""
        add = Bitrix24Data.B.callMethod('tasks.task.add', fields={"TITLE": f"Оповещение из Телеграм. {TreatmentData.getCategory(idCategory)}",
                                                                  "RESPONSIBLE_ID": str(idSupport),
                                                                  "DEADLINE":str(datetime.now(timezone(zone='Europe/Moscow')) + timedelta(hours=2))[0:19],
                                                                  "DESCRIPTION":f"Сообщение от клиента: {client}\nТекст сообщения: {message}",
                                                                  "AUDITORS": [groupLeader],
                                                                  "CREATED_BY": str(idSupport),
                                                                  "DATE_START": str(datetime.now(timezone(zone='Europe/Moscow')))[0:19]
                                                                  },
                                                                  )
        return True