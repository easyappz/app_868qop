from django.urls import path
from .views import (
    HelloView,
    RegisterView,
    LoginView,
    MeView,
    ListingListCreateView,
    ListingDetailView,
    ChatStartView,
    ChatListView,
    ChatMessagesView,
)

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("me/", MeView.as_view(), name="me"),
    path("listings/", ListingListCreateView.as_view(), name="listings"),
    path("listings/<int:pk>/", ListingDetailView.as_view(), name="listing-detail"),
    path("chats/start/", ChatStartView.as_view(), name="chat-start"),
    path("chats/", ChatListView.as_view(), name="chat-list"),
    path("chats/<int:thread_id>/messages/", ChatMessagesView.as_view(), name="chat-messages"),
]
