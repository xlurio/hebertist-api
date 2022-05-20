from django.contrib.auth import authenticate
# noinspection PyUnresolvedReferences
from core.models import GameModel, WishlistModel
# noinspection PyUnresolvedReferences
from game.serializers import GameSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializes the user objects"""
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'date_of_birth', ]

    def create(self, validated_data):
        """Create a new user objects"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update the authenticated user information"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


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


class WishlistSerializer(serializers.ModelSerializer):
    """Serializes the wishlist objects"""
    game = serializers.PrimaryKeyRelatedField(
        queryset=GameModel
    )

    class Meta:
        model = WishlistModel
        fields = ['id', 'game']
        read_only_fields = ['id']


class WishlistDetailSerializer(WishlistSerializer):
    """Serializes the wishlist object details"""
    game = GameSerializer(read_only=True)
