import unittest
import numpy as np
import numpy.testing as npt
import vidmods as vm
import matplotlib.pyplot as plt


class TestTimeBaseCorrector(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(Exception):
            vm.time_base_correction([])

    def test_array(self):
        img_in = np.zeros(5, dtype=int)
        with self.assertRaises(Exception):
            vm.time_base_correction(img_in)

    def test_zeros(self):
        img_in = np.zeros([5, 5], dtype=int)
        npt.assert_allclose(vm.time_base_correction(img_in), img_in)

    def test_twos(self):
        img_in = np.zeros([5, 5], dtype=int) + 2
        npt.assert_allclose(vm.time_base_correction(img_in), img_in)

    def test_noise(self):
        np.random.seed(42)
        img_in = np.random.rand(5, 5)
        npt.assert_allclose(vm.time_base_correction(img_in), img_in)

    def test_float(self):
        img_in = np.zeros([5, 5], dtype=float) + 2.0
        npt.assert_allclose(vm.time_base_correction(img_in), img_in)

    def test_no_shift(self):
        img_out = np.zeros([5, 5], dtype=int)
        img_out[1:4, 1:4] = 1
        img_in = img_out
        npt.assert_allclose(vm.time_base_correction(img_in), img_out)

    def test_easy_shift(self):
        img_out = np.zeros([7, 7], dtype=int)
        img_out[:, 2:6] = 1
        img_in = np.copy(img_out)
        img_in[1, :] = [0, 1, 1, 1, 1, 0, 0]
        npt.assert_allclose(vm.time_base_correction(img_in), img_out)

    def test_easy_shift_3D(self):
        img_out = np.zeros([7, 7, 3], dtype=int)
        img_out[:, 2:6, :] = 1
        img_in = np.copy(img_out)
        img_in[1, :, 0] = [0, 1, 1, 1, 1, 0, 0]
        img_in[1, :, 1] = [0, 1, 1, 1, 1, 0, 0]
        img_in[1, :, 2] = [0, 1, 1, 1, 1, 0, 0]
        npt.assert_allclose(vm.time_base_correction(img_in), img_out)

    def test_hard_shift(self):
        img_out = np.zeros([10, 10], dtype=int)
        img_out[0:10, 0:9] = 1
        img_in = np.copy(img_out)
        img_in[1, :] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        npt.assert_allclose(vm.time_base_correction(img_in), img_out)

    def test_realistic_shift(self):
        print("HERE")
        np.random.seed(42)
        img_out = np.zeros([50, 50], dtype=float)
        img_out[5:45, 5:45] = 0.1 + np.random.rand(40, 40)
        img_in = np.copy(img_out)
        shift = np.random.randint(-2, high=3, size=50)
        print(shift + 5)
        for line in range(0, 50):
            img_in[line, :] = np.roll(img_in[line, :], shift[line])
        """
        plt.figure(1)
        plt.imshow(img_out)
        plt.figure(2)
        plt.imshow(img_in)
        plt.figure(3)
        plt.imshow(vm.time_base_correction(img_in))
        plt.show()
        """
        npt.assert_allclose(vm.time_base_correction(img_in), img_out)

    def test_realistic_shift_left_aligned(self):
        print("THERE")
        np.random.seed(24)
        img_out = 0.01 / 0.7 * np.random.rand(50, 50)
        img_out[:, 1:41] = np.random.rand(50, 40)
        img_in = np.copy(img_out)
        shift = np.random.randint(-1, high=2, size=50)
        for line in range(0, 50):
            img_in[line, :] = np.roll(img_in[line, :], shift)
        # plt.imshow(img_out)
        # plt.show()
        npt.assert_allclose(vm.time_base_correction(img_in), img_out)

class TestDeinterlaceBlendMethods(unittest.TestCase):

    def test_twos(self):
        img_in = np.zeros([5, 5], dtype=float) + 2
        img_out = np.ones([5, 5], dtype=float)
        img_out[0:5, 0] = 2
        # npt.assert_allclose(vm.deinterlace_blend(img_in), img_out)

"""
class TestRGB2YUVMethods(unittest.TestCase):

    def test_sample(self):
        # print(vm.rgb2yuv((73, 186, 154)))
        # npt.assert_allclose(vm.deinterlace_blend(img_in), img_out)

    def test_matrix(self):
        # print(vm.rgb2yuv(np.zeros([5, 5, 3], dtype=int)))
"""

if __name__ == '__main__':
    unittest.main()
