# --- Transport Layer Configuration ---
# Set to "raw" for raw MAVLink over serial
# Set to "slip" for MAVLink over SLIP over serial
TRANSPORT_TYPE = "slip"

# Common device settings
MUX_PATH = "/dev/ttyACM0"
MUX_ADDR = 0xAB # The custom mux address byte that precedes a SLIP message (only used for SLIP)
BAUDRATE = 500000

# UAS ID and OPERATOR ID
DEMO_UAS_ID = "DEMO_UAS_XY123456789"
DEMO_OPERATOR_ID = "DEMO_OPID_X123456789"

# --- Coordinate Data Source Configuration ---
# Set to "fixed" to use a single fixed GPS coordinate
# Set to "cycling" to cycle through the pre-defined logo coordinates
COORDINATE_SOURCE = "cycling"

# --- Coordinate Data ---
# Fixed coordinates for raw mode
FIXED_LAT_E7 = int(50.0755 * 1e7)
FIXED_LON_E7 = int(14.4378 * 1e7)

# Base origin for the logo in Prague, Czechia (WGS84)
# These base coordinates are also in 1e7 degrees
BASE_LAT_E7 = int(50.0755 * 1e7)
BASE_LON_E7 = int(14.4378 * 1e7)

# Relative position coordinates
LOGO_RELATIVE_COORDS_RAW = [
    (-23186, 17616), (-38214, 16791), (-53241, 16791), (-68269, 15690),
    (-81150, 17066), (-66981, -1376), (-59253, -7432), (-54100, -12112),
    (-49377, -15690), (-44654, -20095), (-35637, -25876), (-23186, -20095),
    (-15028, -11837), (-7728, -6606), (0, 0), (-3435, 5505),
    (-10734, 11286), (-15886, 16791), (-21039, 20919), (-25762, 25323),
    (-30056, 29727), (-34349, 33581), (6011, 32755), (17175, 34131),
    (33062, 33306), (44654, 33306), (61829, 33581), (75140, 33856),
    (88450, 34131), (103478, 34957), (117647, 36058), (114212, 31104),
    (108201, 24222), (103907, 17341), (101760, 11836), (100472, 7157),
    (97037, -1376), (91456, -7157), (86303, -15690), (81151, -21196),
    (72993, -28078), (67411, -33583), (61400, -39364), (55818, -44595),
    (45513, -42117), (35208, -34960), (26192, -27252), (17604, -20370),
    (12023, -12387), (7729, -7983), (-859, 1101)
]

# --- Message Sending Intervals (in seconds) ---
INTERVAL_SCALED_PRESSURE = 0.1
INTERVAL_GPS_RAW_INT = 0.1
INTERVAL_SYSTEM_TIME = 0.1
INTERVAL_GLOBAL_POSITION_INT = 0.1
INTERVAL_HEARTBEAT = 0.2
INTERVAL_ODID_ARM_STATUS = 0.1
INTERVAL_ODID_BASIC_ID = 0.1
INTERVAL_ODID_LOCATION = 0.1
INTERVAL_ODID_OPERATOR_ID = 0.1
INTERVAL_ODID_SYSTEM = 0.1
INTERVAL_MAIN_LOOP_PAUSE = 0.5
