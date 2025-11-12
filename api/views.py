from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from django.contrib.auth.hashers import make_password
from .serializers import (
    MemberSerializer,
    RegisterSerializer,
    LoginSerializer,
    ListingSerializer,
    ListingWriteSerializer,
    ChatThreadSerializer,
    MessageSerializer,
)
from .models import Member, Listing, ChatThread, Message
from .auth import create_jwt


class HelloView(APIView):
    @extend_schema(responses={200: MessageSerializer}, description="Get a hello world message")
    def get(self, request):
        data = {"message": "Hello!", "timestamp": timezone.now()}
        return Response(data)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: MemberSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.save()
            return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: dict})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.validated_data["member"]
            token = create_jwt(member.id)
            return Response({"token": token, "member": MemberSerializer(member).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: MemberSerializer})
    def get(self, request):
        member = getattr(request, "member", None)
        return Response(MemberSerializer(member).data)

    @extend_schema(request=MemberSerializer, responses={200: MemberSerializer})
    def patch(self, request):
        member = getattr(request, "member", None)
        serializer = MemberSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
