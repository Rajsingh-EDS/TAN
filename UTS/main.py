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
import sort_function as sf
from PySide6.QtCore import QThread
import serial

QR_PATH = "/tmp/payment_qr.png"
# =====================================================
# Serial Connections
# =====================================================
class SerialWorker(QThread):
    def __init__(self, backend,
                 port="/dev/ttyUSB0",
                 baud=115200):
        super().__init__()
        self.backend = backend
        self.port = port
        self.baud = baud
        self._running = True
        self.ser = None   # 👈 keep reference

    def run(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                timeout=0.5
            )
        except Exception as e:
            print("❌ Serial open failed:", e)
            return

        buffer = b""

        while self._running:
            data = self.ser.read(self.ser.in_waiting or 1)
            if data:
                print("RAW BYTES:", data)
            
            if not data:
                continue

            buffer += data

            while b'^' in buffer:
                frame_bytes, buffer = buffer.split(b'^', 1)
                frame_bytes += b'^'

                try:
                    frame = frame_bytes.decode(errors="ignore")
                    print("FRAME:", frame)
                    sf.sort_and_update(self.backend, frame)
                except Exception as e:
                    print("Serial parse error:", e)

        # 👇 clean close
        if self.ser:
            self.ser.close()
            self.ser = None

    def stop(self):
        self._running = False


# =====================================================
# BACKEND 
# =====================================================
class Backend(QObject):
    # ===== signals =====
  #  print("no 8 print")
    stationFromChanged = Signal()
    destinationChanged = Signal()
    dateChanged = Signal()
    monthChanged= Signal()
    amountChanged = Signal()
    operatorNameChanged = Signal()
    qrImagePathChanged = Signal()
    terminalIdChanged = Signal()      
    windowNoChanged = Signal() 
    adultChanged = Signal()
    childChanged = Signal()
    typeOfTrainChanged = Signal()
    paymodeChanged = Signal()     
    classNameChanged = Signal()
    transactiontypeChanged = Signal()
    paymentgatewayChanged = Signal()

    def __init__(self):
        ''' This values are used at first time as default'''
        super().__init__()
      #  print("no 9 print")
        # ===== initial ticket data =====
        self._stationFrom = ""
        self._destination = ""
        self._date = ""
        self._month = ""
        self._adult = ""
        self._child = ""
        self._className = ""
        self._type_of_train = ""
        self._paymode = ""
        self._amount = "₹ 0.00"
        self._operatorName = "INDIAN RAILWAYS"
        self._terminalId = "00"    
        self._windowNo = "00"
        self._transactiontype = ""  
        self._paymentgateway = ""     

        # ===== QR DATA =====
        # Generate initial QR with amount
        self._qrData = self._generateUpiQrData(self._amount)
        self._qrImagePath = ""
        self._generateAndUpdateQR(self._qrData)



        # ===== SERIAL START =====
        self.serialWorker = SerialWorker(
            backend=self,
            port="/dev/ttyUSB0",
            baud=115200
        )
        self.serialWorker.start()

    


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

    @Property(str, notify=dateChanged)
    def date(self):
        return self._date
    
    @Property(str, notify=monthChanged)
    def month(self):
        return self._month

    @Property(str, notify=classNameChanged)
    def className(self):
        return self._className

    @Property(str, notify=amountChanged)
    def amount(self):
        return self._amount
    
    @Property(str, notify=childChanged)
    def child(self):
        return self._child
    
    @Property(str, notify=adultChanged)
    def adult(self):
        return self._adult
    
    @Property(str, notify=paymodeChanged)
    def paymode(self):
        return self._paymode
    
    @Property(str, notify=typeOfTrainChanged)
    def type_of_train(self):
        return self._type_of_train
    

    @Property(str, notify=operatorNameChanged)
    def operatorName(self):
        return self._operatorName

    @Property(str, notify=terminalIdChanged)
    def terminalId(self):
        return self._terminalId

    @Property(str, notify=windowNoChanged)
    def windowNo(self):
        return self._windowNo
    
    @Property(str, notify=transactiontypeChanged)
    def transactiontype(self):
        return self._transactiontype
    
    @Property(str, notify=paymentgatewayChanged)
    def paymentgateway(self):
        return self._paymentgateway
    
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

        if "date" in data:
            self._date = data["date"]
            self.dateChanged.emit()
        
        if "month" in data:
            self._month = data["month"]
            self.monthChanged.emit()

        if "paymode" in data:
            self._paymode = str(data["paymode"])
            self.paymodeChanged.emit()

        if "type_of_train" in data:
            self._type_of_train = data["type_of_train"]
            self.typeOfTrainChanged.emit()

        if "amount" in data:
            self._amount = data["amount"]
            self.amountChanged.emit()

        if "adult" in data:
            self._adult = data["adult"]
            self.adultChanged.emit()

        if "child" in data:
            self._child = data["child"]
            self.childChanged.emit()

        if "class" in data:
            self._className = data["class"]
            self.classNameChanged.emit()

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
        
        if "transactiontype" in data:
            self._transactiontype = data["transactiontype"]
            self.transactiontypeChanged.emit()
            
        if "paymentgateway" in data:
            self._paymentgateway = data["paymentgateway"]
            self.paymentgatewayChanged.emit()
   

# =====================================================
# APP ENTRY
# =====================================================
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    backend = Backend()
   
    engine.rootContext().setContextProperty("backend", backend)
    
    engine.load("main.qml")
 
    def cleanup():
        backend.serialWorker.stop()
        backend.serialWorker.wait()   

    app.aboutToQuit.connect(cleanup)

    sys.exit(app.exec())