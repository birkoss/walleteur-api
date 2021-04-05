from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users.api.urls import urlpatterns as users_urlpatterns
from transactions.api.urls import urlpatterns as transactions_urlpatterns

urlpatterns = [
    # path('logout/', admin.site.urls, name='logout'),

    path('admin/', admin.site.urls),

] + users_urlpatterns + transactions_urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
