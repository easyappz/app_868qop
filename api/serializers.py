from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Member, Listing, ChatThread, Message


class MemberPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "name", "phone", "about", "date_joined"]
        read_only_fields = fields


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "name", "phone", "about", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=32)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_phone(self, value):
        if Member.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Телефон уже зарегистрирован")
        return value

    def create(self, validated_data):
        return Member.objects.create(
            name=validated_data["name"],
            phone=validated_data["phone"],
            password_hash=make_password(validated_data["password"]),
        )


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=32)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")
        try:
            member = Member.objects.get(phone=phone)
        except Member.DoesNotExist:
            raise serializers.ValidationError("Неверный телефон или пароль")
        if not check_password(password, member.password_hash):
            raise serializers.ValidationError("Неверный телефон или пароль")
        attrs["member"] = member
        return attrs


class ListingSerializer(serializers.ModelSerializer):
    author = MemberPublicSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "author",
            "title",
            "description",
            "price",
            "images",
            "phone",
            "category",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]


class ListingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["title", "description", "price", "images", "phone", "category"]


class ChatThreadSerializer(serializers.ModelSerializer):
    member_a = MemberPublicSerializer(read_only=True)
    member_b = MemberPublicSerializer(read_only=True)

    class Meta:
        model = ChatThread
        fields = ["id", "listing", "member_a", "member_b", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    sender = MemberPublicSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "thread", "sender", "content", "created_at"]
        read_only_fields = ["id", "thread", "sender", "created_at"]
