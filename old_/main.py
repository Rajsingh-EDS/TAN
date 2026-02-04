import sys
import qrcode
import urllib.parse

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer
from PySide6.QtCore import (
    QObject,
    Property,
    Signal,
    Slot,
    QAbstractListModel,
    Qt,
    QModelIndex,
)
import update_functions as uf
import sort_function as sf


QR_PATH = "/tmp/payment_qr.png"


# =====================================================
# PASSENGER MODEL 
# =====================================================
class PassengerModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    SexRole = Qt.UserRole + 2
    AgeRole = Qt.UserRole + 3
    StatusRole = Qt.UserRole + 4
    
    countChanged = Signal()
   
   # print("no 1 print")
    def __init__(self):
        super().__init__()
        self._passengers =  []
      #  print("no 2 print")

    def rowCount(self, parent=QModelIndex()):
        # Return ALL passengers, not limited to 14
      #  print("no 3 print")
        return len(self._passengers)  # Now returns 18 (or however many you have)

    def data(self, index, role):
        if not index.isValid():
          #  print("no 4 print")
            return None

        passenger = self._passengers[index.row()]
       # print("no 5 print")
        if role == self.NameRole:
            return passenger.get("name", "")
        if role == self.SexRole:
            return passenger.get("sex", "")
        if role == self.AgeRole:
            return passenger.get("age", "")
        if role == self.StatusRole:
            return passenger.get("status", "")

        return None

    def roleNames(self):
       # print("no 6 print")
        return {
            self.NameRole: b"name",
            self.SexRole: b"sex",
            self.AgeRole: b"age",
            self.StatusRole: b"status",
        }

    @Property(int, notify=countChanged)
    def count(self):
        return len(self._passengers)

    def setPassengers(self, passengers: list):
        print(f"Setting {len(passengers)} passengers")

        self.beginResetModel()
        self._passengers = passengers
        self.endResetModel()

        self.countChanged.emit()
        print(f"Model reset with {len(self._passengers)} passengers")

     # ================= NEW: append ONE passenger =================
    @Slot(dict)
    def appendPassenger(self, passenger: dict):
        row = len(self._passengers)
        self.beginInsertRows(QModelIndex(), row, row)
        self._passengers.append(passenger)
        self.endInsertRows()
        self.countChanged.emit()

    # ================= NEW: append LIST of passengers =================
    @Slot(list)
    def appendPassengers(self, passengers: list):
        if not passengers:
            return

        start = len(self._passengers)
        end = start + len(passengers) - 1

        self.beginInsertRows(QModelIndex(), start, end)
        self._passengers.extend(passengers)
        self.endInsertRows()
        self.countChanged.emit()


