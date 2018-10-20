from datetime import datetime, time
import pytz

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
