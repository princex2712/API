from .serializers import CustomUserModelSerializer, UserPostModelSerializer
from .models import UserPost,CustomUser
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import LoginSerializer, UserUpdateSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserPostViewset(viewsets.ModelViewSet):
    queryset = UserPost.objects.all()
    serializer_class = UserPostModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPost.objects.filter(user=self.request.user)

class CreatePostView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = UserPostModelSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            access_token = AccessToken.for_user(user)

            return Response(
                {'access_token': str(access_token)},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UpdateUserDetail(generics.UpdateAPIView):
    serializer_class = CustomUserModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserModelSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class UpdateUserView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserModelSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class DeleteAccountView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserModelSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    lookup_field = 'pk' 

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this account.")
        return obj

    def delete(self, request, *args, **kwargs):
        user = self.get_object() 
        self.perform_destroy(user) 
        return Response(
            {"message": "Account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT 
        )