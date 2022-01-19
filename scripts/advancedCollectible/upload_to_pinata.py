from brownie import config
from pathlib import Path
import requests

PINATA_BASE_URL = 'https://api.pinata.cloud'
endpoint = "/pinning/pinFileToIPFS"

filepath= "./img/shiba-inu.png"

def main():
    upload_to_pinata()

def upload_to_pinata():
    # open the image files as read binary
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # upload via IPFS commandline
        # to our own IPFS node, via http api; can check IPFS documentation

        headers = {
            "pinata_api_key": config["pinata"]["pinata_api_key"],
            "pinata_secret_api_key": config["pinata"]["pinata_secret_api_key"]
        }

        # "./img/PUG.png" -> "PUG.pug" (We split the string by / into an array, then take the last item)
        filename = filepath.split("/")[-1:][0]
        response = requests.post(PINATA_BASE_URL + endpoint, files={"file":(filename, image_binary)}, headers=headers)
        print(response.json())
        ipfs_hash = response.json()["IpfsHash"]
        # https://gateway.pinata.cloud/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?preview=1
        # this is the image_uri path where the image is stored
        image_uri = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        print(image_uri)
        return image_uri