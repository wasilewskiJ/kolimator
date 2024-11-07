import time
import serial

def control_laser(turn_on=True):
    # Command bytes for turning the laser on and off
    laser_on = bytes([0xAA, 0x00, 0x01, 0xBE, 0x00, 0x01, 0x00, 0x01, 0xC1])
    laser_off = bytes([0xAA, 0x00, 0x01, 0xBE, 0x00, 0x01, 0x00, 0x00, 0xC0])
    
    # Command to read status (optional, for debugging)
    rdstatus = bytes([0xAA, 0x80, 0x00, 0x00, 0x80])
    
    def setup_connection():
        try:
            print("Attempting to open serial connection...")
            ser = serial.Serial('/dev/serial0', 19200, timeout=3)
            print("Serial connection established.")
            return ser, None
        except serial.SerialException as e:
            print(f"Serial connection error: {e}")
            return None, f"Cannot open port: {e}"

    ser, error = setup_connection()
    if ser:
        try:
            # Select the command based on input
            command = laser_on if turn_on else laser_off
            print(f"Sending command to {'turn on' if turn_on else 'turn off'} laser...")
            ser.write(command)
            return "Laser turned on." if turn_on else "Laser turned off."
        except Exception as e:
            print(f"Error sending command: {e}")
            return f"Error: {e}"
        finally:
            ser.close()
            print("Serial connection closed.")
    else:
        return error

# Example usage
if __name__ == "__main__":
    result = control_laser(turn_on=True)  # Set to False to turn off
    print(result)

