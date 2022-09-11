import pywaves as pw
from constants import *


def get_assets_pair(asset1_name:str, asset2_name:str):
    """
    :param asset1_name: asset name from dict in constants
    :param asset2_name: asset name from dict in constants
    :return: AssetPair object
    """

    asset_1 = pw.Asset(assets_dict[asset1_name])
    asset_2 = pw.Asset(assets_dict[asset2_name])

    return pw.AssetPair(asset_1, asset_2)




if __name__ == '__main__':
    usdt_usdn = get_assets_pair("USDT","USDN")

