"""Testes adicionais: cenários não cobertos pelos testes fornecidos."""

from helpers import run_cli


def test_all_rows_are_read_beyond_200(tmp_path):
    rows = [{"reservation_id": f"R-{i}"} for i in range(250)]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_reservations"] == 250
    assert report["summary"]["total_room_nights"] == 250


def test_nights_across_year_boundary_and_rooms(tmp_path):
    report = run_cli(
        tmp_path,
        [{"checkin_date": "2024-12-30", "checkout_date": "2025-01-02", "rooms": "2"}],
    )
    assert report["summary"]["total_room_nights"] == 6
    assert report["by_month"][0]["month"] == "2024-12"


def test_top_hotels_tie_breaks_by_hotel_id(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H02", "hotel_name": "B", "amount": "100.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "hotel_name": "A", "amount": "100.00"},
        ],
    )
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H01", "H02"]


def test_money_uses_decimal_and_half_up(tmp_path):
    report = run_cli(tmp_path, [{"amount": "0.005"}])
    assert report["summary"]["total_amount_brl"] == "0.01"


def test_no_billable_rows_gives_zero_average(tmp_path):
    report = run_cli(tmp_path, [{"status": "CANCELLED"}])
    assert report["summary"]["average_nightly_rate_brl"] == "0.00"
    assert report["by_month"] == [] and report["top_hotels"] == []


def test_by_month_sorted_and_uses_checkin_month(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "checkin_date": "2025-02-01", "checkout_date": "2025-02-02"},
            {"reservation_id": "R-2", "checkin_date": "2025-01-31", "checkout_date": "2025-02-02"},
        ],
    )
    assert [m["month"] for m in report["by_month"]] == ["2025-01", "2025-02"]
