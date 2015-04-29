from allauth.account.models import EmailConfirmation, EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

from rest_framework.authtoken.models import Token
from .models import User, PasswordReset, HelpTicket, SignupCode

from applications.accounts import forms

class UserAdmin(UserAdmin):
    add_form = forms.UserCreationAdminForm
    list_display = ('admin_thumbnail', 'username', 'email', 'name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'gender', 'image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Points & Analytiucs'), {'fields': ('first_page', 'total_points','redeemable_points','activity_level')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )



admin.site.register(User, UserAdmin)

class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'email')


admin.site.register(PasswordReset, PasswordResetAdmin)




class HelpTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'time_created')
admin.site.register(HelpTicket, HelpTicketAdmin)

class SignupCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code')

admin.site.register(SignupCode, SignupCodeAdmin)


from rest_framework.authtoken.models import Token


class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created')
    fields = ('user',)
    ordering = ('-created',)

admin.site.unregister(Token) #First unregister the old class
admin.site.unregister(EmailConfirmation)
admin.site.unregister(EmailAddress)
admin.site.register(Token, AuthTokenAdmin)

