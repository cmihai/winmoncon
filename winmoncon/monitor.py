from __future__ import print_function

import itertools

from ctypes import WINFUNCTYPE, POINTER, Structure, c_int, c_void_p, windll, pointer
from ctypes.wintypes import BOOL, HWND, RECT, LPARAM, HDC, HANDLE, DWORD, WCHAR


# Constants
PHYSICAL_MONITOR_DESCRIPTION_SIZE = 128
TRUE = 1

# Enums
MC_COLOR_TEMPERATURE_UNKNOWN = 0
MC_COLOR_TEMPERATURE_4000K = 1
MC_COLOR_TEMPERATURE_5000K = 2
MC_COLOR_TEMPERATURE_6500K = 3
MC_COLOR_TEMPERATURE_7500K = 4
MC_COLOR_TEMPERATURE_8200K = 5
MC_COLOR_TEMPERATURE_9300K = 6
MC_COLOR_TEMPERATURE_10000K = 7
MC_COLOR_TEMPERATURE_11500K = 8
MC_COLOR_TEMPERATURE = ['UNKNOWN', '4000K', '5000K', '6500K', '7500K', '8200K', '9300K', '10000K', '11500K']

MC_SHADOW_MASK_CATHODE_RAY_TUBE = 0
MC_APERTURE_GRILL_CATHODE_RAY_TUBE = 1
MC_THIN_FILM_TRANSISTOR = 2
MC_LIQUID_CRYSTAL_ON_SILICON = 3
MC_PLASMA = 4
MC_ORGANIC_LIGHT_EMITTING_DIODE = 5
MC_ELECTROLUMINESCENT = 6
MC_MICROELECTROMECHANICAL = 7
MC_FIELD_EMISSION_DEVICE = 8
MC_DISPLAY_TECHNOLOGY_TYPE = [
    'SHADOW MASK CATHODE RAY TUBE',
    'APERTURE GRILL CATHODE RAY TUBE',
    'THIN FILM TRANSISTOR',
    'LIQUID CRYSTAL ON SILICON',
    'PLASMA',
    'ORGANIC LIGHT EMITTING DIODE',
    'ELECTROLUMINESCENT',
    'MICROELECTROMECHANICAL',
    'FIELD EMISSION DEVICE'
]

MC_HORIZONTAL_POSITION = 0
MC_VERTICAL_POSITION = 1

MC_WIDTH = 0
MC_HEIGHT = 1

MC_RED_DRIVE = 0
MC_GREEN_DRIVE = 1
MC_BLUE_DRIVE = 2

MC_RED_GAIN = 0
MC_GREEN_GAIN = 1
MC_BLUE_GAIN = 2

# Types
class PHYSICAL_MONITOR(Structure):
    _fields_ = ("hPhysicalMonitor", HANDLE), ("szPhysicalMonitorDescription", WCHAR * PHYSICAL_MONITOR_DESCRIPTION_SIZE)

HMONITOR = HANDLE

# Function prototypes
MONITOR_ENUM_PROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, POINTER(RECT), LPARAM)


class classproperty(object):
    # With regards to http://stackoverflow.com/a/13624858/287185

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
    

