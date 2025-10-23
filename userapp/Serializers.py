from rest_framework import serializers

from userapp.models import User, Banners



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class BannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields= '__all__'