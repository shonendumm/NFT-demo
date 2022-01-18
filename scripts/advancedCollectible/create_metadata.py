from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import getBreed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests

# until https://youtu.be/M576WGiDBdQ?t=40608
# download ipfs commandline in order to upload images to ipfs programmatically

def main():
    advanced_collectible = AdvancedCollectible[-1]
    print(f"Your contract is deployed at: {advanced_collectible.address}")
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        # returns a number 0 to 2, then we use python function to return the name
        breed = getBreed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        print(metadata_file_name)
        collectible_metadata = metadata_template
        
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed}"
            print(collectible_metadata)
            # formatting the image_path so that we can get the respective files
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_IPFS(image_path)
            # collectible_metadata["image"] = image_uri

def upload_to_IPFS(filepath):
    # open the image files as read binary
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # upload via IPFS commandline
        # to our own IPFS node, via http api; can check IPFS documentation
        ipfs_url = "http://127.0.0.1:5001"
        # make a post request to its endpoint 
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file":image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/PUG.png" -> "PUG.pug" (We split the string by / into an array, then take the last item)
        filename = filepath.split("/")[-1:][0]
        # this is the image_uri path where the image is stored
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri

