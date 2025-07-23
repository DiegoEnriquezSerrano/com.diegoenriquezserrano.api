from rest_framework import serializers

from blog.models import Subscription, User


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Subscription
        fields = ["id", "email", "activated_date", "active", "user"]
        read_only_fields = ["id", "activated_date"]

    def validate(self, data):
        super().validate(data)

        publisher_email = data["user"].email

        if publisher_email == data["email"]:
            raise serializers.ValidationError("Cannot self-subscribe")

        return data
