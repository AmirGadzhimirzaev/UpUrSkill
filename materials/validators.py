import re

from rest_framework.serializers import ValidationError

pattern = r'youtube\.com'

def validate_accepted_site(value):
    if not re.search(pattern, value):
        raise ValidationError('Ссылка на запрещенный сайт (доступно только на youtube.com)')