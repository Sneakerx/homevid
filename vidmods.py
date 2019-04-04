"""
This module contains some useful image processing functions.
"""

import numpy as np
import matplotlib.pyplot as plt


def time_base_correction(img_in):
    """
    Detects and corrects line by line horizontal shifts in an image.
    This is done in two steps:

    1. identify starting and trailing black pixels globally in image.
       In case no global offset is found, just return the input.
    2. identify line shifts relative to the global offset.
       Move the individual lines to match the global offset.

    Returns a 2D image

    :Args:
        img_in: a 2D or 3D input image

    :Returns:
        A 2D/3D image of the same size, but with horizontally aligned rows
        The alignment is computed upfront by the median line start index

    :Raises:
        An error occurred accessing the image.

    """

    # check input. First convert to array to use array checks.
    img_in = np.asarray(img_in)

    if (img_in.ndim < 2 or img_in.ndim > 3):
        raise Exception("Received wrong input dimension, need 2D or 3D image.")
    if img_in.ndim == 2:
        Idim = 0
        img_gray = np.copy(img_in)
    if img_in.ndim == 3:
        Idim = img_in.shape[2]
        img_gray = rgb2gray(img_in)

    Iwidth = img_in.shape[1]
    Iheight = img_in.shape[0]

    # Intensity of a pixel must be below threshold to be marked as sync-line.
    # On VHS black is encoded as 0.01V of 0.7V, so 1.4% of the maximum value.
    black = 0.01 / 0.7

    # Use 3sigma value here.
    confidence = 3

    if np.mean(img_gray) > 1:
        max_value = 255
    else:
        max_value = 1

    thresh = max_value * black * confidence

    # limit the possible line start by default minimum and maximum.
    d_linestart = -1
    d_linestop = Iwidth

    # default out
    img_out = np.copy(img_in)

    # get pixels below threshold
    mask = (img_gray < thresh)

    # get transitions along 'x' to find start==-1 and stop==1 in each line.
    line_check = np.diff(np.median(mask, axis=0))
    if not np.any(line_check):
        return img_out

    # detect start
    f_linestart = np.argwhere(line_check == -1)

    # detect end
    f_linestop = np.argwhere(line_check == 1)

    # set new values if something was found, else keep the previous value
    d_linestart = d_linestart if f_linestart.size == 0 else f_linestart[0]
    d_linestop = d_linestop if f_linestop.size == 0 else f_linestop[0]

    """
    # create a distance vector from the found linestart for weigthing reasons
    # then compute gradient and weight the amplitudes
    # This way, large peaks near the linestart should be found
    # The higher, the more confident. Thresholding selects the confident ones
    # The missing or filtered elements are interpolated/extrapolated
    # special treatment of lowest lines is TBD
    dist_linestart = np.abs(np.arange(Iwidth - 1) - d_linestart) + 1
    dist_linestop = np.abs(np.arange(Iwidth - 1) - d_linestop) + 1
    img_diff = np.diff(img_gray, axis=1)
    weight_start = img_diff / dist_linestart**4
    weight_stop = img_diff / dist_linestop**4
    plt.plot(weight_start)
    plt.show()

    # this vector now contains the max value --> confidence level
    # As improvement low values can be removed and interpolated from neighbours
    I_linestart = np.argmax(weight_start, axis=1)
    I_linestop = np.argmin(weight_stop, axis=1)
    print(I_linestart)

    # pad front with zeros (=pad) or cut first samples
    # e.g if I_linestart is at  8 and linestart is at 14 we need to pad 6 zeros
    #     if I_linestart is at 18 and linestart is at 14 we need to crop 4
    start_diff = d_linestart - I_linestart
    # padneed    = start_diff.clip(min=0)
    # cropneed   = (-1*start_diff).clip(min=0)
    """
    lines_check = np.argwhere(mask > 0)
    print(lines_check)

    for line in range(0, Iheight):
        if Idim > 0:
            for ndim in range(0, Idim):
                img_out[line, :, ndim] = \
                    np.roll(img_in[line, :, ndim], start_diff[line])
        else:
            img_out[line, :] = np.roll(img_in[line, :], start_diff[line])

    return img_out


def rgb2gray(rgb):
    """
    Converts an RGB image to grayscale

    :Args:
        rgb: red, green, blue input image

    :Returns:
        luminance component
    """

    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


def yuv2rgb(yuv):
    """
    Converts a YUV image to RGB

    :Args:
        yuv: luminance (y), blue/yellow-diff (u), red/green-diff (v)

    :Returns:
        rgb: red, green, blue
    """

    # (y, u, v) = yuv
    y, u, v = yuv[:, :, 0], yuv[:, :, 1], yuv[:, :, 2]
    r = y + 1.14 * v
    g = y - 0.39 * u - 0.58 * v
    b = y + 2.03 * u

    return (r, g, b)


def rgb2yuv(rgb):
    """
    Converts an RGB image to YUV

    :Args:
        rgb: red, green, blue

    :Returns:
        yuv: luminance (y), blue/yellow-diff (u), red/green-diff (v)
    """

    rgb = np.asarray(rgb)

    if rgb.ndim == 1:
        r, g, b = rgb[0], rgb[1], rgb[2]
    elif rgb.ndim == 3:
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    else:
        raise Exception("Received neither input tuple nor 3D input image.")

    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = -0.147 * r + -0.289 * g + 0.436 * b
    v = 0.615 * r + -0.515 * g + -0.100 * b

    return (y, u, v)


def deinterlace_blend(img_in):
    """
    Deinterlaces a video frame based on VLC's 'blend' option
    """

    # copy input to output
    img_out = np.copy(img_in)

    # second to last line are a 'blend' of odd and even lines
    # this can be expressed as convolution with a [1 1]/2 kernel
    # img_out[1:, :] = np.convolve(img_in, [.5, .5], method='valid')
    for line in range(0, img_in.shape[0] - 1):
        for ndim in range(0, img_in.shape[2]):
            img_out[line, :, ndim] = 0.5 * img_in[line, :, ndim] \
                + 0.5 * img_in[line + 1, :, ndim]

    return img_out


# Schwarzanhebung 0.01V von 0.7V = Grauwert 4 von 256
# 15625 kHz Zeilenfrequenz (625 Zeilen bei 25 Bildern)
#   von den 64 µs sind nur 52 µs aktiv nutzbar
# Luma 3 MHz -> 312 Linie/Zeile Abtastung (156 sinusiods -> 4 pix)
# Chroma 500 kHz -> 52 Linie/Zeile Abtastung (26 sinusoids -> 28 pix)
