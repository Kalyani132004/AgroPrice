from django.core.management.base import BaseCommand

from prices.services.price_service import PriceService


class Command(BaseCommand):
    help = "Fetch live mandi prices from Agmarknet API and store them in MongoDB"

    def handle(self, *args, **options):
        service = PriceService()

        self.stdout.write("Starting live mandi price synchronization...")

        try:
            inserted = service.sync_live_prices()

            if inserted > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully synced {inserted} live mandi price record(s)."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "No new records were inserted. Either the API returned no data, duplicate records were skipped, or the API is currently unavailable."
                    )
                )

        except Exception as exc:
            self.stdout.write(
                self.style.ERROR(
                    f"Sync failed: {exc}"
                )
            )