""" helper functions for reading and writing CSV files. """
import csv
import io


def read_csv_from_upload(uploaded_file) -> list:
    """Reads a Django UploadedFile into a list of dict rows (csv.DictReader)."""
    decoded = uploaded_file.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    return [row for row in reader]


def write_csv_response(rows: list, fieldnames: list) -> str:
    """Builds CSV text content from a list of dicts — used for CSV download/export."""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fieldnames})
    return buffer.getvalue()
