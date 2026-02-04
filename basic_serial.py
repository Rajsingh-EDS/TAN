import serial

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    timeout=0.5
)

print("Listening on", ser.port)

buffer = b""

try:
    while True:
        data = ser.read(ser.in_waiting or 1)
        if data:
            buffer += data
            print("RAW:", data)

            # Agar end marker '^' hai
            if b'^' in buffer:
                print("FRAME:", buffer.decode(errors='ignore'))
                buffer = b""

except KeyboardInterrupt:
    print("\nExit")
finally:
    ser.close()
