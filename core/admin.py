from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import user_profile
from core.models import Team
from core.models import Match
from core.models import Season

class user_profileAdmin(UserAdmin):
    list_display = ('email','username','gamertag','profile_pic','date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('email','username',)
    readonly_fields=('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(user_profile, user_profileAdmin)
admin.site.register(Match)
admin.site.register(Season)
admin.site.register(Team)
