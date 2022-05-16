from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    """Serializes the authentication token objects"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validates and authenticates user"""
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            if not user:
                msg = _('Incorrect email or password')
                raise serializers.ValidationError(msg, code='Authorization')
        else:
            msg = _('Username and password required')
            raise serializers.ValidationError(msg, code='Authorization')

        attrs['user'] = user
        return attrs
