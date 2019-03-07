import unittest
import numpy as np
import numpy.testing as npt
import vidmods as vm


class TestHalignMethods(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(Exception):
            vm.halign([])

    def test_array(self):
        img_in = np.zeros(5, dtype=int)
        with self.assertRaises(Exception):
            vm.halign(img_in)

    def test_zeros(self):
        img_in = np.zeros([5, 5], dtype=int)
        npt.assert_allclose(vm.halign(img_in), img_in)

    def test_twos(self):
        img_in = np.zeros([5, 5], dtype=int) + 2
        npt.assert_allclose(vm.halign(img_in), img_in)

    def test_noise(self):
        np.random.seed(42)
        img_in = np.random.rand(5, 5)
        npt.assert_allclose(vm.halign(img_in), img_in)

    def test_float(self):
        img_in = np.zeros([5, 5], dtype=float) + 2.0
        npt.assert_allclose(vm.halign(img_in), img_in)

    def test_no_shift(self):
        img_out = np.zeros([5, 5], dtype=int)
        img_out[1:4, 1:4] = 1
        img_in = img_out
        npt.assert_allclose(vm.halign(img_in), img_out)

    def test_easy_shift(self):
        img_out = np.zeros([7, 7], dtype=int)
        img_out[:, 2:6] = 1
        img_in = np.copy(img_out)
        img_in[1, :] = [0, 1, 1, 1, 1, 0, 0]
        npt.assert_allclose(vm.halign(img_in), img_out)

    def test_hard_shift(self):
        img_out = np.zeros([10, 10], dtype=int)
        img_out[0:10, 0:9] = 1
        img_in = np.copy(img_out)
        img_in[1, :] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        npt.assert_allclose(vm.halign(img_in), img_out)

    def test_realistic_shift(self):
        np.random.seed(42)
        img_out = np.zeros([50, 50], dtype=int)
        img_out[5:45, 5:45] = np.random.rand(40, 40)
        img_in = np.copy(img_out)
        shift = np.random.randint(-2, high=3, size=50)
        for line in range(0, 50):
            img_in[line, :] = np.roll(img_in[line, :], shift)
        npt.assert_allclose(vm.halign(img_in), img_out)


if __name__ == '__main__':
    unittest.main()
