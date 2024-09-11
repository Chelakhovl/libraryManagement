from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'role', 'is_active']
    
    def validate_email(self, value):
        if not "@" in value:
            raise serializers.ValidationError("Invalid email address")
        return value