from rest_framework import serializers

from blog.services.challenge_service import ChallengeService


class ChallengeImageSerializer(serializers.Serializer):
    signed_answer = serializers.CharField(required=True)
    challenge_answer = serializers.CharField(required=True)

    def validate(self, data):
        super().validate(data)

        if not ChallengeService.validate_image_challenge_answer(
            data["challenge_answer"], data["signed_answer"]
        ):
            raise serializers.ValidationError("Captcha invalid")

        return data