class PhysicalMonitor(object):
    """ Represents a physical monitor.
    """

    def __init__(self, handle, description):
        self.__handle, self.description = handle, description

    @classproperty
    def all(cls):
        """ Gets a list of all physical monitors in the system.
        """
        return list(itertools.chain.from_iterable(m.physical for m in get_display_monitors()))

    @property
    def min_brightness(self):
        """ Gets the monitor's minimum brightness, as an integer
        """
        return self.get_brightness()[0]

    @property
    def max_brightness(self):
        """ Gets the monitor's maximum brightness, as an integer
        """
        return self.get_brightness()[2]

    @property
    def brightness(self):
        """ Gets or sets the current monitor brightness, as an integer
        """
        return self.get_brightness()[1]

    @brightness.setter
    def brightness(self, value):
        windll.Dxva2.SetMonitorBrightness(self.__handle, DWORD(value))

    @property
    def min_contrast(self):
        """ Gets the monitor's minimum contrast, as an integer
        """
        return self.get_contrast()[0]

    @property
    def max_contrast(self):
        """ Gets the monitor's maximum contrast, as an integer
        """
        return self.get_contrast()[2]

    @property
    def contrast(self):
        """ Gets or sets the current monitor contrast, as an integer
        """
        return self.get_contrast()[1]

    @contrast.setter
    def contrast(self, value):
        windll.Dxva2.SetMonitorContrast(self.__handle, DWORD(value))

    @property
    def color_temperature(self):
        """ Gets the monitor's current color temperature, as a string.
        
        Possible values: 'UNKNOWN', '4000K', '5000K', '6500K', '7500K', '8200K', '9300K', '10000K', '11500K'
        """
        color_temp = c_int(1)
        windll.Dxva2.GetMonitorColorTemperature(self.__handle, pointer(color_temp))
        return MC_COLOR_TEMPERATURE[color_temp.value]

    @property
    def color_temperature(self):
        """ Gets the monitor's current color temperature, as a string.
        
        Possible values: 'UNKNOWN', '4000K', '5000K', '6500K', '7500K', '8200K', '9300K', '10000K', '11500K'
        """
        color_temp = c_int(1)
        windll.Dxva2.GetMonitorColorTemperature(self.__handle, pointer(color_temp))
        return MC_COLOR_TEMPERATURE[color_temp.value]
        
    @color_temperature.setter
    def color_temperature(self, new_temp):
        if type(new_temp) == str:
            new_temp = MC_COLOR_TEMPERATURE.index(new_temp)
        windll.Dxva2.SetMonitorColorTemperature(self.__handle, new_temp)

    @property
    def technology_type(self):
        """ Return the monitor technology type, as one of the following strings:
         
         - 'SHADOW MASK CATHODE RAY TUBE'
         - 'APERTURE GRILL CATHODE RAY TUBE'
         - 'THIN FILM TRANSISTOR'
         - 'LIQUID CRYSTAL ON SILICON'
         - 'PLASMA'
         - 'ORGANIC LIGHT EMITTING DIODE'
         - 'ELECTROLUMINESCENT'
         - 'MICROELECTROMECHANICAL'
         - 'FIELD EMISSION DEVICE'
        """
        tech_type = DWORD(0)
        windll.Dxva2.GetMonitorTechnologyType(self.__handle, pointer(tech_type))
        return MC_DISPLAY_TECHNOLOGY_TYPE[tech_type.value]
        
    def degauss(self):
        result = windll.Dxva2.DegaussMonitor(self.__handle)
        if result == 0:
            last_error = windll.Kernel32.GetLastError()
            print("Error encountered: %x" % last_error)

    def get_brightness(self):
        """ Return a tuple of three integers, representing the minimum, current, and maximum monitor brightness.
        """
        min, crt, max = DWORD(0), DWORD(0), DWORD(0)
        windll.Dxva2.GetMonitorBrightness(self.__handle, pointer(min), pointer(crt), pointer(max))
        return (min.value, crt.value, max.value)
    
    def get_capabilities(self):
        caps, supported_temps = DWORD(0), DWORD(0)
        windll.Dxva2.GetMonitorCapabilities(self.__handle, pointer(caps), pointer(supported_temps))
        return (caps.value, supported_temps.value)

    def get_contrast(self):
        """ Return a tuple of three integers, representing the minimum, current, and maximum monitor contrast.
        """
        min, crt, max = DWORD(0), DWORD(0), DWORD(0)
        windll.Dxva2.GetMonitorContrast(self.__handle, pointer(min), pointer(crt), pointer(max))
        return (min.value, crt.value, max.value)

    def get_display_area_position(self, position_type):
        """ Return a tuple of three integers, representing the minimum, current, and maximum monitor display area position.

        The following values for *position_type* are supported:
         - *MC_VERTICAL_POSITION* - return the vertical position.
         - *MC_HORIZONTAL_POSITION* - return the horizontal position.
        """
        min, crt, max = DWORD(0), DWORD(0), DWORD(0)
        windll.Dxva2.GetMonitorDisplayAreaPosition(self.__handle, position_type, pointer(min), pointer(crt), pointer(max))
        return (min, crt, max)

    def get_display_area_size(self, size_type):
        """ Return a tuple of three integers, representing the minimum, current, and maximum monitor width or height.

        The following values for *size_type* are supported:
         - *MC_WIDTH* - return the monitor width.
         - *MC_HEIGHT* - return the monitor height.
        """
        min, crt, max = DWORD(0), DWORD(0), DWORD(0)
        windll.Dxva2.GetMonitorDisplayAreaSize(self.__handle, size_type, pointer(min), pointer(crt), pointer(max))
        return (min, crt, max)

    def get_red_green_or_blue_drive(self, drive_type):
        min, crt, max = DWORD(0), DWORD(0), DWORD(0)
        windll.Dxva2.GetMonitorRedGreenOrBlueDrive(self.__handle, drive_type, pointer(min), pointer(crt), pointer(max))
        return (min.value, crt.value, max.value)

    def get_red_green_or_blue_gain(self, gain_type):
        min, crt, max = DWORD(0), DWORD(0), DWORD(0)
        windll.Dxva2.GetMonitorRedGreenOrBlueGain(self.__handle, gain_type, pointer(min), pointer(crt), pointer(max))
        return (min.value, crt.value, max.value)
       
    def restore_factory_color_defaults(self):
        windll.Dxva2.RestoreMonitorFactoryColorDefaults()
       
    def restore_factory_defaults(self):
        windll.Dxva2.RestoreMonitorFactoryDefaults()
       
    def save_current_settings(self):
        windll.Dxva2.SaveCurrentMonitorSettings()
        

class DisplayMonitor(object):

    def __init__(self, hmonitor, rect):
        self.__handle = hmonitor
        self.top, self.bottom, self.left, self.right = rect.top, rect.bottom, rect.left, rect.right

    @property
    def physical(self):
        cnt_mon = DWORD(0)
        windll.Dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(self.__handle, pointer(cnt_mon))

        phys_monitors = (PHYSICAL_MONITOR * cnt_mon.value)()
        windll.Dxva2.GetPhysicalMonitorsFromHMONITOR(self.__handle, 1, phys_monitors)

        return [PhysicalMonitor(x.hPhysicalMonitor, x.szPhysicalMonitorDescription) for x in phys_monitors]


def get_display_monitors():
    def monitor_enum_proc(hmonitor, hdc_monitor, rc_monitor, data):
        result.append(DisplayMonitor(hmonitor, rc_monitor.contents))
        return TRUE

    result = []
    windll.user32.EnumDisplayMonitors(None, None, MONITOR_ENUM_PROC(monitor_enum_proc), None)
    return result
