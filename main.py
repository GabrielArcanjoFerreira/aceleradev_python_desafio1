from datetime import datetime as dt
from datetime import timedelta as td


# Base of calls
records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]

# Important to keep all fees as we may need them
DAY_PERMANENT_RATE = 0.36
NIGHT_PERMANENT_RATE = 0.36
DAY_ADD_PER_MINUTE = 0.09
NIGHT_ADD_PER_MINUTE = 0.00
START_DAYTIME = 6
END_DAYTIME = 22


# Main function
def classify_by_phone_number(records):
    """Returns the base of calls received
    in the format: [{"source": "phone_number", "total": "bill_value"}]

    >>> classify_by_phone_number([{
        'source': '48-996355555',
        'destination': '48-666666666',
        'end': 1564610974,
        'start': 1564610674
    }])
    [{"source": "48-996355555", "total": 128.99}]

    :param records: Base of calls
    :return: List of dictionaries grouped by phone number and account value
    """
    records_tarifado = {}  # Destination dictionary that will contain the number and tariff

    for record in records:
        start_call = record["start"]
        end_call = record["end"]
        source_number = record["source"]

        # Calculate the account value
        account = __calculate_account(start_call, end_call)
        records_tarifado[source_number] = round((records_tarifado.setdefault(source_number, 0) + account), 2)

    records = [{"source": record, "total": records_tarifado[record]} for record in records_tarifado]
    records.sort(reverse=True, key=lambda tarifa: tarifa["total"])

    print(records)

    return records


def __calculate_account(start_call, end_call, ):
    """Returns the account value of a call

    :param start_call: Start of the connection
    :param end_call: End of the connection
    :param call_duration: Duration time per call in minutes
    :return: The account value
    """
    account = 0

    # Defines the start of a call, the end and the duration time
    start = dt.fromtimestamp(start_call)
    end = dt.fromtimestamp(end_call)
    call_duration = int(((end - start).total_seconds())/60)

    account = __check_shift(start, account)

    # checks if the call duration is over 1 minute
    if call_duration >= 1:
        for minute in range(1, call_duration + 1):
            rated_time = start + td(minutes=minute)

            account += __check_shift(rated_time, account)

    return account


def __check_shift(rated_time, account):
    """Returns the correct value for the current shift

    :param rated_time: current time
    :return: fare amount
    """
    value = 0

    # checks the current shift
    if START_DAYTIME <= rated_time.hour < END_DAYTIME:
        if account != 0:
            value = DAY_ADD_PER_MINUTE
        else:
            value = DAY_PERMANENT_RATE
    else:
        if account != 0:
            value = NIGHT_ADD_PER_MINUTE
        else:
            value = NIGHT_PERMANENT_RATE

    return value


if __name__ == "__main__":
    classify_by_phone_number(records)