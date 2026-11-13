def parse_request(text):
    """Parse 'FROM->TO' into (from_floor, to_floor). Returns None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split('->')
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def total_travel(floors_csv):
    """Total floors travelled for a CSV of floors. Returns None if invalid."""
    if not isinstance(floors_csv, str):
        return None
    try:
        floors = [int(f) for f in floors_csv.split(',')]
    except ValueError:
        return None
    return sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))


def load_percent(text):
    """Parse 'X of Y' and return X as a whole percent of Y. Returns None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split(' of ')
    if len(parts) != 2:
        return None
    try:
        load, capacity = int(parts[0]), int(parts[1])
    except ValueError:
        return None
    if load < 0 or capacity <= 0:
        return None
    return load * 100 // capacity


def main():
    print("==== Running parse_request ====")
    user_input = input("Enter a request as FROM->TO (e.g. 5->9): ")
    result = parse_request(user_input)
    print("From and To:", result if result is not None else "Invalid input")

    print("\n==== Running total_travel ====")
    user_input = input("Enter floors visited as CSV (e.g. 1,5,3,9): ")
    result = total_travel(user_input)
    print("Floors Travelled:", result if result is not None else "Invalid input")

    print("\n==== Running load_percent ====")
    user_input = input("Enter load as 'X of Y' (e.g. 450 of 630): ")
    result = load_percent(user_input)
    print("Load Percent:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
