# MAVLink Transport Sender

This project provides a Python-based MAVLink message sender designed for testing and development with Dronetag devices.
It allows you to transmit standard MAVLink messages (like HEARTBEAT, GPS_RAW_INT) and Open Drone ID (ODID) MAVLink messages over serial, with support for 2 different transport protocols.
One using raw mavlink messages and the other one using Dronetag Slip encoding to connec to devices mux channel.

Key Features:

    MAVLink Messages: Capable of sending standard MAVLink messages (like HEARTBEAT, GPS_RAW_INT) and Open Drone ID (ODID) messages.
    Flexible Transports: Supports two main ways to send data:
        SLIP: Encapsulates messages in SLIP frames, which can be prefixed with a custom MUX address. This helps with robust data transfer.
        Raw: Sends MAVLink packets directly.
    Customization: Easy to add more MAVLink message types or adjust how GPS coordinates are simulated.

Project Files Overview:

    config.py: This is the configuration file. You'll set your serial port details, chosen transport method, and MAVLink specifics here.
    coordinate_providers.py: Defines how latitude and longitude data is generated for messages (e.g., fixed coordinates or simulated movement).
    main.py: This is the script you'll run to start the sender.
    mavlink_manager.py: Handles the actual creation and packing of MAVLink messages.
    transports/: This folder contains the different serial communication methods, like raw or SLIP.

Requirements:

    Python 3, pymavlink and pyserial libraries: This project relies on the pymavlink library. It was tested successfully with pymavlink==2.4.47. Using this version or newer is highly recommended for full compatibility, especially with Open Drone ID messages.

Setup and Installation:

    Install pymavlink: pip install pymavlink pyserial
    Linux Serial Port Permissions: If you're using Linux and encounter "Permission Denied" errors when trying to access the serial port (/dev/ttyACM0), you might need to add your user to the dialout group or run the script under sudo mode.

Configuration Steps:

Before running, you need to adjust config.py to match your setup:

    Open the config.py file.
    PORT: Set this to your embedded device's serial port. On Linux, this is typically /dev/ttyACM0.
    BAUDRATE: Set this to match the baud rate of the Dronetag device (default 500000).
    TRANSPORT_TYPE: Choose "slip" for SLIP-encapsulated messages, "raw" for direct MAVLink transmission (but these are still SLIP encoded when received from device, not advised to be used at the moment).
    MUX_ADDR: If TRANSPORT_TYPE is set to "slip", define this byte (0xAB). This address will precede the SLIP frames.

Dronetag Device Configuration:

To make your Dronetag device receive MAVLink data from this sender via the MUX channel, you need to set specific providers in the device's configuration.

    If using "SLIP" transport:
    Set these three configuration values on your Dronetag device:
    "dt_bt/mavlink_provider": "MV_MUX_SLIP"
    "loc_service/provider": "LPROV_MV_MUX_SLIP"
    "press_service/provider": "PPROV_MV_MUX_SLIP"

If using "RAW" transport:
    Set these three configuration values on your Dronetag device:
    "dt_bt/mavlink_provider": "MV_MUX_RAW"
    "loc_service/provider": "LPROV_MV_MUX_RAW"
    "press_service/provider": "PPROV_MV_MUX_RAW"

How to Run the Sender:

    Make sure you are in the directory that contains the mavlink_transport_sender folder.
    Execute the script using Python's module running command: python -m mavlink_transport_sender.main
    To stop the sender at any time, press Ctrl+C.

Verification with Dronescanner:

Once the sender script is running and the Dronetag device is configured and connected, you can verify that it's receiving and using the data.

    Open the Dronescanner application.
    Check if the UAS ID and Operator ID displayed in Dronescanner match the ones configured in config.py in this sender project.
    Observe the coordinates in Dronescanner. They should correspond to the fixed coordinates or the simulated movement you've set up.

