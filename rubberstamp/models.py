from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey


class AppPermissionManager(models.Manager):
    def assign(self, permission, user, obj=None):
        content_type = ContentType.objects.get_for_model(obj)
        (app_label, codename) = permission.split('.', 1)
        perm = self.get(
            app_label=app_label,
            content_types=content_type,
            codename=codename
        )
        return AssignedPermission.objects.get_or_create(
            permission=perm,
            user=user,
            content_type=content_type,
            object_id=obj.id
        )


class AppPermission(models.Model):
    """
    Permission model which allows apps to add permissions for models in other
    apps, keeping track of the permissions added by each app.
    """
    
    app_label = models.CharField(max_length=100)
    codename = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    content_types = models.ManyToManyField(ContentType)
    
    objects = AppPermissionManager()
    
    class Meta:
        unique_together = ('app_label', 'codename')
    
    def __unicode__(self):
        return '%s.%s' % (self.app_label, self.codename)


class AssignedPermission(models.Model):
    permission = models.ForeignKey(AppPermission)
    user = models.ForeignKey(User)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey()