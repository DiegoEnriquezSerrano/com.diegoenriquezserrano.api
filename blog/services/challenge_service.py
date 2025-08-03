import base64
import secrets

from captcha.image import ImageCaptcha

from django.core.signing import TimestampSigner, SignatureExpired, BadSignature


signer = TimestampSigner()


class ChallengeService:
    def generate_image_challenge():
        image = ImageCaptcha(
            fonts=["static/fonts/orbitron-medium.otf"],
            width=320,
            height=120,
            font_sizes=(48, 64, 96),
        )

        code = secrets.token_hex(3)
        data = image.generate(
            code, "webp", bg_color=(23, 23, 23), fg_color=(101, 255, 255)
        )
        base64_image = base64.b64encode(data.read()).decode("utf-8")
        signed_token = signer.sign_object({"code": code})
        response = {"challenge_image": base64_image, "signed_answer": signed_token}

        return response

    def validate_image_challenge_answer(challenge_answer: str, signed_answer: str):
        try:
            unsigned = signer.unsign_object(signed_answer)
            unsigned_token = unsigned["code"]
        except SignatureExpired:
            return False
        except BadSignature:
            return False

        return unsigned_token == challenge_answer
