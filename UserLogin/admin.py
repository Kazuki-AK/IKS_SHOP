#from django.contrib import admin

# Register your models here.

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from .models import User,Shop


admin.site.site_title = 'IKS管理サイト' 
admin.site.site_header = 'メンバー管理' 
admin.site.index_title = 'テーブル操作用'
 

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
 
 
# Now register the new MyUserAdmin...
#admin.site.register(User, MyUserAdmin)+( ShopInfo )　※利用客側アプリでは名簿のみ登録
@admin.register(User, Shop)
class AppAdmin(admin.ModelAdmin):
    pass
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

