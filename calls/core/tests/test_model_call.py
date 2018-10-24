from datetime import datetime, time
import pytz
from dateutil.parser import parse

from decimal import Decimal

from django.test import TestCase

from model_mommy import mommy

from calls.core.models.call import Call, CallDetail
from calls.core.models.pricing_rule import PricingRule


class CallModelTest(TestCase):
    def setUp(self):

        detail_start = mommy.make(CallDetail, type=CallDetail.START)
        detail_end = mommy.make(CallDetail, type=CallDetail.END)

        self.call = Call(
            id=70,
            detail_start=detail_start,
            detail_end=detail_end,
            price=Decimal(10.50)
        )
        self.call.save()

    def test_create(self):
        self.assertTrue(CallDetail.objects.exists())

    def test_str(self):
        self.assertEqual("Call 70", str(self.call))


class CallModelDeleteTest(TestCase):
    fixtures = ['pricingrule.json']

    def setUp(self):
        # Input a Detail Start Record
        self.start_detail = CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        # Input a Detail End Record
        self.end_detail = CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

    def test_delete_call(self):
        self.assertTrue(Call.objects.exists(), msg="A Call record should be created")
        Call.objects.get(id=70).delete()
        self.assertFalse(Call.objects.exists(), msg="A Call record should be deleted")
        self.assertTrue(CallDetail.objects.exists(), msg="Call Details record should not be deleted")

    def test_delete_Start_call_detail(self):
        self.start_detail.delete()
        self.assertEqual(CallDetail.objects.count(), 1, msg="Just one Call Detail record should be deleted")
        self.assertTrue(Call.objects.exists(), msg="The Call record should not be deleted")
        self.assertIsNone(Call.objects.get(id=70).detail_start, msg="Start Call detail should be none")
        self.assertIsNotNone(Call.objects.get(id=70).detail_end, msg="End Call detail should not be none")
        self.assertEqual(Call.objects.get(id=70).price, Decimal('0.00'), msg="The price should be clean")

    def test_delete_both_call_details(self):
        self.start_detail.delete()
        self.end_detail.delete()
        self.assertFalse(CallDetail.objects.exists(), msg="Call Details record should be deleted")
        self.assertFalse(Call.objects.exists(), msg="The Call record should be deleted")


class CallDurationCalculationTest(TestCase):
    def test_duration_after_receiving_start_and_end_records(self):
        """
        Call duration should be calculated after receive Start and End records on that order.
        """
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        self.assertEqual(Call.objects.filter(id=70).count(), 1, msg="Should create one Call record.")
        call = Call.objects.get(id=70)

        expected_duration = "0h20m40s"

        self.assertEqual(expected_duration, call.duration, msg="Should calculate the call duration.")

    def test_duration_after_receiving_just_start_record(self):
        """
        Call duration should be zero after receive just a Call Start Detail Record.
        """
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        self.assertEqual(Call.objects.filter(id=70).count(), 1, msg="Should create one Call record.")
        call = Call.objects.get(id=70)

        expected_duration = '0h0m0s'

        self.assertEqual(expected_duration, call.duration, msg="Should return zero as call duration.")

    def test_duration_after_receiving_just_end_records(self):
        """
        Call duration should be zero after receive just a Call End Detail Record.
        """
        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        self.assertEqual(Call.objects.filter(id=70).count(), 1, msg="Should create one Call record.")
        call = Call.objects.get(id=70)

        expected_duration = '0h0m0s'

        self.assertEqual(expected_duration, call.duration, msg="Should return zero as call duration.")

    def test_duration_after_receiving_end_and_start_records(self):
        """
        Call duration should be calculated after receive End and Start records (inverse order).
        """
        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        self.assertEqual(Call.objects.filter(id=70).count(), 1, msg="Should create one Call record.")
        call = Call.objects.get(id=70)

        expected_duration = '0h20m40s'

        self.assertEqual(expected_duration, call.duration, msg="Should calculate the call duration.")


