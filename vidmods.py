import numpy as np


def halign(img_gray):
    """Detects line by line horizontal shifts in an image and corrects them.
    Retrieves a 2D image

    :Args:
        img_gray: a 2D image, thus called 'grayscale'

    :Returns:
        A 2D image of the same size, but with horizontally aligned rows
        The alignment is computed upfront by the median line start index

    :Raises:
        An error occurred accessing the image.
    """

    # check input. First convert to array to use array checks.
    img_gray = np.asarray(img_gray)
    if img_gray.size == 0:
        raise Exception("Received [] input, need 2D image.")
    if img_gray.ndim == 1:
        raise Exception("Received 1D input, need 2D image.")
    if img_gray.ndim == 2:
        Iwidth = img_gray.shape[1]
        Iheight = img_gray.shape[0]
    if img_gray.ndim > 2:
        raise Exception("Received >2 dimensional input, need 2D image.")

    # intensity of a pixel must be below threshold to be marked as sync-line
    thresh = np.mean(img_gray) / 10

    # limit the possible line start by default minimum and maximum.
    d_linestart = -1
    d_linestop = Iwidth

    # default out
    img_out = np.copy(img_gray)

    # get pixels below threshold
    mask = (img_gray < thresh)

    # get transitions along 'x' to find start==-1 and stop==1 in each line.
    line_check = np.diff(np.median(mask, axis=0))
    if not np.any(line_check):
        return img_out

    # detect start
    frame_linestart = np.argwhere(line_check == -1)
    # remove elements that are too big
    # frame_line_start = [item for item in frame_line_start if item < Iwidth/2]
    # print(frame_line_start)

    # detect end
    frame_linestop = np.argwhere(line_check == 1)
    # remove elements that are too small
    # frame_line_stop  = [item for item in frame_line_stop if item > Iwidth/2]
    # print(frame_line_stop)

    # set new values if something was found, else keep the previous value
    d_linestart = d_linestart if frame_linestart.size == 0 else frame_linestart[0]
    d_linestop = d_linestop if frame_linestop.size == 0 else frame_linestop[0]

    # print('Mean: ', np.mean(img_gray), ' Start: ', d_linestart, ' Stop: ', d_linestop)

    # create a distance vector from the found linestart for weigthing reasons
    # then compute gradient and weight the amplitudes
    # This way, large peaks near the linestart should be found
    # The higher, the more confident. Thresholding selects the confident ones
    # The missing or filtered elements are interpolated/extrapolated
    # special treatment of lowest lines is TBD
    dist_linestart = np.abs(np.arange(Iwidth) - d_linestart) + 1
    dist_linestop = np.abs(np.arange(Iwidth) - d_linestop) + 1
    img_diff = np.diff(img_gray, axis=1, append=1)
    weight_start = img_diff / dist_linestart
    weight_stop = img_diff / dist_linestop
    # this vector now contains the max value --> confidence level
    # As improvement low values can be removed and interpolated from neighbours
    v_linestart = np.amax(weight_start, axis=1)
    I_linestart = np.argmax(weight_start, axis=1)
    v_linestop  = np.amin(weight_stop, axis=1)
    I_linestop  = np.argmin(weight_stop, axis=1)

    # pad front with zeros (=pad) or cut first samples
    # e.g if I_linestart is at  8 and linestart is at 14 we need to pad 6 zeros
    #     if I_linestart is at 18 and linestart is at 14 we need to crop 4
    start_diff = d_linestart - I_linestart
    # padneed    = start_diff.clip(min=0)
    # cropneed   = (-1*start_diff).clip(min=0)

    for line in range(0, Iheight):
        img_out[line, :] = np.roll(img_gray[line, :], start_diff[line])

    return img_out
