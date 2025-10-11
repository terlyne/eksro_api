from jinja2 import Environment, FileSystemLoader
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema

from core.config import settings, BASE_DIR


class EmailService:
    config = ConnectionConfig(
        MAIL_USERNAME=settings.email.username,
        MAIL_PASSWORD=settings.email.password,
        MAIL_FROM=settings.email.mail_from,
        MAIL_FROM_NAME=settings.email.mail_from_name,
        MAIL_PORT=settings.email.port,
        MAIL_SERVER=settings.email.server,
        MAIL_STARTTLS=settings.email.starttls,
        MAIL_SSL_TLS=settings.email.ssl_tls,
        USE_CREDENTIALS=settings.email.use_credentials,
    )
    fast_mail = FastMail(config)
    templates_path = BASE_DIR / "app" / "core" / "email" / "templates"
    env = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=True,
        auto_reload=True,  # False для prod'а, True для dev'а
    )

    @classmethod
    async def send_register_invitation(cls, email: str, token: str):
        template = cls.env.get_template("register_invitation.html")

        html_content = template.render(
            invitation_url=f"{settings.frontend.register_invitation_url}/?token={token}"
        )

        message = MessageSchema(
            subject="Приглашение на регистрацию",
            recipients=[email],
            body=html_content,
            subtype="html",
        )

        await cls.fast_mail.send_message(message)

    @classmethod
    async def send_changing_password_url(cls, email: str, token: str):
        template = cls.env.get_template("changing_password.html")

        html_content = template.render(
            changing_password_url=f"{settings.frontend.changing_password_url}/?token={token}"
        )

        message = MessageSchema(
            subject="Изменение пароля",
            recipients=[email],
            body=html_content,
            subtype="html",
        )

        await cls.fast_mail.send_message(message)

    @classmethod
    async def send_response_to_feedback(
        cls,
        email: str,
        name: str,
        question: str,
        response: str,
    ):
        template = cls.env.get_template("feedback_response.html")

        html_content = template.render(
            name=name,
            question=question,
            response=response,
        )

        message = MessageSchema(
            subject="Ответ на вопрос",
            recipients=[email],
            body=html_content,
            subtype="html",
        )

        await cls.fast_mail.send_message(message)

    @classmethod
    async def send_confirmation_subscription(cls, email: str, token: str):
        template = cls.env.get_template("confirmation_subscription.html")

        html_content = template.render(
            confirmation_url=f"{settings.frontend.subscription_confirmation_url}/?token={token}",
        )

        message = MessageSchema(
            subject="Подтверждение рассылки",
            recipients=[email],
            body=html_content,
            subtype="html",
        )

        await cls.fast_mail.send_message(message)

    @classmethod
    async def mailing_to_subscribed(
        cls,
        news_title: str,
        news_text: str,
        news_url: str,
        *emails: str,
    ):
        template = cls.env.get_template("mailing.html")

        html_content = template.render(
            title=news_title,
            text=news_text,
            redirect_url=news_url,
        )

        message = MessageSchema(
            subject="Новая новость",
            recipients=[*emails],
            body=html_content,
            subtype="html",
        )

        await cls.fast_mail.send_message(message)
