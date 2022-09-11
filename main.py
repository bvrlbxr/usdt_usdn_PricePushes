import pywaves as pw
from constants import *
from config import *
import datetime, win10toast

def get_assets_pair(asset1_name:str, asset2_name:str):
    """
    :param asset1_name: asset name from dict in constants
    :param asset2_name: asset name from dict in constants
    :return: AssetPair object
    """

    asset_1 = pw.Asset(assets_dict[asset1_name])
    asset_2 = pw.Asset(assets_dict[asset2_name])

    return pw.AssetPair(asset_1, asset_2)

def get_last_price(pair:object, req_period:int):
    """
    :param pair: AssetPair object
    :param req_period: server request period (sec)
    :return:
    """
    start_timestamp = datetime.datetime.now().timestamp()

    while True:
        cur_timestamp = datetime.datetime.now().timestamp()
        if cur_timestamp - start_timestamp > req_period:
            break

    return float(pair.last())

def price_signal(last_price, price_setpoint):
    if last_price >= price_setpoint:
        return True

if __name__ == '__main__':

    toast = win10toast.ToastNotifier()
    asset_pair = get_assets_pair(ASSET_1, ASSET_2)

    while True:
        last_price = get_last_price(asset_pair, SERVER_REQUEST_PERIOD)
        allert = price_signal(last_price, PRICE_SETPOINT)

        if allert:
            toast.show_toast(title=f"Price {ASSET_1}/{ASSET_2} allert!", msg=f'Last price {ASSET_1}/{ASSET_2} reached {PRICE_SETPOINT}! Last price = {last_price}',duration=30)
