from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from judge.models import Profile, Language, Organization


class UserResource(resources.ModelResource):
    name = fields.Field(attribute='profile__name')
    about = fields.Field(attribute='profile__about')
    organizations = fields.Field(widget=widgets.ManyToManyWidget(model=Organization, field='key'),
                                 attribute='profile__organizations')

    def init_instance(self, row=None):
        usr = super(UserResource, self).init_instance(row)
        usr.is_active = True
        usr.profile = Profile(language=Language.objects.get(key=getattr(settings,
                                                                        'DEFAULT_USER_LANGUAGE',
                                                                        'CPP11')))
        return usr

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.set_password(instance.password)

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)
        export_order = ('username', 'email', 'name', 'about', 'organizations')
        import_id_fields = ('username',)


class MyUserAdmin(UserAdmin, ImportExportModelAdmin):
    resource_class = UserResource
