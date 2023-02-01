
import requests
import re
import os
import imghdr


def check_for_image(response):
    if 'image' in response.headers['Content-Type']:

        image_type = imghdr.what('', response.content)
        if image_type:
            print("Image type detected: {0}".format(image_type))
            return True
        else:
            print("Error: Unable to verify the signature of the image")
            exit(1)
    return False


async def get_image(url, name):
    found = False
    for file in os.listdir(os.curdir):
        if file.startswith(name):
            found = True
    if not found:
        try:
            response = requests.get(url)
        except:
            print("Error: While requesting url: {0}".format(url))
            exit(1)

        if response:
            if check_for_image(response):
                extension = os.path.basename(response.headers['Content-Type'])
                if 'content-disposition' in response.headers:
                    content_disposition = response.headers['content-disposition']
                    filename = re.findall("filename=(.+)", content_disposition)
                elif url[-4:] in ['.png', '.jpg', 'jpeg', '.svg']:
                    filename = os.path.basename(url)
                else:
                    filename = name+'.' + str(extension)
                with open(filename, 'wb+') as wobj:
                    wobj.write(response.content)
                print(
                    "Success: Image is saved with name: {0}".format(filename))
            else:
                print("Sorry: The url doesn't contain any image :(")
