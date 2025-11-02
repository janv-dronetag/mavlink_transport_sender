# mavlink_transport_sender/main.py
import time
import sys

from .config import (
    TRANSPORT_TYPE, MUX_PATH, MUX_ADDR, BAUDRATE, COORDINATE_SOURCE,
    INTERVAL_SCALED_PRESSURE, INTERVAL_GPS_RAW_INT, INTERVAL_SYSTEM_TIME,
    INTERVAL_GLOBAL_POSITION_INT, INTERVAL_HEARTBEAT,
    INTERVAL_ODID_ARM_STATUS, INTERVAL_ODID_BASIC_ID, INTERVAL_ODID_LOCATION,
    INTERVAL_ODID_OPERATOR_ID, INTERVAL_ODID_SYSTEM, INTERVAL_MAIN_LOOP_PAUSE
)
from .mavlink_manager import MavlinkManager
from .coordinate_providers import FixedCoordinateProvider, CyclingCoordinateProvider

def main():
    # --- 1. Choose and Instantiate Transport Layer ---
    transport = None
    if TRANSPORT_TYPE == "raw":
        from .transports.raw_transport import RawTransport
        transport = RawTransport(MUX_PATH, baudrate=BAUDRATE)
    elif TRANSPORT_TYPE == "slip":
        from .transports.slip_transport import SlipTransport    
        transport = SlipTransport(MUX_PATH, MUX_ADDR, baudrate=BAUDRATE)
    else:
        print(f"Error: Unknown TRANSPORT_TYPE '{TRANSPORT_TYPE}' in config.py")
        sys.exit(1)

    # --- 2. Choose and Instantiate Coordinate Provider ---
    coord_provider = None
    if COORDINATE_SOURCE == "fixed":
        coord_provider = FixedCoordinateProvider()
    elif COORDINATE_SOURCE == "cycling":
        coord_provider = CyclingCoordinateProvider()
    else:
        print(f"Error: Unknown COORDINATE_SOURCE '{COORDINATE_SOURCE}' in config.py")
        sys.exit(1)

    # --- 3. Instantiate MavlinkManager ---
    mavlink_sender = MavlinkManager(transport, coord_provider)

    try:
        transport.open()
        print(f"Sending MAVLink packets using {TRANSPORT_TYPE.upper()} transport with {COORDINATE_SOURCE.upper()} coordinates to {MUX_PATH}. Hit Ctrl-C to stop.")
        script_start_time = time.time()

        while True:
            now_us = int(time.time() * 1e6)
            time_boot_ms = int((time.time() - script_start_time) * 1e3) & 0xFFFFFFFF

            mavlink_sender.send_scaled_pressure(time_boot_ms)
            time.sleep(INTERVAL_SCALED_PRESSURE)

            mavlink_sender.send_gps_raw_int(now_us, time_boot_ms)
            time.sleep(INTERVAL_GPS_RAW_INT)

            mavlink_sender.send_system_time(time_boot_ms)
            time.sleep(INTERVAL_SYSTEM_TIME)

            mavlink_sender.send_global_position_int(time_boot_ms)
            time.sleep(INTERVAL_GLOBAL_POSITION_INT)

            mavlink_sender.send_heartbeat()
            time.sleep(INTERVAL_HEARTBEAT)

            # Open Drone ID messages
            mavlink_sender.send_odid_arm_status()
            time.sleep(INTERVAL_ODID_ARM_STATUS)

            mavlink_sender.send_odid_basic_id()
            time.sleep(INTERVAL_ODID_BASIC_ID)

            mavlink_sender.send_odid_location()
            time.sleep(INTERVAL_ODID_LOCATION)

            mavlink_sender.send_odid_operator_id()
            time.sleep(INTERVAL_ODID_OPERATOR_ID)

            mavlink_sender.send_odid_system()
            time.sleep(INTERVAL_ODID_SYSTEM)

            print("Sent MAVLink and ODID messages\n")
            time.sleep(INTERVAL_MAIN_LOOP_PAUSE)

    except FileNotFoundError as e:
        print(e)
    except IOError as e:
        print(f"Serial port error: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        if transport:
            transport.close() # Ensure the serial port is closed

if __name__ == "__main__":
    main()