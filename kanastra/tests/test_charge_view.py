from datetime import datetime
from django.urls import reverse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from django.urls import get_resolver

from charge.models import Charge


# csv_content = "name,governmentId,email,debtAmount,debtDueDate,debtId\n"
# csv_content += "Elijah Santos,9558,janet95@example.com,7811,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f4fcb3\n"
# csv_content += "Elijah Santos,9558,janet95@example.com,7811,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f4fcb3\n"
# csv_content += "Elijah Santos,9558,janet95@example.com,7811,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f4fcb3\n"
# csv_content += "Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d\n"


class CSVUploadTests(TestCase):

    @pytest.mark.django_db
    def test_upload_csv_success(self):

        csv_content = "name,governmentId,email,debtAmount,debtDueDate,debtId\n"
        csv_content += "Elijah Santos,9558,janet95@example.com,7811,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f4fcb3\n"
        csv_content += "Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d\n"
        csv_content += "Leslie Morgan,9611,russellwolfe@example.net,6177,2022-10-17,9f5a2b0c-967e-4443-a03d-9d7cdcb2216f\n"
        csv_content += "Joseph Rivera,1126,urangel@example.org,7409,2023-08-16,33bec852-beee-477f-ae65-1475c74e1966\n"
        csv_content += "Jessica James,1525,lisa11@example.net,5829,2024-01-18,e2dba21b-5520-4226-82b5-90c6bb3356c6\n"
        csv_content += "Charles Fields,1874,melissa18@example.net,7685,2024-05-12,f94d431b-4629-4880-b4a8-047116ec5fc5\n"
        csv_content += "Kelly Sanchez,7032,erindavis@example.com,5932,2024-05-08,cd3359c9-e5ce-42ef-926d-b28ec70796b3\n"
        csv_content += "Bryan Villarreal,4133,douglasevans@example.net,5235,2024-04-21,674388d1-ebb9-4ec3-8e7e-0776a88bbdc9\n"
        csv_content += "Dennis Davis,7479,angela12@example.com,9269,2022-10-23,a65abc5f-4760-42a5-9dc3-a68526e48a5f\n"
        csv_content += "Crystal Williams,5352,annabrown@example.org,8779,2023-11-19,3f378517-33ba-4dc5-9595-28bd87ca921e\n"

        test_csv = SimpleUploadedFile(
            "test_file.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )

        url = reverse("create-charge")

        charge_count = Charge.objects.all().count()

        assert charge_count == 0

        response = self.client.post(url, {"file": test_csv})

        charge_count = Charge.objects.all().count()

        assert charge_count == 10

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {"message": "CSV processed successfully"},
        )

    @pytest.mark.django_db
    def test_duplicate_from_file_should_insert_2(self):

        csv_content = "name,governmentId,email,debtAmount,debtDueDate,debtId\n"
        csv_content += "Elijah Santos,9558,janet95@example.com,7811,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f4fcb3\n"
        csv_content += "Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d\n"
        csv_content += "Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d\n"
        csv_content += "Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d\n"
        csv_content += "Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d\n"
        csv_content += "Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d\n"

        test_csv = SimpleUploadedFile(
            "test_file.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )

        url = reverse("create-charge")

        charge_count = Charge.objects.all().count()

        assert charge_count == 0

        response = self.client.post(url, {"file": test_csv})

        charge_count = Charge.objects.all().count()

        assert charge_count == 2

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {"message": "CSV processed successfully"},
        )

    @pytest.mark.django_db
    def test_duplicate_from_database_should_insert_4(self):

        csv_content = "name,governmentId,email,debtAmount,debtDueDate,debtId\n"
        csv_content += "Elijah Santos,9558,janet95@example.com,7811,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f4fcb3\n"
        csv_content += "Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d\n"
        csv_content += "Leslie Morgan,9611,russellwolfe@example.net,6177,2022-10-17,9f5a2b0c-967e-4443-a03d-9d7cdcb2216f\n"
        csv_content += "Joseph Rivera,1126,urangel@example.org,7409,2023-08-16,33bec852-beee-477f-ae65-1475c74e1966\n"
        csv_content += "Jessica James,1525,lisa11@example.net,5829,2024-01-18,e2dba21b-5520-4226-82b5-90c6bb3356c6\n"

        Charge.objects.create(
            name="Jessica James",
            government_id="5829",
            email="lisa11@example.net",
            debt_amount=1525,
            debt_due_date=datetime.strptime("2024-01-18", "%Y-%m-%d"),
            debt_id="e2dba21b-5520-4226-82b5-90c6bb3356c6",
        )

        test_csv = SimpleUploadedFile(
            "test_file.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )

        url = reverse("create-charge")

        charge_count = Charge.objects.all().count()

        assert charge_count == 1

        response = self.client.post(url, {"file": test_csv})

        charge_count = Charge.objects.all().count()

        assert charge_count == 5

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {"message": "CSV processed successfully"},
        )

    @pytest.mark.django_db
    def test_upload_csv_no_file(self):
        url = reverse("create-charge")

        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "No file was provided"})

    @pytest.mark.django_db
    def test_upload_csv_invalid_file(self):
        text_content = b"This is not a CSV file."
        test_file = SimpleUploadedFile(
            "test_file.txt", text_content, content_type="text/plain"
        )

        url = reverse("create-charge")

        response = self.client.post(url, {"file": test_file})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "File is not a CSV"})
