# update_functions.py

def clear_display(backend, passengerModel):
    backend.updateFromServer({
        "from": "",
        "to": "",
        "train_no": "",
        "coach": "",
        "date": "",
        "month":"",
        "passengers": 0,
        "class": "",
        "amount": "₹ 0.00",
        "boarding": "",
        "reservation": "",
        "operator": "IRCTC",
        "terminal_id": "00",
        "window_no": "00",
        "upi_qr": " "
    })
    passengerModel.setPassengers([])


def update_passengers_list(passengerModel, passengers):
    print("passenger list updated")
    passengerModel.setPassengers(passengers)

def append_passengers_list(passengerModel, passengers):
    print(f"Appending {len(passengers)} passengers")
    passengerModel.appendPassengers(passengers)




def update_from(backend, station_from):
    backend.updateFromServer({"from": station_from})


def update_to(backend, station_to):
    backend.updateFromServer({"to": station_to})


def update_train_no(backend, train_no):
    backend.updateFromServer({"train_no": train_no})


def update_coach(backend, coach):
    backend.updateFromServer({"coach": coach})


def update_date(backend, date):
    backend.updateFromServer({"date": date})

def update_month(backend, month):
    backend.updateFromServer({"month": month})


def update_passengers_count(backend, count):
    backend.updateFromServer({"passengers": count})


def update_class(backend, class_name):
    backend.updateFromServer({"class": class_name})


def update_amount(backend, amount):
    backend.updateFromServer({"amount": amount})


def update_boarding(backend, boarding):
    backend.updateFromServer({"boarding": boarding})


def update_reservation(backend, reservation):
    backend.updateFromServer({"reservation": reservation})


def update_operator_name(backend, operator):
    backend.updateFromServer({"operator": operator})


def update_terminal_id(backend, terminal_id):
    backend.updateFromServer({"terminal_id": terminal_id})


def update_window_no(backend, window_no):
    backend.updateFromServer({"window_no": window_no})


# ================= QR PARSING =================

def update_qr_string(backend, qr_string: str):
    """
    Update backend with clean UPI QR string
    """
    backend.updateFromServer({
        "upi_qr": qr_string
    })

