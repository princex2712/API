from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, CreatePostView, UserPostViewset, UpdateUserView, DeleteAccountView


router = DefaultRouter()
router.register('list-post',UserPostViewset,basename="post")


urlpatterns = [
    path('',include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('update-profile/', UpdateUserView.as_view(), name='update_profile'),
    path('delete-account/<int:pk>/', DeleteAccountView.as_view(), name='delete_account'),
]