from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(r'^[0-9]*$', "Only numbers are allowed.", "Invalid phone number")