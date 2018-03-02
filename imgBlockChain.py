import Image, hashlib, string, binascii,os
from random import *
from Crypto import Random
from Crypto.Cipher import AES
from argparse import ArgumentParser
from Crypto.Util import Counter
import random

def encrypt(image, AESscheme):
    # Turn image into something we can encrypt
    imgarray = bytes(image.tostring())

    img = AESscheme.encrypt(imgarray)
    return img


def decrypt(image, AESscheme):
    # Turn image into something we can decrypt
    imgarray = bytes(image.tostring())

    img = AESscheme.decrypt(imgarray)
    return img


def schemeBuild(key, mode, modeTitle, iv):
    if modeTitle == "AES.MODE_CTR":
        scheme = AES.new(key, mode, counter=Counter.new(128, initial_value=int(binascii.hexlify(key), 16)))
    else:
        scheme = AES.new(key, mode, iv)
    return scheme


def newImg(imgName, encMode, imgExt):
    newImg = '{}{}d.{}'.format(imgName, encMode, imgExt)
    i = 0

    while os.path.isfile(newImg):
        i += 1
        newImg = '{}{}d{}.{}'.format(imgName, encMode, i, imgExt)

    return newImg


def Main(image, AESmode, modeTitle, ENCmode):
    img = Image.open(image)
    imgSize, imgMode = img.size, img.mode
    imgName, imgExt = image.split('.')

    if ENCmode == "Encode":
        psswd = raw_input("Please enter the password. A random password will be provided if left blank - ")
    else:
        psswd = ''
        while psswd == '':
            psswd = raw_input("Please enter the password - ")

    if psswd == '':
        psswd = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation) for _ in range(randint(16, 24)))
        print "Your randomly generated password is " + psswd
        key = hashlib.sha256(psswd).digest()
    else:
        key = hashlib.sha256(psswd).digest()

    iv = Random.new().read(AES.block_size)

    cipherScheme = schemeBuild(key, AESmode, modeTitle, iv)

    if ENCmode == "Encode":
        data = encrypt(img, cipherScheme)
        new = newImg(imgName, ENCmode, imgExt)
        Image.frombytes(imgMode, imgSize, data).save(new)
    else:
        data = decrypt(img, cipherScheme)
        new = newImg(imgName, ENCmode, imgExt)
        Image.frombytes(imgMode, imgSize, data).save(new)


if __name__ == "__main__":
    parser = ArgumentParser(description="Encode/Decode and image using ECB, CBC, CRT, or OFB")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-cbc", "--cbc", action="store_true")
    group.add_argument("-ecb", "--ecb", action="store_true")
    group.add_argument("-ofb", "--ofb", action="store_true")
    group.add_argument("-crt", "--crt", action="store_true")

    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument("-encode", "--encode", action="store_true")
    group1.add_argument("-decode", "--decode", action="store_true")

    parser.add_argument("input_img", help="Image In (tested with PNG)")

    args = parser.parse_args()

    if args.cbc:
        mode = AES.MODE_CBC
        modeTitle = "AES.MODE_CBC"
    elif args.ecb:
        mode = AES.MODE_ECB
        modeTitle = "AES.MODE_ECB"
    elif args.ofb:
        mode = AES.MODE_OFB
        modeTitle = "AES.MODE_OFB"
    else:
        mode = AES.MODE_CTR
        modeTitle = "AES.MODE_CTR"

    if args.encode:
        encryption = "Encode"
    else:
        encryption = "Decode"

    Main(args.input_img, mode, modeTitle, encryption)
