from django.shortcuts import render
from rest_framework import viewsets, status

from charge.models import Charge
import csv


from rest_framework.response import Response


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

        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)

        for index, row in enumerate(reader):
            if index == 0:  # Skip header
                continue

            name = row[0]
            governmentId = row[1]
            email = row[2]
            debtAmount = row[3]
            debtDueDate = row[4]
            debtId = row[5]

            if not Charge.objects.filter(debtId=debtId).exists():
                Charge.objects.create(
                    name=name,
                    governmentId=governmentId,
                    email=email,
                    debtAmount=debtAmount,
                    debtDueDate=debtDueDate,
                    debtId=debtId,
                )
                print(f"Added {name} ({email}) - {debtId}")
            else:
                print(f"Skipped {debtId}, already exists")

        return Response(
            {"message": "CSV processed successfully"}, status=status.HTTP_200_OK
        )
