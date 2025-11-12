from typing import Tuple, Optional
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from .models import Member
from .auth import verify_jwt


class MemberJWTAuthentication(BaseAuthentication):
    keyword = b"Bearer"

    def authenticate(self, request) -> Optional[Tuple[Member, None]]:
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower():
            return None
        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Недействительный заголовок авторизации.")
        try:
            token = auth[1].decode("utf-8")
        except Exception:
            raise exceptions.AuthenticationFailed("Токен не распознан.")

        data = verify_jwt(token)
        if not data:
            raise exceptions.AuthenticationFailed("Неверный или истёкший токен.")
        member_id = data.get("m")
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            raise exceptions.AuthenticationFailed("Пользователь не найден.")
        # Attach for convenience
        request.member = member
        return (member, None)
