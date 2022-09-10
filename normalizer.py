
def normalize_data(data, weights):
    if not weights["norm_factor"]:
        max_km = max(data, key=lambda e: e["km"])["km"]
        max_price = max(data, key=lambda e: e["price"])["price"]
        weights["norm_factor"] = max(max(max_km, max_price), 1)

    new_data = []
    for car in data:
        new_car = {"km": car["km"] / weights["norm_factor"], "price": car["price"] / weights["norm_factor"]}
        new_data.append(new_car)
    return new_data
