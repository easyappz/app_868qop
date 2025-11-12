from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from datetime import datetime
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


# Listings
class ListingListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(responses={200: ListingSerializer}, description="Список объявлений с фильтрами")
    def get(self, request):
        qs = Listing.objects.select_related("author").all()
        category = request.query_params.get("category")
        search = request.query_params.get("search")
        price_min = request.query_params.get("price_min")
        price_max = request.query_params.get("price_max")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if category:
            qs = qs.filter(category=category)
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        data = ListingSerializer(qs, many=True).data
        return Response(data)

    @extend_schema(request=ListingWriteSerializer, responses={201: ListingSerializer}, description="Создать объявление")
    def post(self, request):
        member = getattr(request, "member", None)
        if not member:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ListingWriteSerializer(data=request.data)
        if serializer.is_valid():
            listing = serializer.save(author=member)
            return Response(ListingSerializer(listing).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListingDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Listing.objects.select_related("author").get(pk=pk)
        except Listing.DoesNotExist:
            return None

    @extend_schema(responses={200: ListingSerializer})
    def get(self, request, pk: int):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "Не найдено"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ListingSerializer(obj).data)

    @extend_schema(request=ListingWriteSerializer, responses={200: ListingSerializer})
    def patch(self, request, pk: int):
        member = getattr(request, "member", None)
        if not member:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "Не найдено"}, status=status.HTTP_404_NOT_FOUND)
        if obj.author_id != member.id:
            return Response({"detail": "Нет прав"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ListingWriteSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ListingSerializer(obj).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int):
        member = getattr(request, "member", None)
        if not member:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "Не найдено"}, status=status.HTTP_404_NOT_FOUND)
        if obj.author_id != member.id:
            return Response({"detail": "Нет прав"}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Chat
class ChatStartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=dict, responses={200: ChatThreadSerializer}, description="Начать чат с пользователем по желанию с привязкой к объявлению")
    def post(self, request):
        me = request.member
        recipient_id = request.data.get("recipient_id")
        listing_id = request.data.get("listing_id")
        if not recipient_id:
            return Response({"detail": "recipient_id обязателен"}, status=status.HTTP_400_BAD_REQUEST)
        if int(recipient_id) == me.id:
            return Response({"detail": "Нельзя начать чат с собой"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            other = Member.objects.get(id=recipient_id)
        except Member.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        # Normalize order so unique_together works regardless of order
        a, b = (me, other) if me.id < other.id else (other, me)
        listing = None
        if listing_id:
            try:
                listing = Listing.objects.get(id=listing_id)
            except Listing.DoesNotExist:
                return Response({"detail": "Объявление не найдено"}, status=status.HTTP_404_NOT_FOUND)
        thread, _ = ChatThread.objects.get_or_create(member_a=a, member_b=b, listing=listing)
        return Response(ChatThreadSerializer(thread).data)


class ChatListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: ChatThreadSerializer})
    def get(self, request):
        me = request.member
        qs = ChatThread.objects.filter(Q(member_a=me) | Q(member_b=me)).select_related("member_a", "member_b", "listing")
        data = ChatThreadSerializer(qs, many=True).data
        return Response(data)


class ChatMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_thread(self, me, thread_id):
        try:
            thread = ChatThread.objects.select_related("member_a", "member_b", "listing").get(id=thread_id)
        except ChatThread.DoesNotExist:
            return None
        if thread.member_a_id != me.id and thread.member_b_id != me.id:
            return None
        return thread

    @extend_schema(responses={200: MessageSerializer})
    def get(self, request, thread_id: int):
        me = request.member
        thread = self.get_thread(me, thread_id)
        if not thread:
            return Response({"detail": "Не найдено"}, status=status.HTTP_404_NOT_FOUND)
        msgs = thread.messages.select_related("sender").all()
        return Response(MessageSerializer(msgs, many=True).data)

    @extend_schema(request=dict, responses={201: MessageSerializer})
    def post(self, request, thread_id: int):
        me = request.member
        thread = self.get_thread(me, thread_id)
        if not thread:
            return Response({"detail": "Не найдено"}, status=status.HTTP_404_NOT_FOUND)
        content = request.data.get("content", "").strip()
        if not content:
            return Response({"detail": "Пустое сообщение"}, status=status.HTTP_400_BAD_REQUEST)
        msg = Message.objects.create(thread=thread, sender=me, content=content)
        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)
