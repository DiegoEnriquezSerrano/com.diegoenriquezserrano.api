import os
import requests

from django.conf import settings
from django.template.loader import render_to_string

from .confirmation_service import ConfirmationService


class MailgunService:
    def perform_send(message):
        result = requests.post(
            f"https://api.mailgun.net/v3/{settings.MAILGUN['CNAME']}/messages",
            auth=("api", settings.MAILGUN["API_KEY"]),
            data={
                "from": message["from"],
                "html": message["html_body"],
                "subject": message["subject"],
                "text": message["text_body"],
                "to": message["to"],
            },
        )

        return result

    def send_confirmation_email(user_instance):
        signed_token = ConfirmationService.generate_signed_token(user_instance)
        message = MailgunService.generate_confirmation_email(
            user_instance, signed_token
        )
        result = MailgunService.perform_send(message)

        return result

    def generate_confirmation_email(user_instance, signed_token):
        attrs = {
            "username": user_instance.username,
            "confirmation_token": signed_token,
            "client_url": os.getenv("CORS_ALLOWED_ORIGIN_CLIENT"),
        }
        msg_plain = render_to_string(
            "email/text/user_confirmation.txt",
            attrs,
        )
        msg_html = render_to_string(
            "email/html/user_confirmation.html",
            attrs,
        )

        return {
            "from": settings.MAILGUN["FROM_EMAIL"],
            "to": user_instance.email,
            "subject": "User confirmation required",
            "html_body": msg_html,
            "text_body": msg_plain,
        }

    def send_subscription_confirmation_email(subscription):
        signed_token = ConfirmationService.generate_signed_token(subscription)
        message = MailgunService.generate_subscription_confirmation_email(
            subscription, signed_token
        )
        result = MailgunService.perform_send(message)

        return result

    def generate_subscription_confirmation_email(subscription, signed_token):
        attrs = {
            "name": subscription.name or subscription.email,
            "confirmation_token": signed_token,
            "client_url": os.getenv("CORS_ALLOWED_ORIGIN_CLIENT"),
            "username": subscription.user.username,
        }
        msg_plain = render_to_string(
            "email/text/subscription_confirmation.txt",
            attrs,
        )
        msg_html = render_to_string(
            "email/html/subscription_confirmation.html",
            attrs,
        )

        return {
            "from": settings.MAILGUN["FROM_EMAIL"],
            "to": subscription.email,
            "subject": "Subscription confirmation required",
            "html_body": msg_html,
            "text_body": msg_plain,
        }
