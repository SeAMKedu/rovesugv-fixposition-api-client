import json

from fixposition_client import Fixposition


def main():
    # PC must connected to the Fixposition device e.g. via Wi-Fi (SSID: fp-xxxxxx)
    host = "10.0.1.1"
    fixpos = Fixposition(host)
    response = fixpos.sys.info()
    print(json.dumps(response, indent=4))


if __name__ == "__main__":
    main()
