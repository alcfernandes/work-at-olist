from datetime import datetime
import pytz

from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.validators import ValidationError

from calls.core.models.call import CallDetail


class CallDetailModelTest(TestCase):
    """
    Test Call Detail creation and its __str__
    """
    def setUp(self):
        self.call_detail = CallDetail(
            id=1,
            type=CallDetail.START,
            timestamp="2016-02-29T12:00:00Z",
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )
        self.call_detail.save()

    def test_create(self):
        self.assertTrue(CallDetail.objects.exists())

    def test_str(self):
        self.assertEqual("Call id:70 - Detail id:1 - start on 2016-02-29T12:00:00Z from 99988526423 to 9933468278.",
                         str(self.call_detail))


class CallDetailModelDuplicityTest(TestCase):
    """
    No more than one call detail record of the same type should be accepted for the same call
    """
    def test_type_start_duplicity_same_call_id(self):

        CallDetail.objects.create(
            type=CallDetail.START,
            timestamp="2016-02-29T12:00:00Z",
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        with self.assertRaises(IntegrityError):
            CallDetail.objects.create(
                type=CallDetail.START,
                timestamp="2016-02-29T16:00:00Z",
                source="99988526423",
                destination="9933468278",
                call_id=70,
            )


class CallDetailModelDateTimeOrderValidationTest(TestCase):

    def test_end_before_start_validation(self):
        """
        A end call detail record timestamp should be before than start call detail record timestamp
        """
        CallDetail.objects.create(
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 12, 00, 00, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        with self.assertRaises(ValidationError):
            CallDetail.objects.create(
                type=CallDetail.END,
                timestamp=datetime(2016, 2, 29, 11, 00, 00, tzinfo=pytz.UTC),
                call_id=70,
            )

    def test_start_after_send_validation(self):
        """
        A start call detail record timestamp should be after than end call detail record timestamp
        """
        CallDetail.objects.create(
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 11, 00, 00, tzinfo=pytz.UTC),
            call_id=70,
        )

        with self.assertRaises(ValidationError):
            CallDetail.objects.create(
                type=CallDetail.START,
                timestamp=datetime(2016, 2, 29, 12, 00, 00, tzinfo=pytz.UTC),
                source="99988526423",
                destination="9933468278",
                call_id=70,
            )
