from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Rooms, Adminrooms
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from rest_framework.generics import ListAPIView
from bingo.models import *
from bingo.serializer import UserBingoCasesSerializer

class RoomDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        user = request.user
        try:
            room = Rooms.objects.get(pk=pk)
        except Rooms.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

        is_admin = Adminrooms.objects.filter(room=room, user=user).exists()

        if not is_admin:
            return Response({'error': 'You are not the admin of this room'}, status=status.HTTP_403_FORBIDDEN)

        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoomCreateVIew(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateRoomSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            room = serializer.save()
            return Response(CreateRoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminRoomsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomListSerializer

    def get_queryset(self):
        user = self.request.user
        admin_room_ids = Adminrooms.objects.filter(user=user).values_list('room_id', flat=True)
        return Rooms.objects.filter(id__in=admin_room_ids)

class RoomMembershipView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomMembershipSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        room_id = request.data.get('room')
        if not room_id:
            return Response({'error': 'room id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            room = Rooms.objects.get(id=room_id)
        except Rooms.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        # Vérifier si déjà membre
        if RoomMembership.objects.filter(user=user, room=room).exists():
            return Response({'error': 'Already joined this room'}, status=status.HTTP_400_BAD_REQUEST)
        # Créer le membership
        membership = RoomMembership.objects.create(user=user, room=room)
        # Créer les UserBingoCases pour cet utilisateur dans cette room
        # On passe le contexte pour que le serializer ait accès à user et room
        user_bingo_serializer = UserBingoCasesSerializer(data={}, context={'request': request})
        user_bingo_serializer.context['request'].room = room  # hack pour compatibilité
        user_bingo_serializer.is_valid(raise_exception=False)  # pas de data à valider
        user_bingo_cases = user_bingo_serializer.create({})
        return Response({
            'membership': RoomMembershipSerializer(membership).data,
            'user_bingo_cases': [
                {'id': case.id, 'case_text': case.case_text, 'position': case.position}
                for case in user_bingo_cases
            ]
        }, status=status.HTTP_201_CREATED)
