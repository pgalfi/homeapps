from unittest import TestCase

from foodtrack.management.commands.parseRecipes import PrepTime


class TestPrepTime(TestCase):
    def test_get1(self):
        self.assertEqual(PrepTime("  5:30 hours ").get(), 330)

    def test_get2(self):
        self.assertEqual(PrepTime(" 60 minutes ").get(), 60)

    def test_get3(self):
        self.assertEqual(PrepTime(" 35-40 minutes ").get(), 37.5)

    def test_get4(self):
        self.assertEqual(PrepTime(" 9-10 Hours  ").get(), 9.5*60)

    def test_get5(self):
        self.assertEqual(PrepTime(" 30 -40 minutes ").get(), 35)

    def test_get6(self):
        self.assertEqual(PrepTime(" About 1 hour ").get(), 60)

    def test_get7(self):
        self.assertEqual(PrepTime(" 1:45 hours ").get(), 105)

    def test_get8(self):
        self.assertEqual(PrepTime(" 1 hour & 30 minutes ").get(), 90)

    def test_get9(self):
        self.assertEqual(PrepTime(" 8 hours and 5 minutes ").get(), 8*60+5)

    def test_get10(self):
        self.assertEqual(PrepTime(" Maybe a day ").get(), -1)

