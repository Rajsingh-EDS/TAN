import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    id: root
    width: 1280
    height: 820
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
                width: 120  // Adjust size as needed
                height: 120  // Adjust size as needed
                fillMode: Image.PreserveAspectFit
                smooth: true
                
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.topMargin: 0
                anchors.rightMargin: 0
            }

            // ================= HEADER =================
            Rectangle {
                id: header
                width: parent.width - topRightImage.width - 200 // Adjust width to accommodate image
                height: 120
                color: "#0B1C2D"
                // border.color: "#6b1b1b"
                // border.width: 2

                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.left: parent.left
                
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
                height: 120
                color: "#0B1C2D"
                // border.color: "#6b1b1b"
                // border.width: 2
                
                // Position it between header and image in the top-right space
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.right: topRightImage.left
                anchors.rightMargin: 10

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
                anchors.topMargin: 5
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

            // ================= Train number and coach Row =================
            Item {
                id: trainRow
                anchors.top: stationRow.bottom
                anchors.topMargin: 5
                anchors.left: parent.left
                anchors.right: parent.right
                height: 70
                
                // Width calculations: labels fixed width, value boxes take remaining space
                property real totalSpacing: 30 // 10px margin between each box
                property real availableWidth: parent.width - totalSpacing
                property real labelWidth: 180 // Fixed width for labels
                property real remainingWidth: availableWidth - (labelWidth * 2) // Subtract both labels
                property real valueBoxWidth: remainingWidth / 2 // Divide remaining space between value boxes

                // Train No. Label (Box 1 - Fixed text, fixed width)
                Rectangle {
                    id: train_no
                    width: parent.labelWidth
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: parent.left

                    Text {
                        anchors.centerIn: parent
                        text: "Train No.\nगाड़ी संख्या"
                        font.pixelSize: 28
                        color: "#0B1C2D"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.WordWrap
                    }
                }

                // Train No. Value Box (Box 2 - Dynamic data, takes available space)
                Rectangle {
                    id: trainNoBox
                    width: parent.valueBoxWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: train_no.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.trainNo : ""
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

                // Quota Label (Box 3 - Fixed text, fixed width)
                Rectangle {
                    id: quota
                    width: parent.labelWidth
                    height: parent.height
                    color: "#E6EEF5"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: trainNoBox.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: "Quota\nकोटा"
                        font.pixelSize: 28
                        color: "#0B1C2D"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.WordWrap
                    }
                }

                // Coach Value Box (Box 4 - Dynamic data, takes available space)
                Rectangle {
                    id: coachBox
                    width: parent.valueBoxWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2

                    anchors.left: quota.right
                    anchors.leftMargin: 10

                    Text {
                        anchors.centerIn: parent
                        text: backend ? backend.coach : ""
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

            // ================= Date, Passengers, Class, Fare, Amount Row =================
            Item {
                id: datePassengerRow
                anchors.top: trainRow.bottom
                anchors.topMargin: 5
                anchors.left: parent.left
                anchors.right: parent.right
                height: 70
                
                // We have 6 total elements: dateLabel, dateBox, passengerBox, classBox, fareLabel, amountBox
                property real totalBoxes: 6
                property real totalMargins: 5 * 10 // 5 margins of 10px each
                
                property real availableWidth: parent.width - totalMargins
                
                // Fixed widths
                property real labelWidth: 100 // Date and Fare labels
                property real fixedBoxWidth: 180 // Date value and Class boxes
                property real amountBoxWidth: Math.max(350, availableWidth * 0.30) // Amount box
                
                // Calculate passenger box width: total available width minus all other boxes
                property real totalFixedWidth: (labelWidth * 2) + (fixedBoxWidth * 2) + amountBoxWidth
                property real passengerBoxWidth: Math.max(availableWidth - totalFixedWidth, 180)

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
                        text:backend ? (backend.date + " / " + backend.month) : ""
                        font.pixelSize: Math.min(28, parent.height * 0.5)
                        color: "#ffffff"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                }

                // Passengers Box (Box 3)
                Rectangle {
                    id: passengerlist
                    width: parent.passengerBoxWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: dateBox.right
                    anchors.leftMargin: 10

                    Column {
                        anchors.centerIn: parent
                        spacing: 4

                        Text {
                            text: "Total Passengers"
                            font.pixelSize: Math.min(22, parent.parent.height * 0.32)
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
                            text: backend ? backend.passengers : ""
                            font.pixelSize: Math.min(24, parent.parent.height * 0.38)
                            color: "#ffffff"
                            font.bold: true
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                // Class Box (Box 4)
                Rectangle {
                    id: classBox
                    width: parent.fixedBoxWidth
                    height: parent.height
                    color: "#0B1C2D"
                    border.color: "#2A3F55"
                    border.width: 2
                    anchors.left: passengerlist.right
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

                // Fare Label (Box 5)
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

                // Amount Box (Box 6)
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

            // ================= BOARDING / RESERVATION ROW =================
            Item {
                id: boardingReservationRow
                anchors.top: datePassengerRow.bottom
                anchors.topMargin: 5
                anchors.left: parent.left
                anchors.right: parent.right
                height: 70
                
                // We have 5 elements: boardingLabel, boardingValue, reservationLabel, reservationValue, and QR space
                property real totalMargins: 4 * 10 // 4 margins of 10px each
                property real availableWidth: parent.width - totalMargins - amountBox.width 
                
                // Fixed widths for labels
                property real boardingLabelWidth: 160
                property real reservationLabelWidth: 160
                
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
                        text: "Boarding\nPoint"
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
                        text: backend ? backend.boardingPoint : ""
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
                        text: "Reservation\nUp To"
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
                        text: backend ? backend.reservationUpto : ""
                        font.pixelSize: 26
                        color: "#ffffff"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
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

            // ================= PASSENGER INFO HEADER ROW =================
            Item {
                id: passengerInfoRow
                anchors.top: boardingReservationRow.bottom
                anchors.topMargin: 5
                anchors.left: parent.left
                anchors.right: qrBox.left
                anchors.rightMargin: 265
                
                height: 30
                
                // We have 4 elements: name, sex, age, status
                // Width distribution: name - 55%, sex - 15%, age - 15%, status - 25%
                property real totalMargins: 0  // No margins between boxes
                property real availableWidth: width - totalMargins
                
                // Calculate widths based on percentages
                property real nameBoxWidth: availableWidth * 0.51  // 51%
                property real sexBoxWidth: availableWidth * 0.12   // 12%
                property real ageBoxWidth: availableWidth * 0.12   // 12%
                property real statusBoxWidth: availableWidth * 0.21  // 25%

                // Passenger Name Label (Box 1 - 51%)
                Rectangle {
                    id: passengerInfoBox
                    width: parent.nameBoxWidth
                    height: parent.height
                    color: "#ffffff"
                    border.color: "#ffffff"
                    border.width: 0.5

                    anchors.left: parent.left

                    Text {
                        anchors.centerIn: parent
                        text: "Passenger Name"
                        font.pixelSize: Math.min(24, parent.height * 0.6)
                        font.bold: true
                        color: "#6b1b1b"
                        elide: Text.ElideRight
                    }
                }

                // Sex Label (Box 2 - 12%)
                Rectangle {
                    id: passengersex
                    width: parent.sexBoxWidth
                    height: parent.height
                    color: "#ffffff"
                    border.color: "#ffffff"
                    border.width: 0.5

                    anchors.left: passengerInfoBox.right

                    Text {
                        anchors.centerIn: parent
                        text: "Sex"
                        font.pixelSize: Math.min(24, parent.height * 0.6)
                        color: "#6b1b1b"
                        font.bold: true
                        elide: Text.ElideRight
                    }
                }

                // Age Label (Box 3 - 12%)
                Rectangle {
                    id: passengerage
                    width: parent.ageBoxWidth
                    height: parent.height
                    color: "#ffffff"
                    border.color: "#ffffff"
                    border.width: 0.5
                    
                    anchors.left: passengersex.right

                    Text {
                        anchors.centerIn: parent
                        text: "Age"
                        font.pixelSize: Math.min(24, parent.height * 0.6)
                        color: "#6b1b1b"
                        font.bold: true
                        elide: Text.ElideRight
                    }
                }

                // Status Label (Box 4 - 25%)
                Rectangle {
                    id: passengerstatus
                    width: parent.statusBoxWidth
                    height: parent.height
                    color: "#ffffff"
                    border.color: "#ffffff"
                    border.width: 0.5
                    
                    anchors.left: passengerage.right

                    Text {
                        anchors.centerIn: parent
                        text: "Status"
                        font.pixelSize: Math.min(24, parent.height * 0.6)
                        color: "#6b1b1b"
                        font.bold: true
                        elide: Text.ElideRight
                    }
                }
            }
            
            // ================= PAYMENT MODE BOX =================
            Rectangle {
                id: payment_mode
                width: 270  // Fixed width
                color: "#0B1C2D"
                border.color: "#2A3F55"
                border.width: 2
                
                // Position at same top as passenger info, but limit height
                anchors.top: passengerInfoRow.top
                anchors.bottom: operatorRow.top  // Stop at operator row
                anchors.bottomMargin: 5  // 5px margin above operator row
                anchors.left: passengerInfoRow.right
                anchors.leftMargin: -15  // 5px margin

                Column {
                    anchors.centerIn: parent
                    spacing: 6

                    Text {
                        text: "Payment Mode"
                        font.pixelSize: Math.min(26, parent.parent.height * 0.08)
                        font.bold: true
                        color: "#C9A24D"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Rectangle {
                        width: parent.parent.width * 0.9
                        height: 2
                        color: "#C9A24D"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Text {
                        text: "UPI-QR CODE"
                        font.pixelSize: Math.min(26, parent.parent.height * 0.08)
                        font.bold: true
                        color: "#C9A24D"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
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

            // ================= PASSENGER DETAILS ROWS (DYNAMIC HEIGHT) =================
         
            Item {
                id: passengerDetailsContainer
                anchors.top: passengerInfoRow.bottom
                anchors.topMargin: 0
                anchors.left: parent.left
                anchors.right: qrBox.left
                anchors.rightMargin: 265
                anchors.bottom: operatorRow.top
                anchors.bottomMargin: 5
                
                // Calculate maximum rows that can fit in available space
                property int maxVisibleRows: Math.max(0, Math.floor(height / 25))  // 25px per row
                
                // Helper property to get passenger count - ADD BINDING TO MODEL!
                property int passengerCount: passengerModel ? passengerModel.count : 0

                
                // ================= Passenger Details BOXES ================
                Column {
                    id: passengerList
                    spacing: 0
                    width: parent.width
                    
                    // FIX: Height should be based on ACTUAL visible rows, not maxVisibleRows
                    height: {
                        var passengerCount = passengerDetailsContainer.passengerCount;
                        var maxRows = passengerDetailsContainer.maxVisibleRows;
                        var rowsToShow = Math.min(passengerCount, maxRows);
                        return rowsToShow * 25;
                    }
                    
                    // Define widths based on passengerInfoRow's distribution
                    property real nameBoxWidth: passengerInfoRow.nameBoxWidth
                    property real sexBoxWidth: passengerInfoRow.sexBoxWidth
                    property real ageBoxWidth: passengerInfoRow.ageBoxWidth
                    property real statusBoxWidth: passengerInfoRow.statusBoxWidth
                    
                    // Use passengerModel as the Repeater model
                    Repeater {
                        model: passengerModel  // Use the model directly
                        
                        delegate: Item {
                            width: passengerList.width
                            height: 25
                            
                            // FIX: Only show if within visible range
                            visible: index < passengerDetailsContainer.maxVisibleRows
                            
                            Row {
                                anchors.fill: parent
                                spacing: 0
                                
                                // Passenger Name Box (51%)
                                Rectangle {
                                    width: passengerList.nameBoxWidth
                                    height: parent.height
                                    color: "#000000"
                                    border.color: "#ffffff"
                                    border.width: 0.5
                                    Text { 
                                        anchors.fill: parent
                                        anchors.margins: 2
                                        text: model.name || ""
                                        font.pixelSize: Math.min(20, parent.height * 0.6)
                                        color: "#ffffff"
                                        font.bold: true
                                        elide: Text.ElideRight
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                }

                                // Sex Box (12%)
                                Rectangle {
                                    width: passengerList.sexBoxWidth
                                    height: parent.height
                                    color: "#000000"
                                    border.color: "#ffffff"
                                    border.width: 0.5
                                    Text { 
                                        anchors.centerIn: parent
                                        text: model.sex || ""
                                        font.pixelSize: Math.min(20, parent.height * 0.6)
                                        color: "#ffffff"
                                        font.bold: true
                                        elide: Text.ElideRight
                                    }
                                }

                                // Age Box (12%)
                                Rectangle {
                                    width: passengerList.ageBoxWidth
                                    height: parent.height
                                    color: "#000000"
                                    border.color: "#ffffff"
                                    border.width: 0.5
                                    Text { 
                                        anchors.centerIn: parent
                                        text: model.age || ""
                                        font.pixelSize: Math.min(20, parent.height * 0.6)
                                        color: "#ffffff"
                                        font.bold: true
                                        elide: Text.ElideRight
                                    }
                                }

                                // Status Box (25%)
                                Rectangle {
                                    width: passengerList.statusBoxWidth
                                    height: parent.height
                                    color: "#000000"
                                    border.color: "#ffffff"
                                    border.width: 0.5
                                    
                                    Text { 
                                        anchors.fill: parent
                                        anchors.margins: 2
                                        text: model.status || ""
                                        font.pixelSize: Math.min(20, parent.height * 0.6)
                                        color: "#ffffff"
                                        font.bold: true
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                        elide: Text.ElideRight
                                    }
                                }
                            }
                        }
                    }
                }
                
                // ================= EMPTY ROWS CONTAINER =================
                // This creates empty rows BELOW the actual passenger list
                Column {
                    id: emptyRowsContainer
                    spacing: 0
                    width: parent.width
                    
                    // Position it right below the passenger list
                    anchors.top: passengerList.bottom
                    anchors.left: parent.left
                    
                    // Height should be the remaining space after passenger list
                    height: {
                        var passengerCount = passengerDetailsContainer.passengerCount;
                        var maxRows = passengerDetailsContainer.maxVisibleRows;
                        var rowsToShow = Math.min(passengerCount, maxRows);
                        var emptyRowsCount = Math.max(0, maxRows - rowsToShow);
                        return emptyRowsCount * 25;
                    }
                    
                    // Define widths (same as passenger list)
                    property real nameBoxWidth: passengerInfoRow.nameBoxWidth
                    property real sexBoxWidth: passengerInfoRow.sexBoxWidth
                    property real ageBoxWidth: passengerInfoRow.ageBoxWidth
                    property real statusBoxWidth: passengerInfoRow.statusBoxWidth
                    
                    // Create empty rows
                    Repeater {
                        model: {
                            var passengerCount = passengerDetailsContainer.passengerCount;
                            var maxRows = passengerDetailsContainer.maxVisibleRows;
                            var rowsToShow = Math.min(passengerCount, maxRows);
                            var emptyRowsCount = Math.max(0, maxRows - rowsToShow);
                            return emptyRowsCount;
                        }
                        
                        delegate: Item {
                            width: emptyRowsContainer.width
                            height: 25
                            
                            Row {
                                anchors.fill: parent
                                spacing: 0
                                
                                // Passenger Name Box (51%)
                                Rectangle {
                                    width: emptyRowsContainer.nameBoxWidth
                                    height: parent.height
                                    color: "#000000"
                                    border.color: "#ffffff"
                                    border.width: 0.5
                                    Text { 
                                        anchors.fill: parent
                                        anchors.margins: 2
                                        text: ""
                                        font.pixelSize: Math.min(20, parent.height * 0.6)
                                        color: "#ffffff"
                                        font.bold: true
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                }

                                // Sex Box (12%)
                                Rectangle {
                                    width: emptyRowsContainer.sexBoxWidth
                                    height: parent.height
                                    color: "#000000"
                                    border.color: "#ffffff"
                                    border.width: 0.5
                                    Text { 
                                        anchors.centerIn: parent
                                        text: ""
                                        font.pixelSize: Math.min(20, parent.height * 0.6)
                                        color: "#ffffff"
                                        font.bold: true
                                    }
                                }

                                // Age Box (12%)
                                Rectangle {
                                    width: emptyRowsContainer.ageBoxWidth
                                    height: parent.height
                                    color: "#000000"
                                    border.color: "#ffffff"
                                    border.width: 0.5
                                    Text { 
                                        anchors.centerIn: parent
                                        text: ""
                                        font.pixelSize: Math.min(20, parent.height * 0.6)
                                        color: "#ffffff"
                                        font.bold: true
                                    }
                                }

                                // Status Box (25%)
                                Rectangle {
                                    width: emptyRowsContainer.statusBoxWidth
                                    height: parent.height
                                    color: "#000000"
                                    border.color: "#ffffff"
                                    border.width: 0.5
                                    
                                    Text { 
                                        anchors.fill: parent
                                        anchors.margins: 2
                                        text: ""
                                        font.pixelSize: Math.min(20, parent.height * 0.6)
                                        color: "#ffffff"
                                        font.bold: true
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                }
                            }
                        }
                    }
                }
                
                // Empty space indicator (only if no space at all)
                Rectangle {
                    visible: passengerDetailsContainer.maxVisibleRows === 0
                    anchors.fill: parent
                    color: "transparent"
                    border.color: "#ffffff"
                    border.width: 1
                    
                    Text {
                        anchors.centerIn: parent
                        text: "No space available for passenger list"
                        font.pixelSize: 20
                        color: "#ffffff"
                        font.bold: true
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