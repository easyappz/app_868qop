from django.urls import path
from .views import (
    HelloView,
    RegisterView,
    LoginView,
    MeView,
    ListingListCreateView,
    ListingDetailView,
)

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("me/", MeView.as_view(), name="me"),
    path("listings/", ListingListCreateView.as_view(), name="listings"),
    path("listings/<int:pk>/", ListingDetailView.as_view(), name="listing-detail"),
]
