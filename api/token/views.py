from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['is_staff'] = user.is_staff
        token['name'] = user.first_name + " " + user.last_name

        return token

class CustomObtainPairView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer