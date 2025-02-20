"""
python -m pip install hid
ERROR: 无法使用
ImportError: Unable to load any of the following libraries:libhidapi-hidraw.so libhidapi-hidraw.so.0 libhidapi-libusb.so libhidapi-libusb.so.0 libhidapi-iohidmanager.so libhidapi-iohidmanager.so.0 libhidapi.dylib hidapi.dll libhidapi-0.dll

解决办法：把hidapi.dll hidapi.lib hidapi.pdb 扔到python安装路径下即可
寻找python路径的方法：
import sys
print(sys.path) 即可看到
"""
import time

import hid


def list_hid_devices():
    for device in hid.enumerate():
        if device['usage_page'] == 0x01 and device['usage'] == 0x06:  # HID 类型为键盘
            print("Found a keyboard:")
            print(f"Vendor ID: {hex(device['vendor_id'])}")
            print(f"Product ID: {hex(device['product_id'])}")
            print(f"Manufacturer: {device['manufacturer_string']}")
            print(f"Product: {device['product_string']}")
            print(f"Path: {device['path']}")
            VENDOR_ID = device['vendor_id']
            PRODUCT_ID = device['product_id']
            print(VENDOR_ID, PRODUCT_ID)
            with hid.Device(VENDOR_ID, PRODUCT_ID) as device:
                print(f'Device manufacturer: {device.manufacturer}')
                print(f'Product: {device.product}')
                print(f'Serial Number: {device.serial}')
            time.sleep(1)
            break


list_hid_devices()
