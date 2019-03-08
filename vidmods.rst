Video Processing Modules
************************
.. automodule:: vidmods

halign()
================
.. autofunction:: vidmods.halign

Example
-------
Load an image and observe typical VHS horizontal line-by-line shifts.
Then correct the hotizontal alignment using halign()

.. plot::

    import matplotlib.pyplot as plt
    import vidmods as vm
    img = plt.imread("./images/original.png")
    img_out = vm.halign(img)
    fig = plt.figure()
    plt.imshow(img, cmap='gray')
    plt.title('original')
    fig = plt.figure()
    plt.imshow(img_out, cmap='gray')
    plt.title('processed')


test()
======
.. autofunction:: vidmods.test

Example
-------