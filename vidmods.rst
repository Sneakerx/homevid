Video Processing Modules
************************
.. automodule:: vidmods

time_base_correction()
======================
.. autofunction:: vidmods.time_base_correction

Example
-------
Load an image and observe typical VHS horizontal line-by-line shifts.
Then correct the hotizontal alignment using time_base_correction()

.. plot::

    import matplotlib.pyplot as plt
    import vidmods as vm
    fig = plt.figure(figsize=(10,5))
    img = plt.imread("./images/original.png")
    img_out = vm.time_base_correction(img)
    ax = plt.subplot(121)
    ax.annotate('shifted', xy=(5, 180), xycoords='data',
        xytext=(5, 80), textcoords='offset points',
        bbox=dict(boxstyle="round", fc="0.8"),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="angle,angleA=90,angleB=0,rad=10"))
    plt.imshow(img, cmap='gray')
    plt.title('original')
    ax = plt.subplot(122)
    ax.annotate('corrected', xy=(5, 180), xycoords='data',
        xytext=(5, 80), textcoords='offset points',
        bbox=dict(boxstyle="round", fc="0.8"),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="angle,angleA=90,angleB=0,rad=10"))
    plt.imshow(img_out, cmap='gray')
    plt.title('processed')
    fig.tight_layout(pad=1.0)


test()
======
.. autofunction:: vidmods.test

Example
-------