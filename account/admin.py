from django.contrib import admin
import datetime

from .models import BoardUser
from .utilities import send_activation_note


def send_activation_msg(modeladmin, request, queryset):
    for req in queryset:
        if not req.is_activated:
            send_activation_note(req)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')


send_activation_msg.short_description = 'Отправка писем с требованиями активации'


class NonActivatedFilter(admin.SimpleListFilter):
    title = 'Активирован'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (('activated', "Активированы"),
                ('threedays', 'He прошли более 3 дней'),
                ('week', 'He прошли более недели'),
                )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined_date_lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined_date_lt=d)


class BroadUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'list_name')
    list_filter = (NonActivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('com_notification', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined')
              )
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_msg, )


admin.site.register(BoardUser, BroadUserAdmin)
