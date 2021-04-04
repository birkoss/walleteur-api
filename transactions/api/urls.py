from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'v1/persons',
        api_views.persons.as_view(),
        name='persons'
    ),
    path(
        'v1/person/<str:person_id>',
        api_views.person.as_view(),
        name='person'
    ),
]
