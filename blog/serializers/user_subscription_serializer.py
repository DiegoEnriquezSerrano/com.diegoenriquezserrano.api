from rest_framework import serializers

from blog.models import UserSubscription, User

from .user_serializer import UserSerializer


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    subscriber = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserSubscription
        fields = ["id", "subscriber", "activated_date", "active", "user"]
        read_only_fields = ["id", "activated_date", "user", "subscriber"]


class CreateUserSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    subscriber = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserSubscription
        fields = ["id", "subscriber", "activated_date", "active", "user"]
        read_only_fields = ["id", "activated_date", "user", "subscriber"]

    def validate(self, data):
        super().validate(data)

        if data.get("subscriber") == data.get("user"):
            raise serializers.ValidationError("Cannot self-subscribe")

        return data
