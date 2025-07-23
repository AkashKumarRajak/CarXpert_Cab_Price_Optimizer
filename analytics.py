def analyze_data(data, city=None):
    if city:
        city_data = [entry for entry in data if entry.get('city', '').lower() == city.lower()]
    else:
        city_data = data

    available_data = [entry for entry in city_data if entry.get('availability', '').lower() == 'available']

    # Car services (excluding bike and auto)
    car_services = [
        entry for entry in available_data
        if 'bike' not in entry.get('service', '').lower()
        and 'rapido' not in entry.get('service', '').lower()
        and 'auto' not in entry.get('service', '').lower()
    ]

    # Bike services (bike or rapido)
    bike_services = [
        entry for entry in available_data
        if 'bike' in entry.get('service', '').lower() or 'rapido' in entry.get('service', '').lower()
    ]

    # Auto services (auto)
    auto_services = [
        entry for entry in available_data
        if 'auto' in entry.get('service', '').lower()
    ]

    best_car_cab_fare = min(car_services, key=lambda x: x['fare'], default=None)
    best_bike_cab_fare = min(bike_services, key=lambda x: x['fare'], default=None)
    best_auto_fare = min(auto_services, key=lambda x: x['fare'], default=None)

    best_fare_option = min(available_data, key=lambda x: x['fare'], default=None)

    return {
        "best_car_cab_fare_option": best_car_cab_fare,
        "best_bike_cab_fare_option": best_bike_cab_fare,
        "best_auto_fare_option": best_auto_fare,
        "best_fare_option": best_fare_option,
        "total_options_found": len(available_data)
    }
