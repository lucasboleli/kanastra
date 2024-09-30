import csv
from django.core.management.base import BaseCommand

from charge.models import Charge


class Command(BaseCommand):
    help = "Import data from CSV file into the Charge model"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="The path to the CSV file to import"
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        # Open the CSV file
        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Assuming the CSV has 'name' and 'email' columns
                name = row["name"]
                governmentId = row["governmentId"]
                email = row["email"]
                debtAmount = row["debtAmount"]
                debtDueDate = row["debtDueDate"]
                debtId = row["debtId"]

                # Check for duplicates by email and avoid inserting if it exists
                if not Charge.objects.filter(debtId=debtId).exists():
                    Charge.objects.create(
                        name=name,
                        governmentId=governmentId,
                        email=email,
                        debtAmount=debtAmount,
                        debtDueDate=debtDueDate,
                        debtId=debtId,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Added {name} ({email}) - {debtId}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Skipped {debtId}, already exists")
                    )
