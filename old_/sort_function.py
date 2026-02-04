# sort_function.py

import update_functions as uf

# ================= PASSENGER COLLECTOR =================

MAX_PASSENGERS = 10   # ← change to 7,8,9 later if needed

_passenger_count = 0


def parse_framed_string(raw_string: str):
    """
    Parse framed protocol string:
    $ + 2-digit code + 3-digit length + data + ^
    """
    if not raw_string.startswith("$") or not raw_string.endswith("^"):
        raise ValueError("Invalid framing")

    payload = raw_string#[1:-1]

    if len(payload) < 5:
        raise ValueError("Payload too short")

    code = payload[1:3]
    #print("code:",code)
    length_str = payload[3:6]
    #print("len string:",length_str)

    if not length_str.isdigit():
        raise ValueError("Invalid length field")

    data_length = int(length_str)
    # print("payload length:",len(payload))
    # print("data length",data_length)
    # print("payload:",payload)
    if len(payload) < 6 + data_length:
        raise ValueError("Payload length mismatch")
    
    data = payload[6:6 + data_length]
    #print("data:",data)
    return data


def sort_station_string(raw_string: str):
    """
    Protocol:
    $ + 2-digit code + 2-digit length + data + :^
    Length INCLUDES ':^'
    """

    if not raw_string.startswith("$"):
        raise ValueError("Invalid framing (missing $)")

    if "^" not in raw_string:
        raise ValueError("Invalid framing (missing ^)")

    # Remove ONLY '$'
    payload = raw_string[1:]

    if len(payload) < 4:
        raise ValueError("Payload too short")

    code = payload[:2]          # "01"
    length_str = payload[2:4]   # "26"

    if not length_str.isdigit():
        raise ValueError("Invalid length field")

    data_length = int(length_str)

    if len(payload) < 4 + data_length:
        raise ValueError("Payload length mismatch")

    # Extract exactly length bytes (includes ':^')
    raw_data = payload[4:4 + data_length]

    # Now safely strip protocol tail
    if raw_data.endswith(":^"):
        raw_data = raw_data[:-2]
    elif raw_data.endswith(":"):
        raw_data = raw_data[:-1]

    parts = raw_data.split(":")

    station_code = parts[0]
    english_name = ""
    hindi_name = ""

    if len(parts) >= 2:
        english_name = parts[1]

    if len(parts) >= 3:
        # Join remaining parts in case ':' appears inside name
        hindi_name = ":".join(parts[2:])

    # print("Station Code :", station_code)
    # print("English Name :", english_name)
    # print("Hindi Name   :", hindi_name)

    return station_code

def sort_and_update(backend, passengerModel, raw_string: str):
    """
    Sort incoming framed string by code
    and route to correct update function
    """
    try:
        if not raw_string.startswith("$") or not raw_string.endswith("^"):
            raise ValueError("Invalid framing")     
        
        payload = raw_string[1:-1]
       # print("len of payload:",len(payload),payload)
        if len(payload) < 4:
            raise ValueError("Payload too short")
        
        code = payload[:2]
        
        if code == "01":
            data = sort_station_string(raw_string)
            uf.update_from(backend, data)
        elif code == "02":
            data = sort_station_string(raw_string)
            uf.update_to(backend, data)
        elif code == "03":                           # chagne based on actual reservation status code
            data = sort_station_string(raw_string)
            uf.update_reservation(backend, data)
        elif code == "04":                           # change based on actual boarding point status code
            data = sort_station_string(raw_string)
            uf.update_boarding(backend, data)
        elif code == "05":                           # change based on actual train no status code
            data = sort_station_string(raw_string)
            uf.update_train_no(backend, data)
        elif code == "06":                           # change based on actual coach(Quota) status
            data = sort_station_string(raw_string)
            uf.update_coach(backend, data)
        elif code == "07":                           # change based on actual date status code
            data = sort_station_string(raw_string)
            uf.update_date(backend, data)
        elif code == "08":                          # change based on actual month status code
            data = sort_station_string(raw_string)
            uf.update_month(backend, data)
        elif code == "09":                          # change based on actual passenger count status code
            data = sort_station_string(raw_string)
            uf.update_passengers_count(backend, data)
        elif code == "10":                          # change based on actual class status code
            data = sort_station_string(raw_string)
            uf.update_class(backend, data)
        elif code == "11":                          # change based on actual fare/amount status code
            data = sort_station_string(raw_string)
            uf.update_amount(backend, data)
        elif code == "12":                          # change based on actual operator name status code
            data = sort_station_string(raw_string)
            uf.update_operator_name(backend, data)
        # elif code == "13":                          # change based on actual Terminal id status code
        #     data = sort_station_string(raw_string)
        #     uf.update_terminal_id(backend, data)
        # elif code == "14":                          # change based on actual window no status code
        #     data = sort_station_string(raw_string)
        #     uf.update_window_no(backend, data)
        # elif code == "15":                          # change based on actual clear display status code
        #     uf.clear_display(backend, passengerModel)
     
     
        elif code in ("13", "14", "15", "16"):
            field_map = {
                "13": "name",
                "14": "sex",
                "15": "age",
                "16": "status",
            }

            role_map = {
                "name": passengerModel.NameRole,
                "sex": passengerModel.SexRole,
                "age": passengerModel.AgeRole,
                "status": passengerModel.StatusRole,
            }

            field = field_map[code]
            value = sort_station_string(raw_string)

            # Ensure fixed number of passengers exist
            _ensure_passengers(passengerModel)

            # -------- NAME logic --------
            if field == "name":
                for row in range(MAX_PASSENGERS):
                    if passengerModel._passengers[row]["name"] == "-":
                        passengerModel._passengers[row]["name"] = value
                        passengerModel.dataChanged.emit(
                            passengerModel.index(row, 0),
                            passengerModel.index(row, 0),
                            [role_map["name"]]
                        )
                        break

            # -------- SEX / AGE / STATUS logic --------
            else:
                for row in range(MAX_PASSENGERS):
                    if passengerModel._passengers[row][field] == "-":
                        passengerModel._passengers[row][field] = value
                        passengerModel.dataChanged.emit(
                            passengerModel.index(row, 0),
                            passengerModel.index(row, 0),
                            [role_map[field]]
                        )
                        break




        
     
     
     
     
     
     
     
        elif code == "22":
            data = parse_framed_string(raw_string)
            uf.update_qr_string(backend, data)
    except ValueError as e:
        print("QR parse error:", e)
        return



def _ensure_passengers(passengerModel):
    global _passenger_count

    while _passenger_count < MAX_PASSENGERS:
        passenger = {
            "name": "-",
            "sex": "-",
            "age": "-",
            "status": "-"
        }
        uf.append_passengers_list(passengerModel, [passenger])
        _passenger_count += 1
