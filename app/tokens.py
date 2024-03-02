from django.contrib.auth.tokens import PasswordResetTokenGenerator
from pip._vendor.six import text_type
from django.contrib.auth.models import User


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) +
            text_type(timestamp),
            text_type(user.profile.register_confirmation)
        )

generate_token = TokenGenerator()