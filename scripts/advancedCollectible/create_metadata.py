from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import getBreed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests, json, os

# until https://youtu.be/M576WGiDBdQ?t=41097
# uploading image to pinata instead of IPFS 

# until https://youtu.be/M576WGiDBdQ?t=40608
# download ipfs commandline in order to upload images to ipfs programmatically

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png"
}


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
            
            # skip upload to ipfs since we already uploaded them.
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_IPFS(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            collectible_metadata["image"] = image_uri
            # metadata completed, so we create a file (.json name) with it
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_IPFS(metadata_file_name)
            # currently false because we uploaded once, so we just skip it

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

