from datetime import date, datetime
from math import ceil

import streamlit as st

from data import load_ddays, save_ddays
from phrases import get_phrase


def calc_dday(deadline_str: str) -> int:
	"""Return the day difference between today and the deadline date."""
	deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
	today = date.today()
	return (deadline - today).days


def calc_today_amount(remaining_amount: int, days_left: int) -> int:
	"""Return the amount to do today, rounded up."""
	if days_left <= 0:
		return remaining_amount

	return ceil(remaining_amount / days_left)


def _normalize_ddays(ddays: list[dict]) -> list[dict]:
	normalized_ddays = []
	next_id = 1

	for item in ddays:
		if not isinstance(item, dict):
			continue

		item_id = item.get("id")
		if isinstance(item_id, int):
			next_id = max(next_id, item_id + 1)
		else:
			item_id = next_id
			next_id += 1

		normalized_ddays.append(
			{
				"id": item_id,
				"name": str(item.get("name", "")),
				"deadline": str(item.get("deadline", date.today().isoformat())),
				"total_amount": int(item.get("total_amount", 0)),
				"remaining_amount": int(item.get("remaining_amount", 0)),
			}
		)

	return normalized_ddays


def _next_id(ddays: list[dict]) -> int:
	return max((int(item["id"]) for item in ddays), default=0) + 1


def _format_dday(days_left: int) -> str:
	if days_left > 0:
		return f"D-{days_left}"
	if days_left == 0:
		return "D-day"
	return f"D+{abs(days_left)}"


def _get_status(item: dict, completed_today: bool) -> str:
	if completed_today or int(item["remaining_amount"]) <= 0:
		return "good"

	days_left = calc_dday(item["deadline"])
	if days_left <= 2:
		return "urgent"

	return "normal"


def _load_session_state() -> None:
	today_key = date.today().isoformat()

	if "ddays" not in st.session_state:
		st.session_state.ddays = _normalize_ddays(load_ddays())

	if "completed_today" not in st.session_state:
		st.session_state.completed_today = {}

	if st.session_state.get("session_date") != today_key:
		st.session_state.completed_today = {}
		st.session_state.session_date = today_key


def _persist_ddays() -> None:
	save_ddays(st.session_state.ddays)


def _add_dday(name: str, deadline: date, total_amount: int) -> None:
	new_item = {
		"id": _next_id(st.session_state.ddays),
		"name": name,
		"deadline": deadline.isoformat(),
		"total_amount": int(total_amount),
		"remaining_amount": int(total_amount),
	}
	st.session_state.ddays.append(new_item)
	_persist_ddays()


def _apply_progress(item_id: int, progress_amount: int) -> None:
	for item in st.session_state.ddays:
		if int(item["id"]) != item_id:
			continue

		applied_amount = min(int(progress_amount), int(item["remaining_amount"]))
		days_left = calc_dday(item["deadline"])
		today_target = calc_today_amount(int(item["remaining_amount"]), days_left)

		item["remaining_amount"] = max(0, int(item["remaining_amount"]) - applied_amount)
		st.session_state.completed_today[str(item_id)] = progress_amount >= today_target
		_persist_ddays()
		break


def _delete_dday(item_id: int) -> None:
	st.session_state.ddays = [item for item in st.session_state.ddays if int(item["id"]) != item_id]
	st.session_state.completed_today.pop(str(item_id), None)
	st.session_state.pop(f"progress_{item_id}", None)
	_persist_ddays()


st.set_page_config(page_title="Study With Me", page_icon="📚", layout="wide")
_load_session_state()

st.title("Study With Me")
st.caption("D-day와 오늘 분량을 함께 관리해보세요.")

with st.sidebar:
	st.header("새 D-day 추가")
	with st.form("add_dday_form", clear_on_submit=True):
		name = st.text_input("과제명")
		deadline = st.date_input("마감일", value=date.today())
		total_amount = st.number_input("전체 분량", min_value=1, step=1, value=1)
		submit_add = st.form_submit_button("추가")

	if submit_add:
		clean_name = name.strip()
		if not clean_name:
			st.warning("과제명을 입력해 주세요.")
		else:
			_add_dday(clean_name, deadline, int(total_amount))
			st.success("D-day를 추가했습니다.")
			st.rerun()

sorted_ddays = sorted(st.session_state.ddays, key=lambda item: item["deadline"])

st.subheader("등록된 D-day")

if not sorted_ddays:
	st.info("아직 등록된 D-day가 없습니다. 사이드바에서 첫 과제를 추가해 보세요.")

for item in sorted_ddays:
	item_id = int(item["id"])
	days_left = calc_dday(item["deadline"])
	today_amount = calc_today_amount(int(item["remaining_amount"]), days_left)
	completed_today = bool(st.session_state.completed_today.get(str(item_id), False))
	status = _get_status(item, completed_today)
	phrase = get_phrase(status)
	dday_label = _format_dday(days_left)
	progress_key = f"progress_{item_id}"

	with st.expander(f"{item['name']} · {dday_label}", expanded=True):
		left_col, right_col = st.columns(2)
		with left_col:
			st.metric("D-day", dday_label)
		with right_col:
			st.metric("오늘 해야 할 분량", today_amount)

		st.write(f"마감일: {item['deadline']}")
		st.write(f"전체 분량: {int(item['total_amount'])}")
		st.write(f"남은 분량: {int(item['remaining_amount'])}")
		st.markdown(f"> {phrase}")

		progress_input_col, action_col = st.columns([3, 2])
		with progress_input_col:
			progress_amount = st.number_input(
				"오늘 진행한 분량",
				min_value=0,
				step=1,
				value=int(st.session_state.get(progress_key, 0)),
				key=progress_key,
			)
		with action_col:
			st.write(" ")
			apply_clicked = st.button("반영하기", key=f"apply_{item_id}")
			delete_clicked = st.button("삭제", key=f"delete_{item_id}")

		if apply_clicked:
			_apply_progress(item_id, int(progress_amount))
			st.session_state[progress_key] = 0
			st.rerun()

		if delete_clicked:
			_delete_dday(item_id)
			st.rerun()
