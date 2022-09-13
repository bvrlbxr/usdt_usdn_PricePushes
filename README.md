# usdt_usdn_PricePushes

push allert in windows when target price reached on waves.exchange (last price).

to compile with pyinstaller in windows:
pyinstaller -D --additional-hooks-dir <hooks dir> --add-data "config.json;." main.py


config.json:
``` 
{
  "req_period" : 3, // waves server request period in seconds
  "asset_1" : "USDT", // assets
  "asset_2" : "USDN",
  "price_sp_high" : 1.09, // setpoint high price
  "price_sp_low" : 1.02  // setpoint low price
}
```

![push allert](https://user-images.githubusercontent.com/28018394/189945050-c7d9a1fb-faad-4f4c-a53a-bff058488e85.png)
