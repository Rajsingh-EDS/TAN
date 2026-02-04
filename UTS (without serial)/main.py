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
 
    sf.sort_and_update(backend, "$0104GBRS:^")
    sf.sort_and_update(backend, "$0204FDZR:^")
    sf.sort_and_update(backend, "$030208:^")
    sf.sort_and_update(backend, "$040210:^")
    sf.sort_and_update(backend, "$050204:^")
    sf.sort_and_update(backend, "$060203:^")
    sf.sort_and_update(backend, "$0701R:^")
    sf.sort_and_update(backend, "$08066871:^")
    sf.sort_and_update(backend, "$0902GN:^")
    sf.sort_and_update(backend, "$1204PART:^")
    sf.sort_and_update(backend, "$1531MUKESH KUMAR GARHWAL:nd9999:123:^")
    sf.sort_and_update(backend, "$1605PAYTM:^")
    sf.sort_and_update(backend, "$22201upi://pay?pa=abc@sbi&pn=test&mc=&tr=ref000003&tn=&am=1&cu=INR&url=&mode=05&purpose=03&orgid=159002&sign=MEUCIFa0RLs4mJLK7pSkb5eP69d5Xd6LstvC6xJjSXeQO9HvAiEAzH7T/OYWhaPmraL4VsY6RkVXaBq+He12iRewCOARItI=^"
)
    gateway = "$2120SBI PAYMENT GATE WAY:^"
    sf.sort_and_update(backend, gateway)
    
    
    #QTimer.singleShot(3000, lambda: sf.sort_and_update(backend, "$13:^"))
    
    
    
    
    sys.exit(app.exec())