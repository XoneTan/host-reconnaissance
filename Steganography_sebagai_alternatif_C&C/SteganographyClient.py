import base64
import png
from auth import authenticate
from datetime import datetime

EOF = "0100100101010101010101100100111101010010010001010011100101000111010101000101010101010110010101000101010100110000010001100100100001010010010100110100010100111101"

def encode_mssg_to_string(message):
    b64 = message.encode('utf8')
    bytes = base64.b64encode(b64)
    bytesrting = "".join(["{:08b}".format(x) for x in bytes])
    bytesrting += EOF
    return bytesrting

def get_pixel(fname):
    img = png.Render(fname).read()
    pixels = img[2]
    return pixels

def encode_pixel_with_message(pixels, bytestring):
    enc_pixels = []
    string_i = 0
    for row in pixels:
        enc_row = []
        for i, char in enumerate(row):
            if string_i >= len(bytestring):
                pixel = row[i]
            else:
                if row[i] % 2 != int(bytestring[string_i]):
                    if row[i] == 0:
                        pixel = 1
                    else:
                        pixel = row[i] - 1
                else:
                    pixel = row[i]
            enc_row.append(pixel)
            string_i += 1

        enc_pixels.append(enc_row)
    return enc_pixels

def write_pixels_to_image(pixels, fname):
    png.from_array(pixels, 'RGB').save(fname)

def upload_image(client):
    """
    Uploads and image to imgur
    """

    config = {
        'album': None,
        'name': new_image,
        'title': new_title,
        'description': 'uploaded at : {0}'.format(datetime.now())
    }

    print('Uploading image...')
    image = client.upload_from_path(new_image, config=config, anon=False)
    print("Done")
    print()

    return image

def main():
    global in_image, new_image, new_title, new_image_path
    in_image = input("enter image name (with .png in it): ")
    in_message = input("enter yout message: ")
    new_image = input("enter new image name (without the .png in it): ")
    new_title = input("enter new title: ")
    new_image_path = new_image + ".png"

    pixels = get_pixel(in_image)
    bytestring = encode_mssg_to_string(in_message)
    epixels = encode_pixel_with_message(pixels, bytestring)
    write_pixels_to_image(epixels, new_image_path)

    client = authenticate()
    image = upload_image(client)


if __name__ == '__main__':
    main()