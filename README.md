# Image Steganography
Hides a message or file inside an image by changing the last bit(s) of each pixel's rgb values. Uses python and OpenCV.

# Usage

Use with the python 3 shell (interactive interpreter). Make sure to <a href="https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup">install OpenCV for Python</a>.

Functions of interest to the end user:

 * conceal_text_in_image
 * unconceal_text_in_image
 * conceal_file_in_image
 * unconceal_file_in_image

#Examples

## Setup
```
image-steganography $ pip install opencv-python
image-steganography $ python3
>>> from image_steganography import *
```

## Text in an Image

Image:

![xp.png](examples/xp.png)

### Conceal

To conceal:

```
>>> conceal_text_in_image("examples/xp.png", "examples/xp-steg.png", "The quick brown fox jumped over the lazy dog")
Number of characters: 44
Bits per character: 7
Text size: 38.5B (308 bits)
Image capacity: 26.5KiB (216900 bits)
Space left in image: 26.4KiB (216594 bits)
```

Note text is concealed at 7 bits per character.

Image with concealed text:

![xp-steg.png](examples/xp-steg.png)

### Unconceal

To unconceal 50 characters at 7 bits per character:

```
>>> unconceal_text_in_image("examples/xp-steg.png", 60, 7)
The quick brown fox jumped over the lazy dogIc/\osw#;Gr0Elb
```

After 50 characters are decoded the text is garbage - just random data from the least significant bits of the image.

## Image in a Image

Big Image:

![xp.png](examples/big-pic.png)

Small Image:

![xp.png](examples/small-pic.png)

### Conceal

To conceal:

```
conceal_file_in_image("examples/big-pic.png", "examples/big-pic-steg.png", "examples/small-pic.png")
	Size: 177.4KiB (1453624 bits)
Image capacity: 759.4KiB (6220800 bits)
Space left in image: 581.9KiB (4767176 bits)
```

Note 1453624 bits used to store image.

Big image with concealed small image:

![xp.png](examples/big-pic-steg.png)

### Unconceal

To unconceal 1453624 bits into an image:

```
>>> unconceal_file_in_image("examples/big-pic-steg.png", "examples/small-pic-output.png", 1453624)
```

Unconcealed small image:

![xp.png](examples/small-pic-output.png)
