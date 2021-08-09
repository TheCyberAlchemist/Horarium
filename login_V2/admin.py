from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

from .models import AuditEntry

class Show_unique_users(admin.SimpleListFilter):
	# Human-readable title which will be displayed in the
	# right admin sidebar just above the filter options.
	title = ('User_id')

	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'Show Unique'

	def lookups(self, request, model_admin):
		"""
		Returns a list of tuples. The first element in each
		tuple is the coded value for the option that will
		appear in the URL query. The second element is the
		human-readable name for the option that will appear
		in the right sidebar.
		"""
		return (
			('Yes', ('Show Unique user_ids')),
		)

	def queryset(self, request, queryset):
		"""
		Returns the filtered queryset based on the value
		provided in the query string and retrievable via
		`self.value()`.
		"""
		# Compare the requested value (either '80s' or '90s')
		# to decide how to filter the queryset.
		if self.value() == 'Yes':
			user_ids = set()
			pks = set()
			for i in queryset.order_by('-timestamp'):
				if i.user_id not in user_ids:
					pks.add(i.pk)
					user_ids.add(i.user_id)
			return queryset.filter(pk__in=pks)



@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['user_id','action','email_used']
    list_filter = ['action',Show_unique_users,"timestamp",]
    readonly_fields = ('timestamp',)

admin.site.register(get_user_model(), CustomUserAdmin)
