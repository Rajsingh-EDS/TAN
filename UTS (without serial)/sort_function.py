# sort_function.py

import update_functions as uf


def sort_qr_string(raw_string: str):
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

    code = payload[:2]  
   # print("code:",code)# "01"
    length_str = payload[2:4]   # "26"
   # print("length str:",length_str)

    if not length_str.isdigit():
        raise ValueError("Invalid length field")

    data_length = int(length_str)
    # print("data length:",data_length)
    # print("payload:",payload)
    # print("len of payload:",len(payload))
    # print("len of 4 + data length:",4 + data_length)
    if len(payload) < 4 + data_length:
        raise ValueError("Payload (actual data) length mismatch")

    # Extract exactly length bytes (includes ':^')
    raw_data = payload[4:4 + data_length]

   # print("raw data:",raw_data)
    
    # Now safely strip protocol tail
    if raw_data.endswith(":^"):
        raw_data = raw_data[:-2]
    elif raw_data.endswith(":"):
        raw_data = raw_data[:-1]

    parts = raw_data.split(":")
    
   # print("parts:",parts)

    station_code = parts[0]
   # print("station code:",station_code)
    english_name = ""
    hindi_name = ""

    if len(parts) >= 2:
        english_name = parts[1]

    if len(parts) >= 3:
        # Join remaining parts in case ':' appears inside name
        hindi_name = ":".join(parts[2:])
        
    if code == "15":
        ''' RETURN THIS WHEN STATUS CODE IS 15 
            station_code as Operator name
            english_name as Terminal ID
            hindi name as Window No'''
        return station_code, english_name, hindi_name
    
    return station_code

def sort_and_update(backend, raw_string: str):
    """
    Sort incoming framed string by code
    and route to correct update function
    """
    try:
        if not raw_string.startswith("$") or not raw_string.endswith("^"):
            raise ValueError("Invalid framing")     
        
        payload = raw_string[1:-1]
       # print("len of payload:",len(payload),payload)
        if len(payload) < 3:
            raise ValueError("Payload too short")
        
        code = payload[:2]
        
        if code == "01":
            data = sort_station_string(raw_string)
            uf.update_from(backend, data)
            
        elif code == "02":
            data = sort_station_string(raw_string)
            uf.update_to(backend, data)

        elif code == "03":
            data = sort_station_string(raw_string)
            uf.update_date(backend, data)
        
        elif code == "04":
            data = sort_station_string(raw_string)
            uf.update_month(backend, data)
        
        elif code == "05":
            data = sort_station_string(raw_string)
            uf.update_adult(backend, data)
            
        elif code == "06":
            data = sort_station_string(raw_string)
            uf.update_child(backend, data)
        
        elif code == "07":
            t_type = sort_station_string(raw_string)
            data = check_type_of_train(t_type)
            uf.update_train_type(backend, data)
        
        elif code == "08":
            data = sort_station_string(raw_string)
            uf.update_amount(backend, data)
        
        elif code == "09":
            data = sort_station_string(raw_string)
            uf.update_class(backend, data)
        
        elif code == "12":
            t_code = sort_station_string(raw_string)
            data = check_transaction_type(t_code)
            uf.update_transactiontype(backend, data)
        
        elif code == "13":                         
            uf.clear_display(backend)    
        
        elif code == "15":
            operator_name, terminal_id, window_no = sort_station_string(raw_string)
            uf.update_operator_name(backend, operator_name)
            uf.update_terminal_id(backend, terminal_id)
            uf.update_window_no(backend, window_no)
            
        elif code == "16":                      # change paymode code based on actual code 
            data = sort_station_string(raw_string)
            uf.update_paymode(backend, data)
        
        elif code == "21":
            data = sort_station_string(raw_string)
            uf.update_paymentgateway(backend, data)
        
        
        elif code == "22":
            data = sort_qr_string(raw_string)
            uf.update_qr_string(backend, data)
    except ValueError as e:
        print("QR parse error:", e)
        return

def check_type_of_train(data):
    mapping = {
                "O": "Ordinary",
                "E": "Express",
                "S": "Superfast",
                "T": "MMTS",
                "C": "Combined",
                "R": "Rajdhani",
                "D": "Shatabdi",
                "M": "Mahamana SF",
                "H": "Darjilling Hill",
                "J": "Jan Shatabdi",
                "P": "Premium SPL",
            }
    type_of_train = mapping.get(data, data)
    return type_of_train    

def check_transaction_type(t_code):
    mapping = {
        "SPLC": "Special Cancel",
        "PLAT": "Platform",
        "NI": "Non-Issue",
        "CANC": "Cancellation",
        "ST": "Season Ticket",
        "BPT": "BPT Ticket",
        "SF": "Superfast Ticket",
        "JRNY": "Journey Ticket",
        "CARD": "I Card",
        "MMQT": "Multiple MST-QST",
        "RRTT": "RAIL/TOURIST",
        "PART": "Partial Cancel"
    }
    data = mapping.get(t_code, "INVALID")
    return data