import sys
import time
import serial
import qrcode
import urllib.parse

import sort_function as sf  

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import (
    QObject,
    Property,
    Signal,
    Slot,
    QAbstractListModel,
    Qt,
    QModelIndex,
    QThread,
    QMetaObject,
    Q_ARG,
)


QR_PATH = "/tmp/payment_qr.png"
# =====================================================
# Serial Connections
# =====================================================

class SerialWorker(QThread):
    def __init__(self, backend, passengerModel,
                 port="/dev/ttyUSB0",
                 baud=115200):
        super().__init__()
        self.backend = backend
        self.passengerModel = passengerModel
        self.port = port
        self.baud = baud
        self._running = True
        self.ser = None


    def run(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                timeout=0.1
            )
        except Exception as e:
            print("❌ Serial open failed:", e)
            return

        buffer = b""
        last_rx_time = time.time()
        FRAME_GAP = 0.3   # 300 ms silence = end of frame

        while self._running:
            data = self.ser.read(self.ser.in_waiting or 1)

            if data:
                buffer += data
                last_rx_time = time.time()
                continue

            # no data → check silence gap
            if buffer and (time.time() - last_rx_time) > FRAME_GAP:
                try:
                    frame = buffer.decode(errors="ignore")
                    print("FRAME:", frame)

                    QMetaObject.invokeMethod(
                        self.backend,
                        "onSerialFrame",
                        Qt.QueuedConnection,
                        Q_ARG(str, frame)
                    )
                    
                except Exception as e:
                    print("Parse error:", e)

                buffer = b""  # reset

        if self.ser:
            self.ser.close()

    def stop(self):
        self._running = False



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
    _operator_code_changed = Signal()      
    windowNoChanged = Signal()        

    def __init__(self, passengerModel):
        super().__init__()
        ''' This values are used at first time as default'''
        self.passengerModel = passengerModel
       
    
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
        self._operator_code = "CLIENT"    
          

        # ===== QR DATA =====
        # Generate initial QR with amount
        self._qrData = self._generateUpiQrData(self._amount)
        self._qrImagePath = ""
        self._generateAndUpdateQR(self._qrData)


        # ===== SERIAL START =====
        self.serialWorker = SerialWorker(
            backend=self,
            passengerModel=self.passengerModel,
            port="/dev/ttyUSB0",
            baud=115200
        )
        self.serialWorker.start()
    # this functions are called from QML to get the properties values #######

    # ================== to update via serial =========
    @Slot(str)
    def onSerialFrame(self, frame):
        sf.sort_and_update(self, self.passengerModel, frame)



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

    @Property(str, notify=_operator_code_changed)
    def operator_code(self):
        return self._operator_code



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

        if "operator_code" in data:
            self._operator_code = data["operator_code"]
            self._operator_code_changed.emit()

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

    passengerModel = PassengerModel()      # 👈 FIRST
    backend = Backend(passengerModel)      # 👈 THEN backend

    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("passengerModel", passengerModel)

    engine.load("main.qml")

    #sf.sort_and_update(backend, passengerModel, "thPRS02111Q174$01:12345$02:21$03:01$04:WHM$05:3A$06:SS$07:GKD$08:8$09:HYD$10:NDLS$11:NDLS99$12:EDS-INDIA$13:5500$14:SANJAY MALHAN$15:M$16:60$17:B3 , 17(LB)$18:NIRMALA M$19:F$20:80$21:B3 , 20(LB)$22:pratap tyagi$23:M$24:25$25:B1 , 19(MB)$26:aman$27:M$28:28$29:B1 , 19(MB)$30:yogesh mishra$31:M$32:22$33:3A , 89(ML)$34:virat kohli$35:M$36:25$37:3E , 67(SL)$38:abd$39:M$40:21$41:SL , 45(UB)$42:rohit sharma$43:M$44:26$45:3A , 23(SU)$46:upi://pay?pa=abc@sbi&pn=test&mc=&tr=ref000003&tn=&am=1&cu=INR&url=&mode=05&purpose=03&orgid=159002&sign=MEUCIFa0RLs4mJLK7pSkb5eP69d5Xd6LstvC6xJjSXeQO9HvAiEAzH7T/OYWhaPmraL4VsY6RkVXaBq+He12iRewCOARItI=$47:01$48:suc")

    def cleanup():
        backend.serialWorker.stop()
        backend.serialWorker.wait()

    app.aboutToQuit.connect(cleanup)

    sys.exit(app.exec())
