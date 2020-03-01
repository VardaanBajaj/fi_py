from django.core.exceptions import ValidationError
from django.conf import settings
# Create your models here.
def validate_content(value):
     content=value
     if content == "":
         raise ValidationError("Content cannot be empty")
     return value
