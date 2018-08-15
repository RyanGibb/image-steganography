# Image Steganography
Hides a message or file inside an image by changing the last bit(s) of each pixel's rgb values. Uses python and OpenCV.

# Usage

Use with the python 3 shell (interactive interpreter). Make sure to <a href="https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup">install OpenCV for Python</a>.

This project was build for on the fly scripting, rather than wrapping the code up in a nice command line interface or UI. As such there are a lot of irrelevant functions (irrelevant to the end user, at least). The functions of the most interest to the user will probably be:

 * conceal_text_in_image
 * unconceal_text_in_image
 * conceal_file_in_image
 * unconceal_file_in_image
 
These could be put in a seperate file but for the sake of simplicity they are left with the more bare metal code.
