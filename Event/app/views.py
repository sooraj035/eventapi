from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from app.models import Event
from app.serializers import EventSerializer, UserSerializer


class Home(APIView):
    def get(self, request):
        return Response({"message": "Welcome to Event API"})


class UserReg(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Registration API",
            "required_fields": [
                "username",
                "email",
                "password",
                "first_name",
                "last_name"
            ]
        })

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "username": user.username
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Userlogin(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Login API",
            "required_fields": [
                "username",
                "password"
            ]
        })

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "username": user.username
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )


class Userlogout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            status.HTTP_204_NO_CONTENT
        })

    def post(self, request):
        request.user.auth_token.delete()

        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )


class Createevent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class Detail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        serializer = EventSerializer(event)

        return Response(serializer.data)

    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        serializer = EventSerializer(
            event,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        event.delete()

        return Response(
            {"message": "Event deleted"},
            status=status.HTTP_204_NO_CONTENT
        )