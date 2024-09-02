import ctypes
import os
import time

import ddddocr
import win32api
import win32clipboard
import win32con
import win32gui
import win32process
import win32ui
from const import BALANCE_CONTROL_ID_GROUP, VK_CODE
from PIL import Image

DdddOcr = ddddocr.DdddOcr()

sleep_time = 0.2
refresh_sleep_time = 0.5
retry_time = 10

window_title = "网上股票交易系统5.0"


def get_clipboard_data():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    finally:
        win32clipboard.CloseClipboard()
    return data


def hot_key(keys):
    time.sleep(sleep_time)
    for key in keys:
        win32api.keybd_event(VK_CODE[key], 0, 0, 0)
    for key in reversed(keys):
        win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)


def set_text(hwnd, string):
    win32gui.SetForegroundWindow(hwnd)
    win32api.SendMessage(hwnd, win32con.EM_SETSEL, 0, -1)
    win32api.keybd_event(VK_CODE["backspace"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["backspace"], 0, win32con.KEYEVENTF_KEYUP, 0)
    for char in string:
        if char.isupper():
            win32api.keybd_event(0xA0, 0, 0, 0)
            win32api.keybd_event(VK_CODE[char.lower()], 0, 0, 0)
            win32api.keybd_event(VK_CODE[char.lower()], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(0xA0, 0, win32con.KEYEVENTF_KEYUP, 0)
        else:
            win32api.keybd_event(VK_CODE[char], 0, 0, 0)
            win32api.keybd_event(VK_CODE[char], 0, win32con.KEYEVENTF_KEYUP, 0)


def get_text(hwnd):
    length = ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_GETTEXTLENGTH)
    buf = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.SendMessageW(
        hwnd, win32con.WM_GETTEXT, length, ctypes.byref(buf)
    )
    return buf.value


def parse_table(text):
    lines = text.split("\t\r\n")
    keys = lines[0].split("\t")
    result = []
    for i in range(1, len(lines)):
        info = {}
        items = lines[i].split("\t")
        for j in range(len(keys)):
            info[keys[j]] = items[j]
        result.append(info)
    return result


class ThsAuto:

    def __init__(self):
        self.hwnd_main = None

    def bind_client(self):
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd > 0:
            win32gui.SetForegroundWindow(hwnd)
            self.hwnd_main = hwnd

    def kill_client(self):
        self.hwnd_main = None
        retry = 5
        while retry > 0:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd == 0:
                time.sleep(1)
                break
            else:
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(sleep_time)
                hot_key(["alt", "F4"])
                time.sleep(1)
                retry -= 1

    def get_tree_hwnd(self):
        hwnd = self.hwnd_main
        hwnd = win32gui.FindWindowEx(hwnd, None, "AfxMDIFrame140s", None)
        hwnd = win32gui.FindWindowEx(hwnd, None, "AfxWnd140s", None)
        hwnd = win32gui.FindWindowEx(hwnd, None, None, "HexinScrollWnd")
        hwnd = win32gui.FindWindowEx(hwnd, None, "AfxWnd140s", None)
        hwnd = win32gui.FindWindowEx(hwnd, None, "SysTreeView32", None)
        return hwnd

    def get_right_hwnd(self):
        hwnd = self.hwnd_main
        hwnd = win32gui.FindWindowEx(hwnd, None, "AfxMDIFrame140s", None)
        hwnd = win32gui.GetDlgItem(hwnd, 0xE901)
        return hwnd

    def get_left_bottom_tabs(self):
        hwnd = self.hwnd_main
        hwnd = win32gui.FindWindowEx(hwnd, None, "AfxMDIFrame140s", None)
        hwnd = win32gui.FindWindowEx(hwnd, None, "AfxWnd140s", None)
        hwnd = win32gui.FindWindowEx(hwnd, None, "CCustomTabCtrl", None)
        return hwnd

    def get_ocr_hwnd(self):
        tid, pid = win32process.GetWindowThreadProcessId(self.hwnd_main)

        def enum_children(hwnd, results):
            try:
                if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                    win32gui.EnumChildWindows(hwnd, handler, results)
            except Exception:
                return

        def handler(hwnd, results):
            if win32gui.GetClassName(hwnd) == "Static":
                results.append(hwnd)
                return False
            enum_children(hwnd, results)
            return len(results) == 0

        popups = []
        windows = []
        win32gui.EnumThreadWindows(tid, lambda hwnd, line: line.append(hwnd), windows)
        for hwnd in windows:
            if not handler(hwnd, popups):
                break
        for ctrl in popups:
            text = get_text(ctrl)
            if "检测到您正在拷贝数据" in text:
                return ctypes.windll.user32.GetWindow(ctrl, win32con.GW_HWNDNEXT)
        return 0

    def get_balance(self):
        self.switch_to_normal()
        hot_key(["F4"])
        self.refresh()
        hwnd = self.get_right_hwnd()
        data = {}
        for key, cid in BALANCE_CONTROL_ID_GROUP.items():
            ctrl = win32gui.GetDlgItem(hwnd, cid)
            if ctrl > 0 and win32gui.IsWindowVisible(ctrl):
                data[key] = get_text(ctrl)
        return {
            "code": 0,
            "status": "succeed",
            "data": data,
        }

    def get_position(self):
        self.switch_to_normal()
        hot_key(["F1"])
        hot_key(["F6"])
        self.refresh()
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x417)

        self.copy_table(ctrl)

        data = None
        retry = 0
        while not data and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            data = get_clipboard_data()
        if data:
            return {
                "code": 0,
                "status": "succeed",
                "data": parse_table(data),
            }
        return {"code": 1, "status": "failed"}

    def get_active_orders(self):
        self.switch_to_normal()
        hot_key(["F1"])
        hot_key(["F8"])
        self.refresh()
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x417)

        self.copy_table(ctrl)

        data = None
        retry = 0
        while not data and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            data = get_clipboard_data()
        if data:
            return {
                "code": 0,
                "status": "succeed",
                "data": parse_table(data),
            }
        return {"code": 1, "status": "failed"}

    def get_filled_orders(self):
        self.switch_to_normal()
        hot_key(["F2"])
        hot_key(["F7"])
        self.refresh()
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x417)

        self.copy_table(ctrl)

        data = None
        retry = 0
        while not data and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            data = get_clipboard_data()
        if data:
            return {
                "code": 0,
                "status": "succeed",
                "data": parse_table(data),
            }
        return {"code": 1, "status": "failed"}

    def sell(self, stock_no, amount, price):
        self.switch_to_normal()
        hot_key(["F2"])
        time.sleep(sleep_time)
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x408)
        set_text(ctrl, stock_no)
        time.sleep(sleep_time)
        if price is not None:
            time.sleep(sleep_time)
            price = "%.3f" % price
            ctrl = win32gui.GetDlgItem(hwnd, 0x409)
            set_text(ctrl, price)
            time.sleep(sleep_time)
        ctrl = win32gui.GetDlgItem(hwnd, 0x40A)
        set_text(ctrl, str(amount))
        time.sleep(sleep_time)
        hot_key(["enter"])
        result = None
        retry = 0
        while retry < retry_time:
            time.sleep(sleep_time)
            result = self.get_result()
            if result:
                hot_key(["enter"])
                return result
            hot_key(["y"])
            retry += 1
        return {
            "code": 2,
            "status": "unknown",
            "msg": "获取结果失败,请自行确认订单状态",
        }

    def buy(self, stock_no, amount, price):
        self.switch_to_normal()
        hot_key(["F1"])
        time.sleep(sleep_time)
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x408)
        set_text(ctrl, stock_no)
        time.sleep(sleep_time)
        if price is not None:
            time.sleep(sleep_time)
            price = "%.3f" % price
            ctrl = win32gui.GetDlgItem(hwnd, 0x409)
            set_text(ctrl, price)
            time.sleep(sleep_time)
        ctrl = win32gui.GetDlgItem(hwnd, 0x40A)
        set_text(ctrl, str(amount))
        time.sleep(sleep_time)
        hot_key(["enter"])
        result = None
        retry = 0
        while retry < retry_time:
            time.sleep(sleep_time)
            result = self.get_result()
            if result:
                hot_key(["enter"])
                return result
            hot_key(["y"])
            retry += 1
        return {
            "code": 2,
            "status": "unknown",
            "msg": "获取结果失败,请自行确认订单状态",
        }

    def sell_kc(self, stock_no, amount, price):
        self.switch_to_kechuang()
        self.click_kc_sell()
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x408)
        set_text(ctrl, stock_no)
        time.sleep(sleep_time)
        if price is not None:
            time.sleep(sleep_time)
            price = "%.3f" % price
            ctrl = win32gui.GetDlgItem(hwnd, 0x409)
            set_text(ctrl, price)
            time.sleep(sleep_time)
        ctrl = win32gui.GetDlgItem(hwnd, 0x40A)
        set_text(ctrl, str(amount))
        time.sleep(sleep_time)
        hot_key(["enter"])
        result = None
        retry = 0
        while retry < retry_time:
            time.sleep(sleep_time)
            result = self.get_result()
            if result:
                hot_key(["enter"])
                return result
            hot_key(["y"])
            retry += 1
        return {
            "code": 2,
            "status": "unknown",
            "msg": "获取结果失败,请自行确认订单状态",
        }

    def buy_kc(self, stock_no, amount, price):
        self.switch_to_kechuang()
        self.click_kc_buy()
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x408)
        set_text(ctrl, stock_no)
        time.sleep(sleep_time)
        if price is not None:
            time.sleep(sleep_time)
            price = "%.3f" % price
            ctrl = win32gui.GetDlgItem(hwnd, 0x409)
            set_text(ctrl, price)
            time.sleep(sleep_time)
        ctrl = win32gui.GetDlgItem(hwnd, 0x40A)
        set_text(ctrl, str(amount))
        time.sleep(sleep_time)
        hot_key(["enter"])
        result = None
        retry = 0
        while retry < retry_time:
            time.sleep(sleep_time)
            result = self.get_result()
            if result:
                hot_key(["enter"])
                return result
            hot_key(["y"])
            retry += 1
        return {
            "code": 2,
            "status": "unknown",
            "msg": "获取结果失败,请自行确认订单状态",
        }

    def cancel(self, entrust_no):
        self.switch_to_normal()
        hot_key(["F3"])
        self.refresh()
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x417)

        self.copy_table(ctrl)

        data = None
        retry = 0
        while not data and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            data = get_clipboard_data()
        if data:
            entrusts = parse_table(data)
            find = None
            for i, entrust in enumerate(entrusts):
                if str(entrust["合同编号"]) == str(entrust_no):
                    find = i
                    break
            if find is None:
                return {"code": 1, "status": "failed", "msg": "没找到指定订单"}
            left, top, right, bottom = win32gui.GetWindowRect(ctrl)
            x = 50 + left
            y = 30 + 16 * find + top
            win32api.SetCursorPos((x, y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(sleep_time)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(sleep_time)
            hot_key(["enter"])
            return {"code": 0, "status": "succeed"}
        return {"code": 1, "status": "failed"}

    def get_result(self, cid=0x3EC):
        tid, pid = win32process.GetWindowThreadProcessId(self.hwnd_main)

        def enum_children(hwnd, results):
            try:
                if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                    win32gui.EnumChildWindows(hwnd, handler, results)
            except Exception:
                return

        def handler(hwnd, results):
            if (
                win32api.GetWindowLong(hwnd, win32con.GWL_ID) == cid
                and win32gui.GetClassName(hwnd) == "Static"
            ):
                results.append(hwnd)
                return False
            enum_children(hwnd, results)
            return len(results) == 0

        popups = []
        windows = []
        win32gui.EnumThreadWindows(tid, lambda hwnd, line: line.append(hwnd), windows)
        for hwnd in windows:
            if not handler(hwnd, popups):
                break
        if popups:
            ctrl = popups[0]
            text = get_text(ctrl)
            if "已成功提交" in text:
                return {
                    "code": 0,
                    "status": "succeed",
                    "msg": text,
                    "entrust_no": text.split("合同编号：")[1].split("。")[0],
                }
            else:
                return {
                    "code": 1,
                    "status": "failed",
                    "msg": text,
                }

    def refresh(self):
        hot_key(["F5"])
        time.sleep(refresh_sleep_time)

    def active_mian_window(self):
        if self.hwnd_main is not None:
            ctypes.windll.user32.SwitchToThisWindow(self.hwnd_main, True)
            time.sleep(sleep_time)

    def right_click_menu(self, hwnd, x, y, idx=None, key=None):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        x = left + x if x > 0 else right + x
        y = top + y if y > 0 else bottom + y
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        time.sleep(sleep_time)
        if idx is not None:
            while idx >= 0:
                hot_key(["down_arrow"])
                idx -= 1
            hot_key(["enter"])
        elif hot_key is not None:
            if isinstance(key, list):
                hot_key(key)
            else:
                hot_key([key])

    def switch_to_normal(self):
        tabs = self.get_left_bottom_tabs()
        left, top, right, bottom = win32gui.GetWindowRect(tabs)
        x = left + 10
        y = top + 5
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(sleep_time)

    def switch_to_kechuang(self):
        tabs = self.get_left_bottom_tabs()
        left, top, right, bottom = win32gui.GetWindowRect(tabs)
        x = left + 200
        y = top + 5
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(sleep_time)

    def click_kc_buy(self):
        tree = self.get_tree_hwnd()
        left, top, right, bottom = win32gui.GetWindowRect(tree)
        x = left + 10
        y = top + 10
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(sleep_time)

    def click_kc_sell(self):
        tree = self.get_tree_hwnd()
        left, top, right, bottom = win32gui.GetWindowRect(tree)
        x = left + 10
        y = top + 30
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(sleep_time)

    def copy_table(self, hwnd):
        win32gui.SetForegroundWindow(hwnd)
        os.system("echo off | clip")
        hot_key(["ctrl", "c"])
        self.input_ocr()

    def input_ocr(self):
        ocr = self.get_ocr_hwnd()
        if ocr > 0:
            self.capture_window(ocr, "ocr.png")
            with open("ocr.png", "rb") as f:
                data = f.read()
                code = DdddOcr.classification(data)
                ctrl = ctypes.windll.user32.GetWindow(ocr, win32con.GW_HWNDNEXT)
                ctrl = ctypes.windll.user32.GetWindow(ctrl, win32con.GW_HWNDNEXT)
                ctrl = ctypes.windll.user32.GetWindow(ctrl, win32con.GW_HWNDNEXT)
                set_text(ctrl, code)
                hot_key(["enter"])

    def capture_window(self, hwnd, file_name):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        hdc = win32gui.GetWindowDC(hwnd)
        dc = win32ui.CreateDCFromHandle(hdc)
        cdc = dc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(dc, width, height)
        cdc.SelectObject(bmp)
        cdc.BitBlt((0, 0), (width, height), dc, (0, 0), win32con.SRCCOPY)

        info = bmp.GetInfo()
        bits = bmp.GetBitmapBits(True)
        img = Image.frombuffer(
            "RGB", (info["bmWidth"], info["bmHeight"]), bits, "raw", "BGRX", 0, 1
        )

        win32gui.DeleteObject(bmp.GetHandle())
        dc.DeleteDC()
        cdc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hdc)

        img.save(file_name)

    def test(self):
        pass