class CallPriceCalculationTest(TestCase):
    def setUp(self):
        self.pricing = PricingRule.objects.create(
            name="Standard time call",
            start_time=time(6, 0, 0),
            end_time=time(22, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.09),
        )

        self.pricing = PricingRule.objects.create(
            name="Reduced tariff time call",
            start_time=time(22, 0, 0),
            end_time=time(6, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.00),
        )

    def test_calculate_after_receiving_start_and_end_records(self):
        """
        Call price should be calculated after receive Start and End records on that order.
        """
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        self.assertEqual(Call.objects.filter(id=70).count(), 1, msg="Should create one Call record.")
        call = Call.objects.get(id=70)

        expected_price = Decimal('0.54')
        self.assertEqual(expected_price, call.price, msg="Should calculate the call price.")

    def test_calculate_after_receiving_just_start_records(self):
        """
        Call price should be zero after receive just a Call Start Detail Record.
        """
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        self.assertEqual(Call.objects.filter(id=70).count(), 1, msg="Should create one Call record.")
        call = Call.objects.get(id=70)

        expected_price = Decimal('0.00')
        self.assertEqual(expected_price, call.price, msg="The call price should be zero.")

    def test_calculate_after_receiving_just_end_records(self):
        """
        Call price should be zero after receive just a Call End Detail Record.
        """
        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        self.assertEqual(Call.objects.filter(id=70).count(), 1, msg="Should create one Call record.")
        call = Call.objects.get(id=70)

        expected_price = Decimal('0.00')
        self.assertEqual(expected_price, call.price, msg="The call price should be zero.")

    def test_calculate_after_receiving_end_and_start_records(self):
        """
        Call price should be calculated after receive End and Start records (inverted order).
        """
        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        self.assertEqual(Call.objects.filter(id=70).count(), 1, msg="Should create one Call record.")
        call = Call.objects.get(id=70)

        expected_price = Decimal('0.54')
        self.assertEqual(expected_price, call.price, msg="Should calculate the call price.")

    def test_price_calculate_case_sample_6(self):
        """
        Case 6: Start: 2017-12-12 21:57:13 End: 2017-12-13 22:10:56.
        """
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2017, 12, 12, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=75,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2017, 12, 13, 22, 10, 56, tzinfo=pytz.UTC),
            call_id=75,
        )

        self.assertEqual(Call.objects.filter(id=75).count(), 1, msg="Should create one Call record.")
        call = Call.objects.get(id=75)

        expected_price = Decimal('86.94')
        self.assertEqual(expected_price, call.price, msg="Should calculate the call price.")


