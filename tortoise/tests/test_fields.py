import unittest
from datetime import date, datetime, timedelta
from decimal import Decimal
from time import sleep

from tortoise import fields
from tortoise.contrib.test import TestCase
from tortoise.exceptions import ConfigurationError, IntegrityError
from tortoise.tests import testmodels


class TestFieldErrors(unittest.TestCase):

    def test_char_field_empty(self):
        with self.assertRaises(ConfigurationError):
            fields.CharField()

    def test_char_field_zero(self):
        with self.assertRaises(ConfigurationError):
            fields.CharField(max_length=0)

    def test_decimal_field_empty(self):
        with self.assertRaises(ConfigurationError):
            fields.DecimalField()

    def test_decimal_field_neg_digits(self):
        with self.assertRaises(ConfigurationError):
            fields.DecimalField(max_digits=0, decimal_places=2)

    def test_decimal_field_neg_decimal(self):
        with self.assertRaises(ConfigurationError):
            fields.DecimalField(max_digits=2, decimal_places=-1)

    def test_datetime_field_auto_bad(self):
        with self.assertRaises(ConfigurationError):
            fields.DatetimeField(auto_now=True, auto_now_add=True)


class TestIntFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.IntFields.create()

    async def test_create(self):
        obj0 = await testmodels.IntFields.create(intnum=1)
        obj = await testmodels.IntFields.get(id=obj0.id)
        self.assertEqual(obj.intnum, 1)
        self.assertEqual(obj.intnum_null, None)
        await obj.save()
        obj2 = await testmodels.IntFields.get(id=obj.id)
        self.assertEqual(obj, obj2)

    async def test_cast(self):
        obj0 = await testmodels.IntFields.create(intnum='3')
        obj = await testmodels.IntFields.get(id=obj0.id)
        self.assertEqual(obj.intnum, 3)


class TestSmallIntFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.SmallIntFields.create()

    async def test_create(self):
        obj0 = await testmodels.SmallIntFields.create(smallintnum=2)
        obj = await testmodels.SmallIntFields.get(id=obj0.id)
        self.assertEqual(obj.smallintnum, 2)
        self.assertEqual(obj.smallintnum_null, None)
        await obj.save()
        obj2 = await testmodels.SmallIntFields.get(id=obj.id)
        self.assertEqual(obj, obj2)


class TestCharFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.CharFields.create()

    async def test_create(self):
        obj0 = await testmodels.CharFields.create(char='moo')
        obj = await testmodels.CharFields.get(id=obj0.id)
        self.assertEqual(obj.char, 'moo')
        self.assertEqual(obj.char_null, None)
        await obj.save()
        obj2 = await testmodels.CharFields.get(id=obj.id)
        self.assertEqual(obj, obj2)


class TestTextFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.TextFields.create()

    async def test_create(self):
        obj0 = await testmodels.TextFields.create(text='baa')
        obj = await testmodels.TextFields.get(id=obj0.id)
        self.assertEqual(obj.text, 'baa')
        self.assertEqual(obj.text_null, None)
        await obj.save()
        obj2 = await testmodels.TextFields.get(id=obj.id)
        self.assertEqual(obj, obj2)


class TestBooleanFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.BooleanFields.create()

    async def test_create(self):
        obj0 = await testmodels.BooleanFields.create(boolean=True)
        obj = await testmodels.BooleanFields.get(id=obj0.id)
        self.assertEqual(obj.boolean, True)
        self.assertEqual(obj.boolean_null, None)
        await obj.save()
        obj2 = await testmodels.BooleanFields.get(id=obj.id)
        self.assertEqual(obj, obj2)


class TestDecimalFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.DecimalFields.create()

    async def test_create(self):
        obj0 = await testmodels.DecimalFields.create(decimal=Decimal('1.23456'))
        obj = await testmodels.DecimalFields.get(id=obj0.id)
        self.assertEqual(obj.decimal, Decimal('1.2346'))
        self.assertEqual(obj.decimal_null, None)
        await obj.save()
        obj2 = await testmodels.DecimalFields.get(id=obj.id)
        self.assertEqual(obj, obj2)


class TestDatetimeFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.DatetimeFields.create()

    async def test_create(self):
        now = datetime.utcnow()
        obj0 = await testmodels.DatetimeFields.create(datetime=now)
        obj = await testmodels.DatetimeFields.get(id=obj0.id)
        self.assertEqual(obj.datetime, now)
        self.assertEqual(obj.datetime_null, None)
        self.assertLess(obj.datetime_auto - now, timedelta(seconds=1))
        self.assertLess(obj.datetime_add - now, timedelta(seconds=1))
        datetime_auto = obj.datetime_auto
        sleep(1)
        await obj.save()
        obj2 = await testmodels.DatetimeFields.get(id=obj.id)
        self.assertEqual(obj2.datetime, now)
        self.assertEqual(obj2.datetime_null, None)
        self.assertEqual(obj2.datetime_auto, obj.datetime_auto)
        self.assertNotEqual(obj2.datetime_auto, datetime_auto)
        self.assertGreater(obj2.datetime_auto - now, timedelta(seconds=1))
        self.assertLess(obj2.datetime_auto - now, timedelta(seconds=2))
        self.assertEqual(obj2.datetime_add, obj.datetime_add)


class TestDateFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.DateFields.create()

    async def test_create(self):
        today = date.today()
        obj0 = await testmodels.DateFields.create(date=today)
        obj = await testmodels.DateFields.get(id=obj0.id)
        self.assertEqual(obj.date, today)
        self.assertEqual(obj.date_null, None)
        await obj.save()
        obj2 = await testmodels.DateFields.get(id=obj.id)
        self.assertEqual(obj, obj2)


class TestFloatFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.FloatFields.create()

    async def test_create(self):
        obj0 = await testmodels.FloatFields.create(floatnum=1.23)
        obj = await testmodels.FloatFields.get(id=obj0.id)
        self.assertEqual(obj.floatnum, 1.23)
        self.assertNotEqual(Decimal(obj.floatnum), Decimal('1.23'))
        self.assertEqual(obj.floatnum_null, None)
        await obj.save()
        obj2 = await testmodels.FloatFields.get(id=obj.id)
        self.assertEqual(obj, obj2)


class TestJSONFields(TestCase):
    async def test_empty(self):
        with self.assertRaises(IntegrityError):
            await testmodels.JSONFields.create()

    @unittest.expectedFailure
    async def test_create(self):
        # TODO: Expect to work
        obj0 = await testmodels.JSONFields.create(data={'some': ['text', 3]})
        obj = await testmodels.JSONFields.get(id=obj0.id)
        self.assertEqual(obj.data, {'some': ['text', 3]})
        self.assertEqual(obj.data, None)
        await obj.save()
        obj2 = await testmodels.JSONFields.get(id=obj.id)
        self.assertEqual(obj, obj2)
