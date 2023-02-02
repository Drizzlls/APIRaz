from rest_framework import serializers


class TgBotDataModel:
    def __init__(self,idManager,category,message,nickname):
        self.idManager = idManager
        self.category = category
        self.message = message
        self.nickname = nickname

class TgBotDataSerializer(serializers.Serializer):
    idManager = serializers.IntegerField()
    category = serializers.IntegerField()
    message = serializers.CharField()
    nickname = serializers.CharField()


class TgBotGetUserSerializer(serializers.Serializer):
    nickname = serializers.CharField()
