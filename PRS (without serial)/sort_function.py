# sort_function.py

import update_functions as uf

def sort_and_update(backend, passengerModel, raw_string: str):
    try:
        print("Raw string:", raw_string)

        # --------------------------------------------------
        # 1. Split and build code:value map
        # --------------------------------------------------
        fields = {}
        parts = raw_string.split("$")

        for part in parts:
            if ":" in part:
                code, value = part.split(":", 1)
                fields[code.strip()] = value.strip()

        # --------------------------------------------------
        # 2. Fixed fields (direct mapping)
        # --------------------------------------------------
        trainNo          = fields.get("01", "")
        date             = fields.get("02", "")
        month            = fields.get("03", "")
        stationFrom      = fields.get("04", "")
        className        = fields.get("05", "")
        quota            = fields.get("06", "")
        destination      = fields.get("07", "")
        total_passengers = int(fields.get("08", "0") or 0)
        reservationUpto  = fields.get("09", "")
        boardingPoint    = fields.get("10", "")
        operator_code    = fields.get("11", "")
        operatorName     = fields.get("12", "")
        amount           = fields.get("13", "")

        # --------------------------------------------------
        # 3. Passenger parsing (dynamic)
        # --------------------------------------------------
        passengers = []
        base_code = 14   # ✅ MUST be before QR calculation

        for i in range(total_passengers):
            idx = base_code + i * 4
            passengers.append({
                "name":   fields.get(str(idx), ""),
                "sex":    fields.get(str(idx + 1), ""),
                "age":    fields.get(str(idx + 2), ""),
                "status": fields.get(str(idx + 3), ""),
            })

        # --------------------------------------------------
        # 4. Dynamic fields AFTER passenger list
        # --------------------------------------------------
        qr_code_index = base_code + total_passengers * 4

        qr_string      = fields.get(str(qr_code_index), "")
        connectivity   = fields.get(str(qr_code_index + 1), "")
        payment_status = fields.get(str(qr_code_index + 2), "")

        # --------------------------------------------------
        # 5. Debug print
        # --------------------------------------------------
        print("Train No        :", trainNo)
        print("Date / Month    :", date, month)
        print("From → To       :", stationFrom, "→", destination)
        print("Class / Quota   :", className, quota)
        print("Passengers      :", total_passengers)
        print("Reservation Upto:", reservationUpto)
        print("Boarding Point  :", boardingPoint)
        print("Operator        :", operator_code, operatorName)
        print("Amount          :", amount)
        print("QR String       :", qr_string)
        print("Connectivity    :", connectivity)
        print("Payment Status  :", payment_status)
        print("Passenger List  :", passengers)

        # --------------------------------------------------
        # 6. Update backend / model
        # --------------------------------------------------
        uf.update_train_no(backend, trainNo)
        uf.update_date(backend, date)
        uf.update_month(backend, month)
        uf.update_from(backend, stationFrom)
        uf.update_to(backend, destination)
        uf.update_coach(backend, quota)
        uf.update_class(backend, className)
        uf.update_passengers_count(backend, total_passengers)
        uf.update_reservation(backend, reservationUpto)
        uf.update_boarding(backend, boardingPoint)
        uf.update_operator_code(backend, operator_code)
        uf.update_operator_name(backend, operatorName)
        uf.update_amount(backend, amount)
        uf.update_qr_string(backend, qr_string)
        uf.update_passengers_list(passengerModel, passengers)

    except Exception as e:
        print("PRS parse error:", e)