# =====================================================
# BACKEND 
# =====================================================
class Backend(QObject):
    # ===== signals =====
  #  print("no 8 print")
    stationFromChanged = Signal()
    destinationChanged = Signal()
    trainNoChanged = Signal()
    coachChanged = Signal()
    dateChanged = Signal()
    monthChanged= Signal()
    passengersChanged = Signal()
    classNameChanged = Signal()
    amountChanged = Signal()
    boardingPointChanged = Signal()
    reservationUptoChanged = Signal()
    operatorNameChanged = Signal()
    qrImagePathChanged = Signal()
    terminalIdChanged = Signal()      
    windowNoChanged = Signal()        

    def __init__(self):
        ''' This values are used at first time as default'''
        super().__init__()
      #  print("no 9 print")
        # ===== initial ticket data =====
        self._stationFrom = ""
        self._destination = ""
        self._trainNo = ""
        self._coach = ""
        self._date = ""
        self._month = ""
        self._passengers = ""
        self._className = ""
        self._amount = "₹ 0.00"
        self._boardingPoint = ""
        self._reservationUpto = ""
        self._operatorName = "INDIAN RAILWAYS"
        self._terminalId = "00"    
        self._windowNo = "00"       

        # ===== QR DATA =====
        # Generate initial QR with amount
        self._qrData = self._generateUpiQrData(self._amount)
        self._qrImagePath = ""
        self._generateAndUpdateQR(self._qrData)

    # this functions are called from QML to get the properties values #######

    # ================= QR IMAGE PATH =================
    @Property(str, notify=qrImagePathChanged)
    def qrImagePath(self):
        return self._qrImagePath

    # ================= TICKET PROPERTIES =================
    @Property(str, notify=stationFromChanged)
    def stationFrom(self):
        return self._stationFrom

    @Property(str, notify=destinationChanged)
    def destination(self):
        return self._destination

    @Property(str, notify=trainNoChanged)
    def trainNo(self):
        return self._trainNo

    @Property(str, notify=coachChanged)
    def coach(self):
        return self._coach

    @Property(str, notify=dateChanged)
    def date(self):
        return self._date
    
    @Property(str, notify=monthChanged)
    def month(self):
        return self._month

    @Property(str, notify=passengersChanged)
    def passengers(self):
        return self._passengers

    @Property(str, notify=classNameChanged)
    def className(self):
        return self._className

    @Property(str, notify=amountChanged)
    def amount(self):
        return self._amount

    @Property(str, notify=boardingPointChanged)
    def boardingPoint(self):
        return self._boardingPoint

    @Property(str, notify=reservationUptoChanged)
    def reservationUpto(self):
        return self._reservationUpto

    @Property(str, notify=operatorNameChanged)
    def operatorName(self):
        return self._operatorName

    @Property(str, notify=terminalIdChanged)
    def terminalId(self):
        return self._terminalId

    @Property(str, notify=windowNoChanged)
    def windowNo(self):
        return self._windowNo

    # ================= QR GENERATION =================
    def _generateUpiQrData(self, amount_str: str):
        """Generate UPI QR code data with amount"""
        # Extract numeric value from amount string (remove ₹ symbol and commas)
       # print("no 10 print")
        
        # For UPI QR, we need the amount without currency symbol
        # UPI QR format: upi://pay?pa=<address>&pn=<name>&am=<amount>&tn=<note>&cu=<currency>
        qr_data = (
        ) 
        return qr_data

    def _generateAndUpdateQR(self, qr_data: str):
        """Generate QR code image and update the property"""
       # print("no 11 print")
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(QR_PATH)

        self._qrImagePath = f"file://{QR_PATH}?v={id(qr)}"
        self.qrImagePathChanged.emit()

    # ================= SERVER UPDATE (WITH TERMINAL & WINDOW) =================
    @Slot(dict)
    def updateFromServer(self, data: dict):
        if "from" in data:
            self._stationFrom = data["from"]
            self.stationFromChanged.emit()

        if "to" in data:
            self._destination = data["to"]
            self.destinationChanged.emit()

        if "train_no" in data:
            self._trainNo = data["train_no"]
            self.trainNoChanged.emit()

        if "coach" in data:
            self._coach = data["coach"]
            self.coachChanged.emit()

        if "date" in data:
            self._date = data["date"]
            self.dateChanged.emit()
        
        if "month" in data:
            self._month = data["month"]
            self.monthChanged.emit()

        if "passengers" in data:
            self._passengers = str(data["passengers"])
            self.passengersChanged.emit()

        if "class" in data:
            self._className = data["class"]
            self.classNameChanged.emit()

        if "amount" in data:
            self._amount = data["amount"]
            self.amountChanged.emit()

        if "boarding" in data:
            self._boardingPoint = data["boarding"]
            self.boardingPointChanged.emit()

        if "reservation" in data:
            self._reservationUpto = data["reservation"]
            self.reservationUptoChanged.emit()

        if "operator" in data:
            self._operatorName = data["operator"]
            self.operatorNameChanged.emit()

        if "terminal_id" in data:
            self._terminalId = data["terminal_id"]
            self.terminalIdChanged.emit()

        if "window_no" in data:
            self._windowNo = data["window_no"]
            self.windowNoChanged.emit()

        if "upi_qr" in data:
            # If server provides custom QR data, use it
            self._qrData = data["upi_qr"]
            self._generateAndUpdateQR(self._qrData)
   

