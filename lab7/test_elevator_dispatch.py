from hypothesis import given, strategies as st
from elevator_dispatch import parse_request, total_travel, load_percent

# Anything a user (or another program) might hand us: text, None, numbers, bytes, lists...
anything = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(),
    st.binary(),
    st.lists(st.integers()),
)

# Inputs shaped like the real formats, with junk mixed in
floors = st.integers(min_value=-1000, max_value=1000)
junk = st.text(alphabet="0123456789-> ,of\t\n_.x", max_size=20)


# ---------- parse_request ----------
@given(st.text() | st.none())
def test_parse_request_no_crash(s):
    try:
        parse_request(s)
    except Exception as e:
        assert False, f"parse_request crashed with: {e!r}"


@given(anything | junk)
def test_parse_request_returns_none_or_int_pair(s):
    result = parse_request(s)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and all(isinstance(x, int) for x in result)
    )


@given(floors, floors)
def test_parse_request_valid_roundtrip(a, b):
    assert parse_request(f"{a}->{b}") == (a, b)


# ---------- total_travel ----------
@given(st.text() | st.none())
def test_total_travel_no_crash(s):
    try:
        total_travel(s)
    except Exception as e:
        assert False, f"total_travel crashed with: {e!r}"


@given(anything | junk)
def test_total_travel_returns_none_or_nonnegative_int(s):
    result = total_travel(s)
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.lists(floors, min_size=1, max_size=30))
def test_total_travel_valid_matches_manual_sum(fl):
    expected = sum(abs(fl[i + 1] - fl[i]) for i in range(len(fl) - 1))
    assert total_travel(",".join(map(str, fl))) == expected


# ---------- load_percent ----------
@given(st.text() | st.none())
def test_load_percent_no_crash(s):
    try:
        load_percent(s)
    except Exception as e:
        assert False, f"load_percent crashed with: {e!r}"


@given(anything | junk)
def test_load_percent_returns_none_or_nonnegative_int(s):
    result = load_percent(s)
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.integers(min_value=0, max_value=10**6), st.integers(min_value=1, max_value=10**6))
def test_load_percent_valid_matches_formula(load, cap):
    assert load_percent(f"{load} of {cap}") == load * 100 // cap


def test_load_percent_zero_capacity_is_handled():
    assert load_percent("5 of 0") is None
