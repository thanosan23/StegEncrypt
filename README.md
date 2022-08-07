# StegEncrypt

Encrypt messages within images

## Steganography
Usually, when one wants to send secret text, they would use a myriad of cryptography tools such as a ceaser cipher or a rot13 cipher. However, instead of obfuscating the text, what if it is possible to conceal the presence of the text? This is steganography. Stenganography is a technique in which data can be hidden **inside** the bytes of another file. 

## Usage
Encoding images:
`python lsb.py encode <original-image-name> <result-image>`

Decoding Images:
`python lsb.py decode <image-with-embedded-message`

## Overview of LSB Steganography
Implementation: `lsb.py`

**NB**: Readers shall be forewarned that this algorithim works well with Bitmap (e.g. PNGs and BMP) images that implement loseless compression. JPEGs won't work well as it implements lossy compression. 

Dangerous thought it may seem, the idea of this steganography technique is hiding the data in the bits that hold the data. More specifically, we will be changing the bits that hold the colour data of the image.
"Won't this corrupt the file and/or change the image's color?" I hear you say. The idea is that if we change the least significant bit (a.k.a LSB, hence the name of the Python file) of the RGB values of the image, we can change the bits of the image without a noticeable change to the human eye. So, when we apply the algorithim to an image, the image with the message embedded in it will seem like the original image.