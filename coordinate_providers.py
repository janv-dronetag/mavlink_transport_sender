from abc import ABC, abstractmethod
from .config import LOGO_RELATIVE_COORDS_RAW, BASE_LAT_E7, BASE_LON_E7, FIXED_LAT_E7, FIXED_LON_E7

class BaseCoordinateProvider(ABC):
    """Abstract base class for coordinate providers."""
    @abstractmethod
    def get_next_coordinate(self) -> tuple[int, int]:
        """Returns the next absolute (lon_e7, lat_e7) coordinate."""
        pass

    @abstractmethod
    def get_current_operator_location(self) -> tuple[int, int]:
        """Returns the operator's fixed base location (lon_e7, lat_e7)."""
        pass

class FixedCoordinateProvider(BaseCoordinateProvider):
    """Provides a fixed set of coordinates."""
    def __init__(self):
        self.lon_e7 = FIXED_LON_E7
        self.lat_e7 = FIXED_LAT_E7
        self.operator_lon_e7 = BASE_LON_E7 # Default operator location
        self.operator_lat_e7 = BASE_LAT_E7

    def get_next_coordinate(self) -> tuple[int, int]:
        """Returns the fixed coordinate."""
        return self.lon_e7, self.lat_e7

    def get_current_operator_location(self) -> tuple[int, int]:
        """Returns the fixed operator location."""
        return self.operator_lon_e7, self.operator_lat_e7

class CyclingCoordinateProvider(BaseCoordinateProvider):
    """Cycles through a predefined list of relative coordinates."""
    def __init__(self):
        self.current_coord_index = 0
        self.coords_list = LOGO_RELATIVE_COORDS_RAW
        self.num_coords = len(self.coords_list)

        self.operator_lon_e7 = BASE_LON_E7 # Default operator location
        self.operator_lat_e7 = BASE_LAT_E7

    def _convert_relative_to_abs_e7(self, relative_lon_raw, relative_lat_raw):
        """
        Converts raw relative integer coordinates (already in 1e7 degrees delta)
        to absolute lat/lon in 1e7 degrees, based on the defined origin.
        """
        abs_lon_e7 = BASE_LON_E7 + relative_lon_raw
        abs_lat_e7 = BASE_LAT_E7 + relative_lat_raw
        return abs_lon_e7, abs_lat_e7

    def get_next_coordinate(self) -> tuple[int, int]:
        """
        Returns the next absolute (lon_e7, lat_e7) coordinate in the logo path,
        and advances the index.
        """
        relative_lon_raw, relative_lat_raw = self.coords_list[self.current_coord_index]
        
        abs_lon_e7, abs_lat_e7 = self._convert_relative_to_abs_e7(relative_lon_raw, relative_lat_raw)
        
        self.current_coord_index = (self.current_coord_index + 1) % self.num_coords
        
        return abs_lon_e7, abs_lat_e7

    def get_current_operator_location(self) -> tuple[int, int]:
        """Returns the base operator location in 1e7 degrees."""
        return self.operator_lon_e7, self.operator_lat_e7