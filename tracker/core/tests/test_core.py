from django.test import TestCase

from core.models import user as core_user_models


class CoreModelManagerTestCase(TestCase):
    def setUp(self):
        self.system_user = core_user_models.CoreUser.objects.get_or_create_system_user()
        self.user_to_hard_delete = core_user_models.CoreUser.objects.create_core_user_from_web({"email": "testuser_hard_deleted@test.com", "password": "password"})
        self.user_to_soft_delete = core_user_models.CoreUser.objects.create_core_user_from_web({"email": "testuser_soft_deleted@test.com", "password": "password"})
        self.user_to_not_delete = core_user_models.CoreUser.objects.create_core_user_from_web({"email": "testuser_not_deleted@test.com", "password": "password"})

        self.user_to_hard_delete.hard_delete(person_id=self.system_user.id)
        self.user_to_soft_delete.soft_delete(person_id=self.system_user.id)

    def test_get_deleted_items(self):
        deleted_items = core_user_models.CoreUser.get_deleted_items()
        self.assertEqual(deleted_items.count(), 2)
        self.assertIn(self.user_to_hard_delete, deleted_items)
        self.assertIn(self.user_to_soft_delete, deleted_items)
        self.assertNotIn(self.user_to_not_delete, deleted_items)

    def test_get_hard_deleted_items(self):
        hard_deleted_items = core_user_models.CoreUser.get_hard_deleted_items()
        self.assertEqual(hard_deleted_items.count(), 1)
        self.assertIn(self.user_to_hard_delete, hard_deleted_items)
        self.assertNotIn(self.user_to_not_delete, hard_deleted_items)

    def test_get_soft_deleted_items(self):
        soft_deleted_items = core_user_models.CoreUser.get_soft_deleted_items()
        self.assertEqual(soft_deleted_items.count(), 1)
        self.assertIn(self.user_to_soft_delete, soft_deleted_items)
        self.assertNotIn(self.user_to_not_delete, soft_deleted_items)


class CoreModelTestCase(TestCase):
    def setUp(self):
        self.system_user = core_user_models.CoreUser.objects.get_or_create_system_user()
        self.user_to_delete = core_user_models.CoreUser.objects.create_core_user_from_web({"email": "testuser@test.com", "password": "password"})

    def test_hard_delete(self):
        self.user_to_delete.hard_delete(person_id=self.system_user.id)
        self.assertIsNotNone(self.user_to_delete.deleted)
        self.assertTrue(self.user_to_delete.deleted.hard_deleted)
        self.assertFalse(self.user_to_delete.deleted.soft_deleted)

    def test_soft_delete(self):
        self.user_to_delete.soft_delete(person_id=self.system_user.id)
        self.assertIsNotNone(self.user_to_delete.deleted)
        self.assertTrue(self.user_to_delete.deleted.soft_deleted)
        self.assertFalse(self.user_to_delete.deleted.hard_deleted)

    def test_undo_hard_delete(self):
        self.user_to_delete.undo_hard_delete(person_id=self.system_user.id)
        self.assertIsNotNone(self.user_to_delete.deleted)
        self.assertTrue(self.user_to_delete.deleted.soft_deleted)
        self.assertFalse(self.user_to_delete.deleted.hard_deleted)

    def test_undo_soft_delete(self):
        self.user_to_delete.soft_delete(person_id=self.system_user.id)
        self.assertIsNotNone(self.user_to_delete.deleted)
        self.user_to_delete.undo_soft_delete(person_id=self.system_user.id)
        self.assertIsNone(self.user_to_delete.deleted)
