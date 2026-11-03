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