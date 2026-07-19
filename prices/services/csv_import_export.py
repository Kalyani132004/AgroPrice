
from core.utils.csv_utils import read_csv_from_upload, write_csv_response
from core.utils.datetime_utils import parse_csv_date
from core.utils.regex_validators import validate_crop_name, validate_quality, validate_price, ValidationError
from db.repositories.price_repository import PriceRepository
from prices.domain.price_record import PriceRecord

REQUIRED_COLUMNS = {"crop_name", "market", "price", "quality", "date"}


class CSVImportResult:
    def __init__(self):
        self.success_count = 0
        self.error_rows = []  # list of (row_number, reason)

    def add_error(self, row_number: int, reason: str):
        self.error_rows.append({"row": row_number, "reason": reason})


class CSVImportExportService:
    def __init__(self):
        self.repo = PriceRepository()

    def import_prices(self, uploaded_file) -> CSVImportResult:
        result = CSVImportResult()
        try:
            rows = read_csv_from_upload(uploaded_file)
        except Exception as exc:  # noqa: BLE001
            result.add_error(0, f"Could not read CSV file: {exc}")
            return result

        if not rows:
            result.add_error(0, "CSV file is empty.")
            return result

        missing_cols = REQUIRED_COLUMNS - set(rows[0].keys())
        if missing_cols:
            result.add_error(0, f"Missing required column(s): {', '.join(missing_cols)}")
            return result

        valid_documents = []
        for i, row in enumerate(rows, start=2):  # row 1 is header
            try:
                crop_name = validate_crop_name(row["crop_name"])
                quality = validate_quality(row["quality"])
                price = validate_price(row["price"])
                date = parse_csv_date(row["date"])
                record = PriceRecord(
                    crop_name=crop_name, market=row["market"].strip().title(),
                    price=price, quality=quality, date=date,
                )
                valid_documents.append(record.to_dict())
            except (ValidationError, ValueError, KeyError) as exc:
                result.add_error(i, str(exc))

        if valid_documents:
            try:
                self.repo.insert_many(valid_documents)
                result.success_count = len(valid_documents)
            except Exception as exc:  # noqa: BLE001
                result.add_error(0, f"Bulk insert failed: {exc}")

        return result

    def export_prices(self, crop_name: str = None) -> str:
        """Returns CSV text of all (or filtered) price records."""
        query = {"crop_name": crop_name} if crop_name else {}
        docs = self.repo.find(query, sort=[("date", -1)])
        rows = []
        for d in docs:
            rows.append({
                "crop_name": d.get("crop_name"),
                "market": d.get("market"),
                "price": d.get("price"),
                "quality": d.get("quality"),
                "date": d.get("date").strftime("%Y-%m-%d") if hasattr(d.get("date"), "strftime") else d.get("date"),
            })
        return write_csv_response(rows, fieldnames=["crop_name", "market", "price", "quality", "date"])
