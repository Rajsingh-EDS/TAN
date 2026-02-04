
def clear_display(backend):
    backend.updateFromServer({
        "from": "",
        "to": "",
        "date": "",
        "month":"",
        "child":"",
        "adult":"",
        "type_of_train":"",
        "paymode":"",  
        "amount": "₹ 0.00",
        "operator": "IRCTC",
        "terminal_id": "00",
        "window_no": "00",
        "type_of_train":"",
        "transctiontype":"",
        "paymentgateway":"",
        "upi_qr": " "
    })



def update_from(backend, station_from):
    backend.updateFromServer({"from": station_from})

def update_to(backend, station_to):
    backend.updateFromServer({"to": station_to})

def update_date(backend, date):
    backend.updateFromServer({"date": date})

def update_month(backend, month):
    backend.updateFromServer({"month": month})

def update_child(backend, child):
    backend.updateFromServer({"child":child})

def update_adult(backend, adult):
    backend.updateFromServer({"adult":adult})

def update_paymode(backend, paymode):
    backend.updateFromServer({"paymode":paymode})

def update_train_type(backend, train_type):
    backend.updateFromServer({"type_of_train":train_type})

def update_class(backend, class_name):
    backend.updateFromServer({"class": class_name})


def update_amount(backend, amount):
    backend.updateFromServer({"amount": amount})


def update_operator_name(backend, operator):
    backend.updateFromServer({"operator": operator})


def update_terminal_id(backend, terminal_id):
    backend.updateFromServer({"terminal_id": terminal_id})


def update_window_no(backend, window_no):
    backend.updateFromServer({"window_no": window_no})
    
def update_transactiontype(backend, transactiontype):
    backend.updateFromServer({"transactiontype": transactiontype})

def update_paymentgateway(backend, paymentgateway):
    backend.updateFromServer({"paymentgateway": paymentgateway})

# ================= QR PARSING =================

def update_qr_string(backend, qr_string: str):
    """
    Update backend with clean UPI QR string
    """
    backend.updateFromServer({
        "upi_qr": qr_string
    })