# =====================================================
# APP ENTRY
# =====================================================
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    backend = Backend()
    passengerModel = PassengerModel()

    
    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("passengerModel", passengerModel)
    
    engine.load("main.qml")
 
    passengers = [
        {"name": "RAJ SINGH", "sex": "M", "age": "32", "status": "S4 - 11"},
        {"name": "RAJ SINGH", "sex": "M", "age": "32", "status": "S4 - 12"},
        {"name": "RAJ SINGH", "sex": "M", "age": "32", "status": "S4 - 13"},
        {"name": "RAJ SINGH", "sex": "M", "age": "32", "status": "S4 - 14"}
    ]
  
    

    #Call after 5 second delay
    # Clear display after 10 seconds
   # QTimer.singleShot(10000, clear_display)

    # Update passengers after 5 seconds
    # QTimer.singleShot(
    #     5000,
    #     lambda: update_passengers(passengers)
    # )
    # uf.update_passengers_list(passengerModel, [passengers[0]]) # to update single passenger list reset and update
    # QTimer.singleShot(1000, lambda: uf.append_passengers_list(passengerModel, [passengers[1]] )) # append to previous list 
    # QTimer.singleShot(2000, lambda: uf.append_passengers_list(passengerModel, [passengers[2]] ))
    # QTimer.singleShot(3000, lambda: uf.append_passengers_list(passengerModel, [passengers[3]] ))



    # QTimer.singleShot(2000, lambda: uf.update_from(backend, "ndls"))
    # QTimer.singleShot(3000, lambda: uf.update_to(backend, "mas"))
    # QTimer.singleShot(4000, lambda: uf.update_train_no(backend, "12345"))
    # QTimer.singleShot(5000, lambda: uf.update_coach(backend, "S4 - 01"))
    # QTimer.singleShot(6000, lambda: uf.update_date(backend, "20/01"))
    # QTimer.singleShot(7000, lambda: uf.update_passengers_count(backend, "5"))
    # QTimer.singleShot(8000, lambda: uf.update_class(backend, "3A"))
    # QTimer.singleShot(9000, lambda: uf.update_amount(backend, "5500"))
    # QTimer.singleShot(10000, lambda: uf.update_boarding(backend, "whm"))
    # QTimer.singleShot(11000, lambda: uf.update_reservation(backend, "hin"))
    # QTimer.singleShot(12000, lambda: uf.update_operator_name(backend, "rajsingh"))
    # QTimer.singleShot(13000, lambda: uf.update_terminal_id(backend, "1"))
    # QTimer.singleShot(14000, lambda: uf.update_window_no(backend, "2"))

    sf.sort_and_update(backend, passengerModel,"$0126NDLS:NEW DELHI:NEW DELHI:^")
    sf.sort_and_update(backend, passengerModel,"$0219WHM:WASHIM:WASHIM:^")
    sf.sort_and_update(backend, passengerModel,"$0304GBRS:^")
    sf.sort_and_update(backend, passengerModel,"$0404FBRS:^")
    sf.sort_and_update(backend, passengerModel,"$050512345:^")
    sf.sort_and_update(backend, passengerModel,"$0602GN:^")
    sf.sort_and_update(backend, passengerModel,"$070201:^")
    sf.sort_and_update(backend, passengerModel,"$080202:^")
    sf.sort_and_update(backend, passengerModel,"$090207:^")
    sf.sort_and_update(backend, passengerModel,"$1002SL:^")
    sf.sort_and_update(backend, passengerModel,"$1106456789:^")
    sf.sort_and_update(backend, passengerModel,"$1209eds-india:^")
   # sf.sort_and_update(backend, passengerModel,"$1306NDLS99:^")
   # sf.sort_and_update(backend, passengerModel,"$140204:^")
   # QTimer.singleShot(5000,lambda: sf.sort_and_update(backend, passengerModel, "$1503 :^"))
    sf.sort_and_update(backend, passengerModel, "$22201upi://pay?pa=abc@sbi&pn=test&mc=&tr=ref000003&tn=&am=1&cu=INR&url=&mode=05&purpose=03&orgid=159002&sign=MEUCIFa0RLs4mJLK7pSkb5eP69d5Xd6LstvC6xJjSXeQO9HvAiEAzH7T/OYWhaPmraL4VsY6RkVXaBq+He12iRewCOARItI=^"
)
    sf.sort_and_update(backend, passengerModel, "$1316rajsingh chauhan:^")
    QTimer.singleShot(2000, lambda: sf.sort_and_update(backend, passengerModel, "$1401M:^"))
    QTimer.singleShot(4000, lambda: sf.sort_and_update(backend, passengerModel, "$150218:^"))
    QTimer.singleShot(6000, lambda: sf.sort_and_update(backend, passengerModel, "$1607S4 - 12:^"))
    
    QTimer.singleShot(10000, lambda: sf.sort_and_update(backend, passengerModel, "$1308rajsingh:^"))
    QTimer.singleShot(9000, lambda: sf.sort_and_update(backend, passengerModel, "$1401M:^"))
    QTimer.singleShot(8000, lambda: sf.sort_and_update(backend, passengerModel, "$150285:^"))
    QTimer.singleShot(7000, lambda: sf.sort_and_update(backend, passengerModel, "$1607S5 - 17:^"))

    QTimer.singleShot(11000, lambda: sf.sort_and_update(backend, passengerModel, "$1401F:^"))
    QTimer.singleShot(12000, lambda: sf.sort_and_update(backend, passengerModel, "$150216:^"))
    QTimer.singleShot(13000, lambda: sf.sort_and_update(backend, passengerModel, "$1303raj:^"))
    QTimer.singleShot(14000, lambda: sf.sort_and_update(backend, passengerModel, "$1607S5 - 19:^"))

    #QTimer.singleShot(15000, lambda: uf.clear_display(backend, passengerModel))

    sys.exit(app.exec())