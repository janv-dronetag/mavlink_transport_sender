# MAVLink Transport Sender for Dronetag DRI

A Python tool for publishing MAVLink messages (including Open Drone ID) over UART to **Dronetag DRI**.  
It is designed for testing, development, and integration of custom firmware or flight controllers with the Dronetag unit.

---

## Features
- Publish **standard MAVLink messages** (e.g., HEARTBEAT, GPS_RAW_INT).
- Publish **Open Drone ID messages** for Remote ID compliance.
- Support for two transport modes:
  - **SLIP with MUX address** – recommended, robust framing.
  - **Raw** – direct transmission, less suitable.
- Configurable coordinate provider (fixed position or simulated movement).
- Easy verification of output using the **Dronescanner** app.

---

## Requirements
- Python 3.8+
- Libraries:
  - `pymavlink>=2.4.47`
  - `pyserial`

Installation using `requirements.txt`:

```
pip install -r requirements.txt
```

**or** directly:

```
pip install "pymavlink>=2.4.47" pyserial
```

---

##️ Configuration
Edit `config.py` to set:
- **Port**: e.g. `/dev/ttyACM0`
- **Baudrate**: typically `500000`
- **Transport**: `slip` or `raw`
- **MUX address**: required for SLIP mode

---

## Usage
```
python -m mavlink_transport_sender.main
```

---

## Dronetag DRI Configuration
Depending on the chosen transport mode, configure Dronetag DRI:

- **SLIP mode**:  
  - `mavlink_provider = slip`  
  - `loc_service/provider = slip`  
  - `press_service/provider = slip`

- **Raw mode**:  
  - `mavlink_provider = raw`  
  - `loc_service/provider = raw`  
  - `press_service/provider = raw`

---

## Verification
- Launch the **Dronescanner** app from Dronetag.
- Confirm that the following are displayed:
  - UAS ID
  - Operator ID
  - Coordinates as defined in `config.py`

---

## Project Structure
- `main.py` – entry point
- `config.py` – configuration (port, baudrate, transport)
- `coordinate_providers.py` – GPS coordinate generator
- `mavlink_manager.py` – MAVLink message creation
- `transports/` – SLIP and Raw transport implementations

---

## License
MIT License – see `LICENSE` file.
