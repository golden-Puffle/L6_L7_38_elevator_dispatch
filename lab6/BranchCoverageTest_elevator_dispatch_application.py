import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---------- Starter examples ----------
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"


def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


# ---------- next_direction ----------
def test_up_continues_up_when_requests_above():
    assert next_direction(3, "up", [5]) == "up"


def test_up_reverses_down_when_only_requests_below():
    assert next_direction(3, "up", [1]) == "down"


def test_down_continues_down_when_requests_below():
    assert next_direction(3, "down", [1]) == "down"


def test_down_reverses_up_when_only_requests_above():
    assert next_direction(3, "down", [5]) == "up"


def test_idle_goes_up_when_request_above():
    assert next_direction(3, "idle", [5]) == "up"


def test_idle_goes_down_when_request_below():
    assert next_direction(3, "idle", [1]) == "down"


# ---------- door_action ----------
def test_overload_door():
    assert door_action(700, False, False) == "overload"


def test_blocked_door_reopens():
    assert door_action(100, True, False) == "reopen"


def test_normal_door_closes():
    assert door_action(100, False, False) == "close"


# ---------- pick_elevator ----------
def test_pick_nearest_idle_car():
    cars = [("A", 1, True), ("B", 5, False)]
    assert pick_elevator(cars, 2) == "A"


# ================= Extra tests for BRANCH coverage =================

# next_direction: every "else/no requests" path
def test_up_with_no_requests_goes_idle():
    assert next_direction(3, "up", []) == "idle"


def test_down_with_no_requests_goes_idle():
    assert next_direction(3, "down", []) == "idle"


# Boundary: request on the current floor is neither above nor below
@pytest.mark.parametrize("direction", ["up", "down", "idle"])
def test_request_at_current_floor_is_idle(direction):
    assert next_direction(3, direction, [3]) == "idle"


def test_up_with_requests_on_both_sides_keeps_going_up():
    assert next_direction(5, "up", [2, 8]) == "up"


def test_down_with_requests_on_both_sides_keeps_going_down():
    assert next_direction(5, "down", [2, 8]) == "down"


def test_unknown_direction_treated_like_idle():
    assert next_direction(5, "stopped", [8]) == "up"


# door_action: priorities and the 630 kg boundary
def test_load_exactly_630_is_not_overload():
    assert door_action(630, False, False) == "close"


def test_load_631_is_overload():
    assert door_action(631, False, False) == "overload"


def test_emergency_overrides_overload():
    assert door_action(900, True, True) == "hold_open"


def test_overload_overrides_blocked():
    assert door_action(900, True, False) == "overload"


# pick_elevator
def test_pick_no_cars_returns_none():
    assert pick_elevator([], 4) is None


def test_pick_single_car():
    assert pick_elevator([("A", 9, False)], 1) == "A"


def test_idle_farther_car_beats_closer_busy_car():
    # A busy: 1 + 5 = 6, B idle: 2  -> B wins (later car replaces best)
    cars = [("A", 2, False), ("B", 5, True)]
    assert pick_elevator(cars, 3) == "B"


def test_tie_returns_first_car():
    cars = [("A", 1, True), ("B", 3, True)]
    assert pick_elevator(cars, 2) == "A"


def test_all_busy_picks_closest():
    cars = [("A", 10, False), ("B", 4, False)]
    assert pick_elevator(cars, 5) == "B"