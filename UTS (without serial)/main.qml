import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    id: root
    width: 1280
    height: 720
    visible: true
    color: "#000000"
    title: "UPI Payment"

    Rectangle {
        id: background
        anchors.fill: parent
        color: "#0B1C2D"
        border.color: "#C9A24D"
        border.width: 2

        /*
         * ============================
         * MAIN CONTENT LAYER
         * ============================
         */
        Item {
            anchors.fill: parent
            anchors.margins: 10

            // ================= IMAGE AT TOP RIGHT CORNER =================
            Image {
                id: topRightImage
                source: "image.png"
                width: 200  // Adjust size as needed
                height: 180  // Adjust size as needed
                fillMode: Image.PreserveAspectFit
                smooth: true
                
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.topMargin: 5
                anchors.rightMargin: -10
            }

            // ================= HEADER =================
            Rectangle {
                id: header
                width: parent.width - topRightImage.width - 230// Adjust width to accommodate image
                height: 100
                color: "#0B1C2D"
                // border.color: "#6b1b1b"
                // border.width: 2

                anchors.top: parent.top
                anchors.topMargin: 100
                anchors.left: parent.left
                anchors.leftMargin: 0
                
                Text {
                    anchors.centerIn: parent
                    text: "Ticket Information"
                    font.pixelSize: Math.min(90, parent.height * 1)
                    font.bold: true
                    color: "#FFFFFF"
                }
            }

            // ================= TERMINAL ID & WINDOW NO BOX (TOP RIGHT) =================
            Rectangle {
                id: terminalWindowBox
                width: 200   // Same width as image
                height: 100
                color: "#0B1C2D"
                // border.color: "#6b1b1b"
                // border.width: 2
                
                // Position it between header and image in the top-right space
                anchors.top: parent.top
                anchors.topMargin: 5
                anchors.left: parent.left
                anchors.leftMargin:10
                // anchors.right: topRightImage.left
                // anchors.rightMargin: 10

                Column {
                    anchors.centerIn: parent
                    spacing: 8
                    width: parent.width 

                    // Terminal ID Section
                    Column {
                        width: parent.width
                        spacing: 2

                        Text {
                            text: "Terminal ID"
                            font.pixelSize: 20
                            color: "#C9A24D"
                            font.bold: true
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        Rectangle {
                            width: parent.width
                            height: 1
                            color: "#C9A24D"
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        Text {
                            text: backend ? backend.terminalId : "T1234"
                            font.pixelSize: 22
                            color: "#C9A24D"
                            font.bold: true
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }

                    // Window No Section
                    Column {
                        width: parent.width
                        spacing: 2

                        Text {
                            text: "Window No."
                            font.pixelSize: 20
                            color: "#C9A24D"
                            font.bold: true
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        Rectangle {
                            width: parent.width
                            height: 1
                            color: "#C9A24D"
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        Text {
                            text: backend ? backend.windowNo : "W01"
                            font.pixelSize: 22
                            color: "#C9A24D"
                            font.bold: true
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }
                }
            }
          

            // ================ Starting Point Row =================
            Item {
                id: stationRow
                anchors.top: header.bottom
                anchors.topMargin: -10
                anchors.left: parent.left
                anchors.right: parent.right
                height: 70
                
                // Width calculations: labels fixed width, station boxes take remaining space
                property real totalSpacing: 30 // 10px margin between each box
                property real availableWidth: parent.width - totalSpacing
                property real labelWidth: 180 // Fixed width for labels
                property real remainingWidth: availableWidth - (labelWidth * 2) // Subtract both labels
                property real stationBoxWidth: remainingWidth / 2 // Divide remaining space between station boxes

                // Starting Point Label (Box 1 - Fixed text, fixed width)
                Rectangle {
                    id: startingPoint
                    width: parent.labelWidth
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: parent.left

                    Text {
                        anchors.centerIn: parent
                        text: "From\nकहाँ से"
                        font.pixelSize: 28
                        color: "#0B1C2D"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.WordWrap
                    }
                }

                // First Station Box (Box 2 - Dynamic data, takes available space)
                Rectangle {
                    id: stationfromBox
                    width: parent.stationBoxWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: startingPoint.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.stationFrom : ""
                        font.pixelSize: Math.min(36, parent.height * 0.6)
                        color: "#FFFFFF"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                        fontSizeMode: Text.HorizontalFit
                        minimumPixelSize: 24
                    }
                }

                // Destination Label (Box 3 - Fixed text, fixed width)
                Rectangle {
                    id: destination
                    width: parent.labelWidth
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: stationfromBox.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: "To\nकहाँ तक"
                        font.pixelSize: 28
                        color: "#0B1C2D"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.WordWrap
                    }
                }

                // Destination Station Box (Box 4 - Dynamic data, takes available space)
                Rectangle {
                    id: destinationBox
                    width: parent.stationBoxWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: destination.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.destination : ""
                        font.pixelSize: Math.min(36, parent.height * 0.6)
                        color: "#FFFFFF"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                        fontSizeMode: Text.HorizontalFit
                        minimumPixelSize: 24
                    }
                }
            }

            // ================= Date, Passengers, Class, Fare, Amount Row =================
 
            Item {
                id: datePassengerRow
                anchors.top: stationRow.bottom
                anchors.topMargin: 15
                anchors.left: parent.left
                anchors.right: parent.right
                height: 70
                
                // We have 7 total elements
                property real totalBoxes: 7
                property real totalMargins: 6 * 10 // 6 margins of 10px each
                
                property real availableWidth: parent.width - totalMargins
                
                // Fixed widths
                property real labelWidth: 100 // Date and Fare labels
                property real fixedBoxWidth: 180 // Date value and Class boxes
                property real amountBoxWidth: Math.max(350, availableWidth * 0.30) // Amount box
                
                // Calculate passenger labels box width
                property real totalFixedWidth: (labelWidth * 2) + (fixedBoxWidth * 2) + amountBoxWidth
                property real passengerLabelsWidth: Math.max((availableWidth - totalFixedWidth) * 0.5, 90)
                property real passengerValuesWidth: Math.max((availableWidth - totalFixedWidth) * 0.5, 90)

                // Date Label (Box 1)
                Rectangle {
                    id: date_label
                    width: parent.labelWidth
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: parent.left

                    Text {
                        anchors.centerIn: parent
                        text: "Date\nदिनांक"
                        font.pixelSize: 28
                        color: "#0B1C2D"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.WordWrap
                    }
                }

                // Date Value Box (Box 2)
                Rectangle {
                    id: dateBox
                    width: parent.fixedBoxWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: date_label.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: backend ? (backend.date + " / " + backend.month) : ""
                        font.pixelSize: Math.min(28, parent.height * 0.5)
                        color: "#ffffff"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                }

                // Passenger Labels Box (Box 3) - Contains Adult and Child labels
                Rectangle {
                    id: passengerLabelsBox
                    width: parent.passengerLabelsWidth
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: dateBox.right
                    anchors.leftMargin: 10

                    Column {
                        anchors.fill: parent
                        spacing: 0

                        // Adult Label
                        Rectangle {
                            id: adultLabel
                            width: parent.width
                            height: parent.height / 2
                            color: "#E6EEF5"
                            border.color: "#0B1C2D"
                            border.width: 1

                            Text {
                                anchors.centerIn: parent
                                text: "Adult"
                                font.pixelSize: 24
                                color: "#0B1C2D"
                                font.bold: true
                            }
                        }

                        // Child Label
                        Rectangle {
                            id: childLabel
                            width: parent.width
                            height: parent.height / 2
                            color: "#E6EEF5"
                            border.color: "#2A3F55"
                            border.width: 1

                            Text {
                                anchors.centerIn: parent
                                text: "Child"
                                font.pixelSize: 24
                                color: "#0B1C2D"
                                font.bold: true
                            }
                        }
                    }
                }

                // Passenger Values Box (Box 4) - Contains Adult and Child values
                Rectangle {
                    id: passengerValuesBox
                    width: parent.passengerValuesWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: passengerLabelsBox.right
                    anchors.leftMargin: 10

                    Column {
                        anchors.fill: parent
                        spacing: 0

                        // Adult Value
                        Rectangle {
                            id: adultValue
                            width: parent.width
                            height: parent.height / 2
                            color: "#0B1C2D"
                            border.color: "#2A3F55"
                            border.width: 1

                            Text {
                                id: adultValueText
                                anchors.centerIn: parent
                                text: backend ? backend.adult : ""
                                font.pixelSize: 26
                                color: "#ffffff"
                                font.bold: true
                            }
                        }

                        // Child Value
                        Rectangle {
                            id: childValue
                            width: parent.width
                            height: parent.height / 2
                            color: "#0B1C2D"
                            border.color: "#2A3F55"
                            border.width: 1

                            Text {
                                id: childValueText
                                anchors.centerIn: parent
                                text: backend ? backend.child : ""
                                font.pixelSize: 26
                                color: "#ffffff"
                                font.bold: true
                            }
                        }
                    }
                }

                // Class Box (Box 5) - Contains Class label and value
                Rectangle {
                    id: classBox
                    width: parent.fixedBoxWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: passengerValuesBox.right
                    anchors.leftMargin: 10

                    Column {
                        anchors.centerIn: parent
                        spacing: 4

                        Text {
                            text: "Class"
                            font.pixelSize: Math.min(24, parent.parent.height * 0.35)
                            color: "#ffffff"
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        Rectangle {
                            width: parent.parent.width * 0.8
                            height: 2
                            color: "#ffffff"
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        Text {
                            text: backend ? backend.className : ""
                            font.pixelSize: Math.min(26, parent.parent.height * 0.4)
                            color: "#ffffff"
                            font.bold: true
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                // Fare Label (Box 6)
                Rectangle {
                    id: fareBox
                    width: parent.labelWidth 
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: classBox.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: "Fare\nकिराया"
                        font.pixelSize: 28
                        color: "#0B1C2D"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.WordWrap
                    }
                }

                // Amount Box (Box 7)
                Rectangle {
                    id: amountBox
                    width: parent.amountBoxWidth
                    height: parent.height
                    color: "#C9792B"
                    border.color: "#0B1C2D"
                    border.width: 2
                    anchors.left: fareBox.right
                    anchors.leftMargin: 10
                    anchors.right: parent.right

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.amount : ""
                        font.pixelSize: Math.min(36, parent.height * 0.6)
                        color: "#ffffff"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                        fontSizeMode: Text.HorizontalFit
                        minimumPixelSize: 24
                    }
                }
            }
           
            // ================= Type of rain / PayMode =================
            Item {
                id: boardingReservationRow
                anchors.top: datePassengerRow.bottom
                anchors.topMargin: 50
                anchors.left: parent.left
                anchors.right: parent.right
                height: 70
                
                // We have 5 elements: boardingLabel, boardingValue, reservationLabel, reservationValue, and QR space
                property real totalMargins: 4 * 10 // 4 margins of 10px each
                property real availableWidth: parent.width - totalMargins - amountBox.width 
                
                // Fixed widths for labels
                property real boardingLabelWidth: 185
                property real reservationLabelWidth: 185
                
                // Remaining width for both value boxes after labels
                property real remainingWidth: availableWidth - boardingLabelWidth - reservationLabelWidth
                
                // Both value boxes share remaining width (50% each or adjustable ratio)
                property real boardingValueWidth: remainingWidth * 0.5  // 40% of remaining space
                property real reservationValueWidth: remainingWidth * 0.5  // 60% of remaining space

                // ---- Boarding Point LABEL ----
                Rectangle {
                    id: boardingLabel
                    width: parent.boardingLabelWidth 
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.top: parent.top
                    anchors.left: parent.left

                    Text {
                        anchors.centerIn: parent
                        text: "Type of Train\nट्रेन का प्रकार"
                        font.pixelSize: 26
                        color: "#0B1C2D"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                // ---- Boarding Station VALUE ----
                Rectangle {
                    id: boardingValue
                    width: parent.boardingValueWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.top: parent.top
                    anchors.left: boardingLabel.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.type_of_train : ""
                        font.pixelSize: 26
                        color: "#ffffff"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                }

                // ---- Reservation Up To LABEL ----
                Rectangle {
                    id: reservationLabel
                    width: parent.reservationLabelWidth 
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.top: parent.top
                    anchors.left: boardingValue.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: "Pay Mode"
                        font.pixelSize: 26
                        color: "#0B1C2D"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                // ---- Reservation Station VALUE (FLEXIBLE, STOPS BEFORE QR) ----
                Rectangle {
                    id: reservationValue
                    width: parent.reservationValueWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.top: parent.top
                    anchors.left: reservationLabel.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.paymode : ""
                        font.pixelSize: 26
                        color: "#ffffff"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                }
            }

            // ================= Transaction Type ===================
            Item {
                id: transactionRow
                anchors.top: boardingReservationRow.bottom
                anchors.topMargin: 50
                anchors.left: parent.left
                anchors.right: parent.right
                height: 70

                property real totalMargins: 4 * 10   // label + 2 values = 4 gaps
                property real availableWidth: parent.width - totalMargins - amountBox.width

                property real labelWidth: 185
                property real remainingWidth: availableWidth - labelWidth
                property real valueWidth: remainingWidth * 0.5
                property real blankwidth: remainingWidth * 0.5

                // ---- Transaction Type LABEL ----
                Rectangle {
                    id: transactionLabel
                    width: parent.labelWidth
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: parent.left

                    Text {
                        anchors.centerIn: parent
                        text: "Transaction Type"
                        font.pixelSize: 22
                        color: "#0B1C2D"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                // ---- Transaction Type VALUE ----
                Rectangle {
                    id: transactionValue
                    width: parent.valueWidth - 90
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: transactionLabel.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.transactiontype : ""
                        font.pixelSize: 26
                        color: "#ffffff"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                }

                // ---- Transaction BLANK VALUE ----
                Rectangle {
                    id: transcationblankvalue
                    width: parent.blankwidth + 100
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: transactionValue.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.paymentgateway : ""
                        font.pixelSize: 26
                        color: "#ffffff"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }

            // ================= QR CODE BOX =================
            Rectangle {
                id: qrBox
                width: amountBox.width  // Same width as amount box
                height: parent.height - datePassengerRow.y - datePassengerRow.height - 80  // Responsive height
                color: "#F4F6F8"
                border.color: "#CBD5E1"
                border.width: 2

                // Position below amount box with 5px spacing
                anchors.top: datePassengerRow.bottom
                anchors.topMargin: 5
                anchors.right: parent.right

                Image {
                    anchors.centerIn: parent
                    source: backend ? backend.qrImagePath : ""
                    width: Math.min(parent.width - 20, parent.height - 20)
                    height: Math.min(parent.width - 20, parent.height - 20)
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                }
            }

            // ================= OPERATOR ROW =================
            Item {
                id: operatorRow
                anchors.top: qrBox.bottom
                anchors.topMargin: 5  // 5px margin below QR box
                anchors.left: parent.left
                anchors.right: parent.right
                height: 70
                
                // We have 3 elements: operatorName, operatorNameValue, and footerLabel
                property real totalMargins: 2 * 10 // 2 margins of 10px each
                property real availableWidth: parent.width - totalMargins - footerLabel.width 
                
                // Fixed width for operator label
                property real operatorLabelWidth: 180
                
                // Operator value takes remaining space before footerLabel
                property real operatorValueWidth: availableWidth - operatorLabelWidth

                Rectangle {
                    id: operatorName
                    width: parent.operatorLabelWidth
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter

                    Text {
                        anchors.centerIn: parent
                        text: "Operator\nName"
                        font.pixelSize: 28
                        font.bold: true
                        color: "#0B1C2D"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                Rectangle {
                    id: operatorNameValue
                    width: parent.operatorValueWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: operatorName.right
                    anchors.leftMargin: 10
                    anchors.verticalCenter: parent.verticalCenter

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.operatorName : ""
                        font.pixelSize: 28
                        color: "#ffffff"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                }
            }

            // ================= FOOTER LABEL =================
            Rectangle {
                id: footerLabel
                width: amountBox.width  // Same width as amount box
                height: 70
                color: "#E6EEF5"
                border.color: "#2A3F55"
                border.width: 2

                // Position at bottom with 10px margin, 5px above that is QR box
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.right: parent.right

                Column {
                    anchors.centerIn: parent
                    spacing: 2
                    width: parent.width - 20

                    Text {
                        text: "North Eastern Railway"
                        font.pixelSize: 24
                        font.bold: true
                        color: "#0B1C2D"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: "#2A3F55"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Text {
                        text: "वाराणसी मंडल"
                        font.pixelSize: 20
                        font.bold: true
                        color: "#0B1C2D"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }
            }
        }
    }
}