class SampleCasesCalculationTest(TestCase):
    def setUp(self):
        self.pricing = PricingRule.objects.create(
            name="Standard time call",
            start_time=time(6, 0, 0),
            end_time=time(22, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.09),
        )

        self.pricing = PricingRule.objects.create(
            name="Reduced tariff time call",
            start_time=time(22, 0, 0),
            end_time=time(6, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.01),
        )

    def test_case_sample_1(self):
        """
        Sample 1: Start: 2016-02-29 12:00:00 End: 2016-02-29 14:00:00.
        """
        call_id = 70
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=parse('2016-02-29T12:00:00Z'),
            source="99988526423",
            destination="9933468278",
            call_id=call_id,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=parse('2016-02-29T14:00:00Z'),
            call_id=call_id,
        )

        self.assertEqual(Call.objects.filter(id=call_id).count(), 1, msg="Should create one Call record")
        call = Call.objects.get(id=call_id)

        expected_duration = '2h0m0s'
        self.assertEqual(expected_duration, call.duration, msg="Call duration different than expected")

        expected_price = Decimal('11.16')
        self.assertEqual(expected_price, call.price, msg="Call price different than expected")

    def test_case_sample_2(self):
        """
        Sample 2: Start: 2017-12-12 15:07:13 End: 2017-12-12 14:56:00.
        """
        call_id = 71
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=parse('2017-12-12T15:07:13Z'),
            source="99988526423",
            destination="9933468278",
            call_id=call_id,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=parse('2017-12-12T15:14:56Z'),
            call_id=call_id,
        )

        self.assertEqual(Call.objects.filter(id=call_id).count(), 1, msg="Should create one Call record")
        call = Call.objects.get(id=call_id)

        expected_duration = '0h7m43s'
        self.assertEqual(expected_duration, call.duration, msg="Call duration different than expected")

        expected_price = Decimal('0.99')
        self.assertEqual(expected_price, call.price, msg="Call price different than expected")

    def test_case_sample_3(self):
        """
        Sample 3: Start: 2017-12-12 22:47:56 End: 2017-12-12 22:50:56.
        """
        call_id = 72
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=parse('2017-12-12T22:47:56Z'),
            source="99988526423",
            destination="9933468278",
            call_id=call_id,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=parse('2017-12-12T22:50:56Z'),
            call_id=call_id,
        )

        self.assertEqual(Call.objects.filter(id=call_id).count(), 1, msg="Should create one Call record")
        call = Call.objects.get(id=call_id)

        expected_duration = '0h3m0s'
        self.assertEqual(expected_duration, call.duration, msg="Call duration different than expected")

        expected_price = Decimal('0.39')
        self.assertEqual(expected_price, call.price, msg="Call price different than expected")

    def test_case_sample_4(self):
        """
        Sample 4: Start: 2017-12-12 21:57:13 End: 2017-12-12 22:10:56.
        """
        call_id = 73
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=parse('2017-12-12T21:57:13Z'),
            source="99988526423",
            destination="9933468278",
            call_id=call_id,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=parse('2017-12-12T22:10:56Z'),
            call_id=call_id,
        )

        self.assertEqual(Call.objects.filter(id=call_id).count(), 1, msg="Should create one Call record")
        call = Call.objects.get(id=call_id)

        expected_duration = '0h13m43s'
        self.assertEqual(expected_duration, call.duration, msg="Call duration different than expected")

        expected_price = Decimal('0.64')
        self.assertEqual(expected_price, call.price, msg="Call price different than expected")

    def test_case_sample_5(self):
        """
        Sample 5: Start: 2017-12-12 04:57:13 End: 2017-12-12 06:10:56.
        """
        call_id = 74
        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=parse('2017-12-12T04:57:13Z'),
            source="99988526423",
            destination="9933468278",
            call_id=call_id,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=parse('2017-12-12T06:10:56Z'),
            call_id=call_id,
        )

        self.assertEqual(Call.objects.filter(id=call_id).count(), 1, msg="Should create one Call record")
        call = Call.objects.get(id=call_id)

        expected_duration = '1h13m43s'
        self.assertEqual(expected_duration, call.duration, msg="Call duration different than expected")

        expected_price = Decimal('1.88')
        self.assertEqual(expected_price, call.price, msg="Call price different than expected")

    def test_case_sample_6(self):
        """
        Sample 6: Start: 2017-12-12 21:57:13 End: 2017-12-13 22:10:56.
        """
        call_id = 75

        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=parse('2017-12-12T21:57:13Z'),
            source="99988526423",
            destination="9933468278",
            call_id=call_id,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=parse('2017-12-13T22:10:56Z'),
            call_id=call_id,
        )

        self.assertEqual(Call.objects.filter(id=call_id).count(), 1, msg="Should create one Call record")
        call = Call.objects.get(id=call_id)

        expected_duration = '24h13m43s'
        self.assertEqual(expected_duration, call.duration, msg="Call duration different than expected")

        expected_price = Decimal('91.84')
        self.assertEqual(expected_price, call.price, msg="Call price different than expected")

    def test_case_sample_7(self):
        """
        Sample 7: Start: 2017-12-12 15:07:58 End: 2017-12-12 15:12:56.
        """
        call_id = 76

        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=parse('2017-12-12T15:07:58Z'),
            source="99988526423",
            destination="9933468278",
            call_id=call_id,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=parse('2017-12-12T15:12:56Z'),
            call_id=call_id,
        )

        self.assertEqual(Call.objects.filter(id=call_id).count(), 1, msg="Should create one Call record")
        call = Call.objects.get(id=call_id)

        expected_duration = '0h4m58s'
        self.assertEqual(expected_duration, call.duration, msg="Call duration different than expected")

        expected_price = Decimal('0.72')
        self.assertEqual(expected_price, call.price, msg="Call price different than expected")

    def test_case_sample_8(self):
        """
        Sample 8: Start: 2018-02-28 21:57:13 End: 2018-03-01 22:10:56.
        """
        call_id = 76

        # Input a Detail Start Record
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=parse('2018-02-28T21:57:13Z'),
            source="99988526423",
            destination="9933468278",
            call_id=call_id,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=parse('2018-03-01T22:10:56Z'),
            call_id=call_id,
        )

        self.assertEqual(Call.objects.filter(id=call_id).count(), 1, msg="Should create one Call record")
        call = Call.objects.get(id=call_id)

        expected_duration = '24h13m43s'
        self.assertEqual(expected_duration, call.duration, msg="Call duration different than expected")

        expected_price = Decimal('91.84')
        self.assertEqual(expected_price, call.price, msg="Call price different than expected")