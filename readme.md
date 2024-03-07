# download_pics_by_code

download pics with magic code in comments on bilibili.

## usage

```sh
python3 filter_code.py source.txt code.txt
python3 download.py code.txt images/ err.txt  # repeat to deal with random status 502

python3 download.py err.txt images/ err1.txt  # repeat only failed code
```

## requiremnts

```sh
requests
pyrfc6266
urllib3==1.25.11
```