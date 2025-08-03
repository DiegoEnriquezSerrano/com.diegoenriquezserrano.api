from django.core.signing import TimestampSigner, SignatureExpired, BadSignature


class ConfirmationService:
    def attempt_token_unsign(signed_token):
        signer = TimestampSigner()

        try:
            unsigned = signer.unsign_object(signed_token, max_age=172_800)
            unsigned_token = unsigned["confirmation_token"]

            return unsigned_token
        except SignatureExpired:
            return None
        except BadSignature:
            return None

    def generate_signed_token(confirmable_instance):
        signer = TimestampSigner()
        signed_token = signer.sign_object(
            {"confirmation_token": confirmable_instance.confirmation_token}
        )

        return signed_token
