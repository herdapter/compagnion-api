from rest_framework import serializers
from .models import *
from room.models import Rooms, Adminrooms

class BingoRoomsListSerializer(serializers.ModelSerializer):
    case_text = serializers.CharField(required=True)

    class Meta:
        model = Bingorooms
        fields = ['case_text']

    def create(self, validated_data):
        user = self.context['request'].user
        case_text = validated_data['case_text']

        try:
            admin = Adminrooms.objects.get(user=user)
        except Adminrooms.DoesNotExist:
            raise serializers.ValidationError("Vous n'êtes pas admin d'une room.")

        try:
            bingo = Bingos.objects.get(case_text=case_text)
        except Bingos.DoesNotExist:
            raise serializers.ValidationError("Cette case n'existe pas dans Bingos.")

        bingoroom = Bingorooms.objects.create(
            bingo=bingo,
            case_text=case_text,
            admin=admin
        )

        return bingoroom

class UserBingoCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBingoCases
        field = ['user', 'room', 'case_text', 'position']

    def create(self, validated_data):
        import random
        user = self.context['request'].user
        room = self.context['request'].room
        # Récupérer tous les Bingorooms disponibles pour cette room (ou globalement si pas filtré)
        all_bingorooms = list(Bingorooms.objects.all())
        if len(all_bingorooms) < 9:
            raise serializers.ValidationError("Il n'y a pas assez de cases bingo disponibles.")
        # Tirer 9 Bingorooms aléatoires sans doublon
        selected_bingorooms = random.sample(all_bingorooms, 9)
        user_bingo_cases = []
        for position, bingoroom in enumerate(selected_bingorooms, start=1):
            case_text = bingoroom.case_text
            # Vérifier que ce case_text n'existe pas déjà pour cet user/room
            if UserBingoCases.objects.filter(user=user, room=room, case_text=case_text).exists():
                continue  # On saute si déjà existant
            user_bingo_case = UserBingoCases.objects.create(
                user=user,
                room=room,
                case_text=case_text,
                position=position
            )
            user_bingo_cases.append(user_bingo_case)
        return user_bingo_cases

class ValidatedCasesSerializer(serializers.ModelSerializer):
    bingoroom_id = serializers.IntegerField(write_only=True)
    is_checked = serializers.BooleanField(required=True)

    class Meta:
        model = ValidatedCases
        fields = ['bingoroom_id', 'is_checked']

    def create(self, validated_data):
        bingoroom_id = validated_data['bingoroom_id']
        is_checked = validated_data['is_checked']
        try:
            bingoroom = Bingorooms.objects.get(id=bingoroom_id)
        except Bingorooms.DoesNotExist:
            raise serializers.ValidationError("Cette case n'existe pas dans Bingorooms.")
        validated_case, created = ValidatedCases.objects.get_or_create(
            bingoroom=bingoroom,
            defaults={'is_checked': is_checked}
        )
        if not created:
            validated_case.is_checked = is_checked
            validated_case.save()
        return validated_case
