from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('foodtrack/', include('foodtrack.urls')),
    # path('api-auth/', include('rest_framework.urls'))
]
