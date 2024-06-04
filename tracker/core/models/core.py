import uuid

from django.db import models
from django.utils import timezone


class DeletedModel(models.Model):
    """
        Flags a record as deleted. Soft delete is the default behavior that allows the user to restore the item, hard delete cannot be undone by the user, but by administrators only.
    """
    deleted_by = models.ForeignKey('core.CoreUser', on_delete=models.CASCADE, editable=False)
    deleted_on = models.DateTimeField(null=False, default=timezone.now, editable=False)
    hard_deleted = models.BooleanField(default=False)
    soft_deleted = models.BooleanField(default=False)


class CoreModelActiveManager(models.Manager):
    """
        Active instances of the CoreModel are not deleted.
    """
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class CoreModel(models.Model):
    class Meta:
        abstract = True

    active_objects = CoreModelActiveManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey('core.CoreUser', on_delete=models.CASCADE, editable=False)
    deleted = models.ForeignKey(DeletedModel, on_delete=models.CASCADE, null=True, blank=True, db_index=False)

    def hard_delete(self, person_id):
        self.deleted = DeletedModel.objects.create(
            created_by_id=person_id,
            soft_deleted=False,
            hard_deleted=True,
            deleted_by_id=person_id,
        )
        self.save()

    def soft_delete(self, person_id):
        self.deleted = DeletedModel.objects.create(
            created_by_id=person_id,
            soft_deleted=True,
            hard_deleted=False,
            deleted_by_id=person_id,
        )
        self.save()

    # TODO: Filter by user/organization/project maybe, or a subclass can override and filter there.
    @classmethod
    def get_deleted_items(self):
        return self.objects.filter(deleted__isnull=False)

    @classmethod
    def get_hard_deleted_items(self):
        return self.objects.filter(deleted__hard_deleted=True)

    @classmethod
    def get_soft_deleted_items(self):
        return self.objects.filter(deleted__soft_deleted=True)
