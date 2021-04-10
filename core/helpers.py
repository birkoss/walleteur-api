import calendar
import datetime
import itertools

from django.db import models
from django.utils.text import slugify

from rest_framework import status
from rest_framework.response import Response


def add_months(date, months):
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def create_error_response(message):
    print("API ERROR: ")
    print(message)
    return Response({
        'error': message,
    }, status=status.HTTP_400_BAD_REQUEST)


def jsonfield_default_value():
    return {}


def slugify_model(model: models.Model, content: str) -> str:
    """
    Slugify a content and assume it's an unique slug in a model
    Parameters
    ----------
    model : django.db.models.Model, mandatory
            The model to check for uniqueness
    content : str, mandatory
            The content to slugify
    Returns
    -------
    slug : str
        the new unique slug for this model
    """
    slug_candidate = slug_original = slugify(content)

    for i in itertools.count(1):
        if not model.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = '{}-{}'.format(slug_original, i)

    return slug_candidate
