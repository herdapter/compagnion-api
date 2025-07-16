from rest_framework import serializers
from .models import *

class CreateRoomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    img_team1 = serializers.CharField(required=True)
    img_team2 = serializers.CharField(required=True)

    class Meta:
        model = Rooms
        fields = ['name', 'img_team1', 'img_team2']

    def create(self, validated_data):
        user = self.context['request'].user
        room = Rooms.objects.create(**validated_data)
        Adminrooms.objects.create(user=user, room=room)
        return room

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['id', 'name', 'img_team1', 'img_team2','status', 'created_at', 'close_at']

class RoomMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMembership
        fields = ['user', 'room', 'joined_at']
