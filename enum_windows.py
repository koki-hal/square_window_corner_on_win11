from ctypes import windll, WINFUNCTYPE, create_unicode_buffer
from ctypes import c_bool, c_void_p

EnumWindows = windll.user32.EnumWindows
# EnumDesktopWindows = windll.user32.EnumDesktopWindows
GetWindowText = windll.user32.GetWindowTextW
GetWindowTextLength = windll.user32.GetWindowTextLengthW
IsWindowVisible = windll.user32.IsWindowVisible
GetWindowLong = windll.user32.GetWindowLongW
GetWindow = windll.user32.GetWindow

WNDENUMPROC = WINFUNCTYPE(c_bool, c_void_p, c_void_p)


class WindowList:
    """
    Window list that enumerated
    """
    def __init__(self, hwnd=0, title=''):
        self.hwnd = hwnd
        self.title = title
        pass


class EnumHwnd:
    def __init__(self):
        self.windows = []

    def enumerate(self) -> list:
        # Refer to : https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows
        EnumWindows(WNDENUMPROC(self._enum_windows_proc), 0)
        # Refer to : https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdesktopwindows?redirectedfrom=MSDN
        # EnumDesktopWindows(None, WNDENUMPROC(self._enum_windows_proc), 0)
        return self.windows

    def _is_app_window(self, hwnd, wndstyle, wndexstyle) -> bool:
        """
        Determine if it is an application window

        Args:
            hwnd: Window handle
            wndstyle: Window style
            wndexstyle: Window extended style
        """

        # Exclude the invisible window
        if IsWindowVisible(hwnd) == 0:
            return False

        # Get the window title string length
        length = GetWindowTextLength(hwnd)
        # Exclude the window that does not have the title string
        if length == 0:
            return False

        # Exclude the tool window
        # Refer to : https://learn.microsoft.com/en-us/windows/win32/winmsg/extended-window-styles
        WS_EX_TOOLWINDOW = 0x0000_0080
        if wndexstyle & WS_EX_TOOLWINDOW == WS_EX_TOOLWINDOW:
            return False

        # Exclude the window that does not have visual content and does not have a caption
        # _CAUTION_ : It might include some windows that wanted to be excluded ...
        WS_EX_NOREDIRECTIONBITMAP = 0x0020_0000
        WS_CAPTION = 0x00C0_0000
        if (wndexstyle & WS_EX_NOREDIRECTIONBITMAP == WS_EX_NOREDIRECTIONBITMAP) and (wndstyle & WS_CAPTION != WS_CAPTION):
            return False

        return True

    def _enum_windows_proc(self, hwnd, lParam) -> bool:
        """
        Callback function for EnumWindows
        """

        # window style
        # Refer to : https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongw
        GWL_STYLE = -16
        wndstyle = GetWindowLong(hwnd, GWL_STYLE)
        if wndstyle < 0:
            wndstyle = wndstyle & 0xFFFF_FFFF

        # window ex style
        # Refer to : https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongw
        GWL_EXSTYLE = -20
        wndexstyle = GetWindowLong(hwnd, GWL_EXSTYLE)
        if wndexstyle < 0:
            wndexstyle = wndexstyle & 0xFFFF_FFFF

        # Determine if it is an application window
        if not self._is_app_window(hwnd, wndstyle, wndexstyle):
            return True

        # Length of the window title string
        length = GetWindowTextLength(hwnd)
        # Get the window title string
        buff = create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        title = buff.value

        # Append to the window list
        wnd = WindowList(hwnd, title)
        self.windows.append(wnd)

        return True


if __name__ == '__main__':
    # _FOR_DEBUG_
    enumhwnd = EnumHwnd()
    windows = enumhwnd.enumerate()
    for wnd in windows:
        print(f'{wnd.hwnd:08X} {wnd.title}')

