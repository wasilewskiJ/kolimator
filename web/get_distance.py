import time
import importlib.util

if importlib.util.find_spec("serial"):
    import serial
else:
    print("WARNING: Serial library not found. Please install it with 'pip install pyserial'")

def get_distance(fast=False):
    autobdr = bytes([0x55])
    shotslow = bytes([0xAA, 0x00, 0x00, 0x20, 0x00, 0x01, 0x00, 0x01, 0x22])
    shotfast = bytes([0xAA, 0x00, 0x00, 0x20, 0x00, 0x01, 0x00, 0x02, 0x23])
    shotcontinous = bytes([0xAA, 0x00, 0x00, 0x20, 0x00, 0x01, 0x00, 0x04, 0x25])
    rdstatus = bytes([0xAA, 0x80, 0x00, 0x00, 0x80])
    rdiv = bytes([0xAA, 0x80, 0x00, 0x06, 0x86])
    laser_on = bytes([0xAA, 0x00, 0x01, 0xBE, 0x00, 0x01, 0x00, 0x01, 0xC1])
    laser_off = bytes([0xAA, 0x00, 0x01, 0xBE, 0x00, 0x01, 0x00, 0x00, 0xC0])

    def setup_connection():
        try:
            print("Attempting to open serial connection...")
            ser = serial.Serial('/dev/serial0', 19200, timeout=3)  # Increased timeout
            print("Serial connection established.")
            ser.write(autobdr)
            time.sleep(0.5)
            ser.write(rdstatus)
            time.sleep(0.5)
            ser.write(rdiv)
            time.sleep(0.5)
            return ser, None
        except serial.SerialException as e:
            print(f"Serial connection error: {e}")
            return None, f"Nie można otworzyć portu: {e}"

    def read_data(ser, fast):
        try:
            print(f"Sending {'fast' if fast else 'slow'} shot command...")
            if fast:
                ser.write(shotfast)
            else:
                ser.write(shotslow)

            time.sleep(0.5)
            bytes_waiting = ser.in_waiting
            if bytes_waiting > 0:
                ser.read(18)
                incomingByte = ser.read(13)
                print(f"Bytes read: {incomingByte.hex()}")
                if len(incomingByte) >= 10:
                    val = incomingByte[6] << 24 | incomingByte[7] << 16 | incomingByte[8] << 8 | incomingByte[9]
                    val_m = val / 1000
                    return val_m, None
                else:
                    return None, "Odebrano niepełne dane."
            else:
                return None, "Brak danych, czekam..."
        except Exception as e:
            print(f"Error reading data: {e}")
            return None, f"Error reading data: {e}"

    ser, error = setup_connection()
    if ser:
        try:
            return read_data(ser, fast)
        finally:
            ser.close()
            print("Serial connection closed.")
    else:
        return None, error

# Example usage for debugging
if __name__ == "__main__":
    distance, error = get_distance()
    if distance:
        print(f"Distance: {distance} meters")
    else:
        print(f"Error: {error}")
