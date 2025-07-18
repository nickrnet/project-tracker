from django.test import TestCase

from core.util import validate_ip_address


class CoreUtilTestCase(TestCase):

    def test_validate_ip_address_valid(self):
        valid_ip = "192.168.1.201"
        self.assertEqual(validate_ip_address(valid_ip), valid_ip)

    def test_validate_ip_address_invalid(self):
        invalid_ip = "192.168.1.291"
        self.assertIsNone(validate_ip_address(invalid_ip))

    def test_validate_ip_address_empty(self):
        invalid_ip = ""
        self.assertIsNone(validate_ip_address(invalid_ip))
