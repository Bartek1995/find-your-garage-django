from django.test import TestCase
import django


class DatabaseConnectionTest(TestCase):
    def test_connection(self):
        result = django.db.connection.ensure_connection()
        self.assertEquals(result, None)
