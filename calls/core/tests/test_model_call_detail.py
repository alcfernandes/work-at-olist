from django.test import TestCase
from django.db.utils import IntegrityError

from calls.core.models.call import CallDetail


class CallDetailModelTest(TestCase):
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

    def test_type_start_duplicity_same_call_id(self):
        """
        No more than one call detail record of the same type should be accepted for the same call
        """
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
