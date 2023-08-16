import re
from rest_framework import serializers

class PasswordValidator:
    @staticmethod
    def validate(value):
        error_messages = []

        if len(value) < 8 or len(value) > 16:
            error_messages.append("Length should be between 8 and 16 characters.")

        if not any(char.isdigit() for char in value):
            error_messages.append("At least 1 number is required.")

        if not any(char.islower() for char in value):
            error_messages.append("At least 1 small letter is required.")

        if not any(char.isupper() for char in value):
            error_messages.append("At least 1 capital letter is required.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            error_messages.append("At least 1 special character is required.")

        if error_messages:
            raise serializers.ValidationError(" ".join(error_messages))

        return value

class CustomPasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [PasswordValidator.validate]
        kwargs['write_only'] = True
        kwargs['style'] = {'input_type': 'password'}
        super().__init__(*args, **kwargs)
