from .serializer import *
from .models import *
from room.models import Rooms, Adminrooms
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework.generics import ListAPIView
from rest_framework import status

class BingoRoomsListView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BingoRoomsListSerializer
    def get(self, request):
        bingo = Bingos.objects.all()
        serializer = BingoRoomsListSerializer(bingo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        if not is_many:
            return Response({"error": "Sélectionnez au minimum 9 cases de bingo."}, status= status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)

class ValidatedCases(GenericAPIView):
    permission_classes = [IsAuthenticated, Adminrooms]
    serializer_class = ValidatedCasesSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_case = serializer.save()
        return Response({
            'id': validated_case.id,
            'bingoroom': validated_case.bingoroom.id,
            'is_checked': validated_case.is_checked
        }, status=status.HTTP_201_CREATED)
