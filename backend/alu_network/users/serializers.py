"""
Serializers for the user API
"""

from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'short_bio', 'about_me',
                  'user_role', 'intake', 'professional_role', 'current_company')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """
        Creates a new user
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a user
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class  AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate the user credentials"""

        user = authenticate(
            request=self.context.get('request'),
            email = attrs.get('email'),
            password = attrs.get('password')
        )

        if not user:
            message = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(message, code='authentication')

        attrs['user'] = user
        return attrs
