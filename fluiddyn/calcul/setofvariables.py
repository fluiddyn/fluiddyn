"""Variable container (:mod:`fluiddyn.calcul.setofvariables`)
=============================================================

Provides:

.. autoclass:: SetOfVariables
   :members:
   :private-members:

"""

import numpy as np


class SetOfVariables(np.ndarray):
    """np.ndarray containing the variables.

    Parameters
    ----------

    input_array : :class:`numpy.ndarray`, optional
        Input array, default to None.

    keys : Iterable, optional
        Keys corresponding to the variables, default to None.

    shape_variable : Iterable, optional
        Shape of an array containing one variable, default to None.

    like : :class:`SetOfVariables`, optional
        Model for creating the new :class:`SetOfVariables`, default to None.

    value : Number, optional
        For initialization of the new :class:`SetOfVariables`, default to None.

    info : :class:`str`, optional
        Description, default to None.

    dtype : :class:`numpy.dtype`, optional
        see :class:`numpy.ndarray` help.

    """

    def __new__(
        cls,
        input_array=None,
        keys=None,
        shape_variable=None,
        like=None,
        value=None,
        info=None,
        dtype=None,
        **kwargs,
    ):
        if input_array is not None:
            arr = input_array

            if keys is None:
                raise ValueError(
                    "If input_array is provided, keys has to be provided."
                )

            if len(keys) != arr.shape[0]:
                raise ValueError(
                    "len(keys) has to be equal to input_array.shape[0]"
                )

        else:
            if like is not None:
                info = like.info
                keys = like.keys
                shape = like.shape
                dtype = like.dtype
            elif keys is None or shape_variable is None:
                raise ValueError(
                    "If like is not provided, keys and "
                    "shape_variable should be provided"
                )

            else:
                shape = (len(keys),) + tuple(shape_variable)

            arr = np.empty(shape, dtype=dtype)
            if value is not None:
                arr.fill(value)

        obj = np.asarray(arr, dtype=dtype, **kwargs).view(cls)

        obj.info = info
        obj.keys = tuple(keys)
        obj.nvar = len(keys)

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

        if obj.shape == self.shape:
            self.info = getattr(obj, "info", None)
            self.keys = getattr(obj, "keys", None)
            self.nvar = getattr(obj, "nvar", None)

    def set_var(self, arg, value):
        """Set a variable."""
        if isinstance(arg, int):
            index = arg
        else:
            try:
                index = self.keys.index(arg)
            except ValueError:
                raise ValueError(
                    "'" + arg + "' is not in tuple " + repr(self.keys)
                )

        # warning: copy... costly!
        self[index] = value

    def get_var(self, arg):
        """Get a variable as a np.array."""
        if isinstance(arg, int):
            index = arg
        else:
            try:
                index = self.keys.index(arg)
            except ValueError:
                raise ValueError(
                    "'" + arg + "' is not in tuple " + repr(self.keys)
                )

        return np.asarray(self[index])

    def initialize(self, value=0):
        """Initialize as a constant array."""
        self[:] = value


if __name__ == "__main__":
    # shape_var = (2, 2)
    # keys = ['a', 'b']
    # shape = (len(keys),) + shape_var
    # data = np.arange(reduce(lambda x, y: x*y, shape)).reshape(shape)

    # a = SetOfVariables(data, dtype=None,
    #                   info='poum', keys=keys)

    # print('a:', a)
    # b = 2*a
    # print('b:', b)

    # c = SetOfVariables(like=b, value=2.)
    # print('c:', c)

    # print(type(a*c))
    # print(type(2*c))
    # print(type(c.get_var('a')))

    sov = SetOfVariables(
        keys=["rot_fft"],
        shape_variable=(33, 18),
        dtype=np.complex128,
        info="state_spect",
    )
