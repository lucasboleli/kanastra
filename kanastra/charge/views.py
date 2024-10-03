from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets, status
from datetime import datetime
import logging

from charge.models import Charge
import csv


from rest_framework.response import Response
import csv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Q
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

CHUNCK_SIZE = 10000


class ChargeViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response(
                {"error": "No file was provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not csv_file.name.endswith(".csv"):
            return Response(
                {"error": "File is not a CSV"}, status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == "POST":
            file = request.FILES["file"].read().decode("utf-8")
            csv_reader = csv.DictReader(file.splitlines())

            unique_lines = []
            debt_ids = []

            for row in csv_reader:

                if row["debtId"] not in debt_ids:
                    unique_lines.append(row)
                    debt_ids.append(row["debtId"])

                if len(unique_lines) == CHUNCK_SIZE:
                    self.process_chunck(unique_lines, debt_ids)
                    unique_lines = []
                    debt_ids = []

            if unique_lines:
                self.process_chunck(unique_lines, debt_ids)

            return JsonResponse({"message": "CSV processed successfully"}, status=201)

    def process_chunck(self, unique_lines, debt_ids):
        data_chunk = []

        logger.warning(
            f"Processing a chunck of {len(unique_lines)} records from csv file"
        )

        existent_charges = list(
            Charge.objects.filter(debt_id__in=debt_ids).values_list(
                "debt_id", flat=True
            )
        )

        logger.warning(f"Found {len(existent_charges)} duplicates on the database")

        if len(existent_charges) == len(unique_lines):
            return

        for line in unique_lines:
            if UUID(line["debtId"]) not in existent_charges:
                data_chunk.append(
                    Charge(
                        name=line["name"],
                        government_id=line["governmentId"],
                        email=line["email"],
                        debt_amount=int(line["debtAmount"]),
                        debt_due_date=datetime.strptime(
                            line["debtDueDate"], "%Y-%m-%d"
                        ),
                        debt_id=line["debtId"],
                    )
                )

        logger.warning(f"inserting {len(data_chunk)} records into the database")
        with transaction.atomic():
            Charge.objects.bulk_create(data_chunk)
