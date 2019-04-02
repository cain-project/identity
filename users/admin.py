from django.contrib import admin

from users.models import User, Group, Responsibility, Role, Membership


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date_created',)
    list_filter = ('locale', 'date_created', 'date_updated',)
    ordering = ('-date_created',)
    search_fields = ('full_name', 'email', 'preferred_name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name')
    search_fields = ('short_name', 'name', 'slug')


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name', 'description', 'slug')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('membership', 'responsibility', 'date_created')
    list_filter = ('responsibility', 'membership__group')
    search_fields = ('membership__group__name', 'membership__group__short_name',
                     'membership__user__full_name', 'membership__user__preferred_name',
                     'responsibility__name',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('group__name', 'group__short_name',
                     'user__full_name', 'user__preferred_name',)
