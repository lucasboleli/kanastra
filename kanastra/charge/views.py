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


class ChargeViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        CHUNCK_SIZE = 50000
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

            data_chunk = []
            unique_lines = []
            debt_ids = []

            for row in csv_reader:
                # Verifica duplicados na lista
                if row["debtId"] not in debt_ids:
                    unique_lines.append(row)  # Adiciona a linha ao conjunto
                    debt_ids.append(row["debtId"])

            logger.warning(
                f"Foram encontrados {len(unique_lines)} registros no arquivo csv"
            )

            # Verifica duplicados no banco com uma query
            existent_charges = list(
                Charge.objects.filter(debt_id__in=debt_ids).values_list(
                    "debt_id", flat=True
                )
            )

            logger.warning(
                f"Foram encontrados {len(existent_charges)} registros ja inseridos no banco de dados"
            )

            for line in unique_lines:
                if UUID(line["debtId"]) not in existent_charges:
                    # logger.warning(f'Encontrado id unico -> {line["debtId"]}')
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

                # Quando atingir o chunk, insere no banco
                if len(data_chunk) == CHUNCK_SIZE:
                    logger.warning(
                        f"Inserindo chunck de {CHUNCK_SIZE} registros no banco"
                    )
                    with transaction.atomic():
                        Charge.objects.bulk_create(data_chunk)
                    data_chunk = []

            # Insere o que sobrou no último chunk
            if data_chunk:
                logger.warning(f"Inserindo {len(data_chunk)} registros no banco")
                with transaction.atomic():
                    Charge.objects.bulk_create(data_chunk)

            return JsonResponse({"message": "CSV processed successfully"}, status=201)
