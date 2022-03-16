from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from members.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Configure admin titles

admin.site.site_header = "Sweaty Games Admin Page"
admin.site.site_title = "Sweaty Games"
admin.site.index_title = "Time to administrate"
