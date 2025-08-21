import serial
import time

# Replace with your actual port: 'COMx' (Windows) or '/dev/ttyUSBx' (Linux/Mac)
arduino_port = 'COM4'
baud_rate = 115200

try:
    # Open serial port
    arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset after connecting

    while True:
        user_input = input("Enter 1 to ARM, 0 to DISARM, q to quit: ").strip()

        if user_input == '1':
            arduino.write(b'1')
            print("Sent: 1 (ARM system)")
        elif user_input == '0':
            arduino.write(b'0')
            print("Sent: 0 (DISARM system)")
        elif user_input.lower() == 'q':
            print("Exiting.")
            break
        else:
            print("Invalid input. Enter 1, 0, or q.")

except serial.SerialException as e:
    print(f"Serial error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print("Serial port closed.")
