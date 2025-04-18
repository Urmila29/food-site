from django.core.validators import RegexValidator, EmailValidator

# Username: Only Letters, digits, and spaces allowed
username_validator = RegexValidator(
    regex=r'^[A-Za-z0-9 ]+$',
    message="Username can contain only letters, digits, and spaces.",
    code='invalid_username'
)

# Email: standard Django email validator (already ensures proper format)
email_validator = EmailValidator(
    message="Enter a valid email address."
)