from datetime import datetime
from math import ceil


def calc_dday(deadline_str: str) -> int:
	"""Return the day difference between today and the deadline date."""
	deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
	today = datetime.today().date()
	return (deadline - today).days


def calc_today_amount(remaining_amount: int, days_left: int) -> int:
	"""Return the amount to do today, rounded up."""
	if days_left <= 0:
		return remaining_amount

	return ceil(remaining_amount / days_left)
