from django.core.signing import TimestampSigner, SignatureExpired, BadSignature

signer = TimestampSigner()


class ConfirmationService:
    def attempt_token_unsign(signed_token):
        try:
            unsigned = signer.unsign_object(signed_token, max_age=172_800)
            unsigned_token = unsigned["confirmation_token"]

            return unsigned_token
        except SignatureExpired:
            return None
        except BadSignature:
            return None

    def generate_signed_token(confirmable_instance):
        signed_token = signer.sign_object(
            {"confirmation_token": confirmable_instance.confirmation_token}
        )

        return signed_token
