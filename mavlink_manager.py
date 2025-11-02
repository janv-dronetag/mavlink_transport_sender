import time
from pymavlink.dialects.v20 import common as mavlink2
from .transports.base_transport import BaseTransport # Import the interface
from .coordinate_providers import BaseCoordinateProvider # Import the interface
from .config import (DEMO_UAS_ID, DEMO_OPERATOR_ID)

class MavlinkManager:
    """
    Manages the creation and sending of various MAVLink messages.
    It uses a provided transport layer and coordinate provider.
    """
    def __init__(self, transport: BaseTransport, coord_provider: BaseCoordinateProvider):
        self.transport = transport
        self.coord_provider = coord_provider
        
        # Initialize MAVLink dialect and source info
        self.mav = mavlink2.MAVLink(None)
        self.mav.srcSystem = 1
        self.mav.srcComponent = 1

        # Internal state for ODID messages (e.g., arm status, airborne status)
        self._is_armed = False

    def _send_mavlink_message(self, msg_type_name: str, msg):
        """
        Packs a MAVLink message and sends it via the configured transport.
        """
        buf = msg.pack(self.mav)
        self.transport.write_packet(buf, msg_type_name)

    def send_heartbeat(self):
        msg = self.mav.heartbeat_encode(
            type=mavlink2.MAV_TYPE_GENERIC,
            autopilot=mavlink2.MAV_AUTOPILOT_GENERIC,
            base_mode=0,
            custom_mode=0,
            system_status=mavlink2.MAV_STATE_ACTIVE
        )
        self._send_mavlink_message("HEARTBEAT", msg)

    def send_system_time(self, time_boot_ms: int):
        time_unix_us = int(time.time() * 1e6)
        msg = self.mav.system_time_encode(
            time_unix_usec=time_unix_us,
            time_boot_ms=time_boot_ms
        )
        self._send_mavlink_message("SYSTEM_TIME", msg)

    def send_scaled_pressure(self, time_boot_ms: int):
        msg = self.mav.scaled_pressure_encode(
            time_boot_ms=time_boot_ms,
            press_abs=1013.25,
            press_diff=0.12,
            temperature=2000
        )
        self._send_mavlink_message("SCALED_PRESSURE", msg)

    def send_gps_raw_int(self, time_usec: int, time_boot_ms: int):
        current_lon_e7, current_lat_e7 = self.coord_provider.get_next_coordinate()

        msg = self.mav.gps_raw_int_encode(
            time_usec=time_usec,
            fix_type=3,
            lat=current_lat_e7,
            lon=current_lon_e7,
            alt=int(250.0 * 1000), # Altitude in mm (250m)
            eph=100, epv=100,
            vel=500, cog=0,
            satellites_visible=10
        )
        self._send_mavlink_message("GPS_RAW_INT", msg)

    def send_global_position_int(self, time_boot_ms: int):
        current_lon_e7, current_lat_e7 = self.coord_provider.get_next_coordinate()

        msg = self.mav.global_position_int_encode(
            time_boot_ms=time_boot_ms,
            lat=current_lat_e7,
            lon=current_lon_e7,
            alt=int(250.0 * 1000), # Altitude in mm (250m)
            relative_alt=int(5.0 * 1000), # Relative altitude in mm (5m above home)
            vx=0, vy=0, vz=0,
            hdg=0
        )
        self._send_mavlink_message("GLOBAL_POSITION_INT", msg)

    # --- Open Drone ID (ODID) Message Sending Functions ---

    def send_odid_arm_status(self):
        status_text = ""
        error_message_bytes = bytearray(32)
        
        status = mavlink2.MAV_ODID_ARM_STATUS_GOOD_TO_ARM
        status_text = "GOOD_TO_ARM"

        msg = self.mav.open_drone_id_arm_status_encode(
            status=status,
            error=error_message_bytes
        )
        self._send_mavlink_message(f"OPEN_DRONE_ID_ARM_STATUS (Status: {status_text})", msg)

    def send_odid_basic_id(self):
        uas_id_str = DEMO_UAS_ID
        uas_id_bytes = bytearray(uas_id_str.encode('ascii'))
        uas_id_bytes.extend([0] * (20 - len(uas_id_bytes)))
        uas_id_bytes = uas_id_bytes[:20]

        id_or_mac_bytes = bytearray([0] * 20)

        msg = self.mav.open_drone_id_basic_id_encode(
            target_system=0,
            target_component=0,
            id_or_mac=id_or_mac_bytes,
            id_type=mavlink2.MAV_ODID_ID_TYPE_SERIAL_NUMBER,
            ua_type=mavlink2.MAV_ODID_UA_TYPE_HELICOPTER_OR_MULTIROTOR,
            uas_id=uas_id_bytes
        )
        self._send_mavlink_message("OPEN_DRONE_ID_BASIC_ID", msg)

    def send_odid_location(self):
        current_lon_e7, current_lat_e7 = self.coord_provider.get_next_coordinate()
        
        status_val = mavlink2.MAV_ODID_STATUS_AIRBORNE

        target_system = 0
        target_component = 0
        id_or_mac_bytes = bytearray([0] * 20)

        latitude_e7 = current_lat_e7
        longitude_e7 = current_lon_e7

        altitude_barometric_m = 255.0
        altitude_geodetic_m = 250.0
        height_reference_val = mavlink2.MAV_ODID_HEIGHT_REF_OVER_GROUND
        height_m = 5.0

        direction_cdeg = 4500
        speed_horizontal_cms = 500
        speed_vertical_cms = 50

        horizontal_accuracy_val = mavlink2.MAV_ODID_HOR_ACC_1_METER
        vertical_accuracy_val = mavlink2.MAV_ODID_VER_ACC_1_METER
        barometer_accuracy_val = mavlink2.MAV_ODID_VER_ACC_1_METER
        speed_accuracy_val = mavlink2.MAV_ODID_SPEED_ACC_1_METERS_PER_SECOND

        current_utc_time = time.time()
        timestamp_s = float(current_utc_time % 3600)
        timestamp_accuracy_val = mavlink2.MAV_ODID_TIME_ACC_0_3_SECOND

        msg = self.mav.open_drone_id_location_encode(
            target_system=target_system,
            target_component=target_component,
            id_or_mac=id_or_mac_bytes,
            status=status_val,
            direction=direction_cdeg,
            speed_horizontal=speed_horizontal_cms,
            speed_vertical=speed_vertical_cms,
            latitude=latitude_e7,
            longitude=longitude_e7,
            altitude_barometric=altitude_barometric_m,
            altitude_geodetic=altitude_geodetic_m,
            height_reference=height_reference_val,
            height=height_m,
            horizontal_accuracy=horizontal_accuracy_val,
            vertical_accuracy=vertical_accuracy_val,
            barometer_accuracy=barometer_accuracy_val,
            speed_accuracy=speed_accuracy_val,
            timestamp=timestamp_s,
            timestamp_accuracy=timestamp_accuracy_val
        )
        self._send_mavlink_message(f"OPEN_DRONE_ID_LOCATION (Status: 'Airborne')", msg)

    def send_odid_operator_id(self):
        target_system = 0
        target_component = 0
        id_or_mac_bytes = bytearray([0] * 20)
        operator_id_type_val = mavlink2.MAV_ODID_OPERATOR_ID_TYPE_CAA
        operator_id_str = DEMO_OPERATOR_ID
        operator_id_bytes = bytearray(operator_id_str.encode('ascii'))
        operator_id_bytes.extend([0] * (20 - len(operator_id_bytes)))
        operator_id_bytes = operator_id_bytes[:20]

        msg = self.mav.open_drone_id_operator_id_encode(
            target_system=target_system,
            target_component=target_component,
            id_or_mac=id_or_mac_bytes,
            operator_id_type=operator_id_type_val,
            operator_id=operator_id_bytes
        )
        self._send_mavlink_message("OPEN_DRONE_ID_OPERATOR_ID", msg)

    def send_odid_system(self):
        target_system = 0
        target_component = 0
        id_or_mac_bytes = bytearray([0] * 20)
        operator_location_type_val = mavlink2.MAV_ODID_OPERATOR_LOCATION_TYPE_FIXED
        classification_type_val = mavlink2.MAV_ODID_CLASSIFICATION_TYPE_EU

        operator_lon_e7, operator_lat_e7 = self.coord_provider.get_current_operator_location()
        operator_altitude_geo_m = 300.0

        area_count = 1
        area_radius = 0
        area_ceiling_m = 120.0
        area_floor_m = 0.0

        category_eu_val = mavlink2.MAV_ODID_CATEGORY_EU_OPEN
        class_eu_val = mavlink2.MAV_ODID_CLASS_EU_CLASS_0

        unix_epoch_2019_01_01_00_00_00 = 1546300800
        current_unix_timestamp = int(time.time())
        timestamp_odid_s = current_unix_timestamp - unix_epoch_2019_01_01_00_00_00
        if timestamp_odid_s < 0:
            timestamp_odid_s = 0
        timestamp_odid_s = min(timestamp_odid_s, 0xFFFFFFFF)

        msg = self.mav.open_drone_id_system_encode(
            target_system=target_system,
            target_component=target_component,
            id_or_mac=id_or_mac_bytes,
            operator_location_type=operator_location_type_val,
            classification_type=classification_type_val,
            operator_latitude=operator_lat_e7,
            operator_longitude=operator_lon_e7,
            area_count=area_count,
            area_radius=area_radius,
            area_ceiling=area_ceiling_m,
            area_floor=area_floor_m,
            category_eu=category_eu_val,
            class_eu=class_eu_val,
            operator_altitude_geo=operator_altitude_geo_m,
            timestamp=timestamp_odid_s
        )
        self._send_mavlink_message("OPEN_DRONE_ID_SYSTEM", msg)