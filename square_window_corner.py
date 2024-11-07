"""
This script makes the specified window corners square on Windows 11.

When taking a screenshot of a window on Windows 11, each corner of a 
window are rounded. It looks awful to use it for documentation because 
the corners are filled out as black.

Valid for Windows 11 build 22000 and later
"""


from ctypes import windll, c_int, byref, sizeof
from enum_windows import EnumHwnd


# Refer to : https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/nf-dwmapi-dwmgetwindowattribute
# DwmGetWindowAttribute = windll.dwmapi.DwmGetWindowAttribute
# Refer to : https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/nf-dwmapi-dwmsetwindowattribute
DwmSetWindowAttribute = windll.dwmapi.DwmSetWindowAttribute


def make_window_corner_square(hwnd):
    """
    Make the specified window corners square

    Args:
        hwnd: Target window handle o make the corners square
    """
    # Refer to : https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    # Refer to : https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwm_window_corner_preference
    DWMWCP_DONOTROUND = 1

    attribute = c_int(DWMWCP_DONOTROUND)
    DwmSetWindowAttribute(hwnd, DWMWA_WINDOW_CORNER_PREFERENCE, byref(attribute), sizeof(attribute))


if __name__ == '__main__':
    # Enumerate windows
    enum_hwnd = EnumHwnd()
    windows = enum_hwnd.enumerate()

    # Make the corners of all enumerated windows square
    for wnd in windows:
        # _FOR_DEBUG_
        print(wnd.title)
        make_window_corner_square(wnd.hwnd)

