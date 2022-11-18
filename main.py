import pywaves as pw
from constants import *
import datetime, win10toast, json, traceback, time
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_config():
    with open("config.json") as f:
        config = json.load(f)
    return config

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
    :return: last price
    """
    start_timestamp = datetime.datetime.now().timestamp()

    while True:
        cur_timestamp = datetime.datetime.now().timestamp()
        if cur_timestamp - start_timestamp > req_period:
            break
        time.sleep(1)  # to decrease processor load

    return float(pair.last())

def price_signal(last_price, price_sp_high, price_sp_low):
    if last_price >= price_sp_high:
        return "high"
    elif last_price <= price_sp_low:
        return "low"


def change_percent(prev_price, cur_price):

    if cur_price > prev_price:
        percent_allert = f"""{bcolors.GREEN} {round(((cur_price - prev_price) / prev_price) * 100, 3)}% \u25B2"""
    else:
        percent_allert = f"""{bcolors.RED} {round(((cur_price - prev_price) / prev_price) * 100, 3)}% \u25BC"""

    return percent_allert

if __name__ == '__main__':


    config = get_config()

    SP_HIGH = config["price_sp_high"]
    SP_LOW = config["price_sp_low"]
    ASSET_1 = config["asset_1"]
    ASSET_2 = config["asset_2"]
    SERVER_REQUEST_PERIOD = config["req_period"]

    toast = win10toast.ToastNotifier()
    asset_pair = get_assets_pair(ASSET_1, ASSET_2)

    new_price = None
    percent = ""


    while True:

        try:
            last_price = get_last_price(asset_pair, SERVER_REQUEST_PERIOD)
            if last_price != new_price:
                os.system('')  # for colours working in terminal
                if new_price is not None:
                    percent = change_percent(new_price,last_price)  # change in percent

                print(f"""{bcolors.ENDC}{datetime.datetime.now().strftime("%H:%M:%S %d.%m.%y")} Last price {ASSET_1}/{ASSET_2}: {last_price}. {percent:>56}""")
                allert = price_signal(last_price, SP_HIGH, SP_LOW)

                price_setpoint = None
                if allert == "high":
                    price_setpoint = SP_HIGH
                elif allert == "low":
                    price_setpoint = SP_LOW

                if price_setpoint is not None:
                    toast.show_toast(title=f"Price {ASSET_1}/{ASSET_2} allert {allert.upper()}!", msg=f'Last price {ASSET_1}/{ASSET_2} reached {price_setpoint}! Last price = {last_price}',duration=30)

                new_price = last_price

        except Exception as e:
            print(f'{bcolors.RED}Error:\n {traceback.format_exc()}')

        time.sleep(1)  # to decrease processor load


