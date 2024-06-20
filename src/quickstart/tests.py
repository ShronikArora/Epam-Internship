from django.test import TestCase

class QuickStartTest(TestCase):
    def setUp(self):
        pass

    def test_1(self):
        x = 2 * 2
        self.assertEqual(x, 4)

    def tearDown(self):
        pass
