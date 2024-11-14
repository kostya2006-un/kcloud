from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ActivationCodeSerializer
from rest_framework import status
from rest_framework.response import Response


class ActivateWithCodeView(APIView):
    def post(self,  request, *args, **kwargs):
        serializer = ActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)