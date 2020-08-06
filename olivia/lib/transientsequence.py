
"""TransientSequence class."""

import pickle
import zlib
from collections.abc import Sequence


class TransientSequence(Sequence):

    """
    A fixed size Sequence type for managing large in-memory structures.

    A TransientSequence is a fixed size linear array of arbitrary objects that are compressed/decompressed
    on the fly and automatically deleted from memory after a certain number of accesses.

    Objects must implement __len__(). Only simple accessors are supported (no slicing).

    TransientSequence has been developed to efficiently manage large successor sets of graphs using bit vector
    representations. It should be used with care in a general setting as implicit compression on accessors
    could be dangerous.

    Parameters
    ----------
    size: int
        Amount of objects to be stored (fixed).
    class_type: class, optional
        Type of objects to be stored.
    compressor: function, optional
        Compressing function. Defaults to simple pickle/zlib compressor.
    decompressor: function, optional
        Decompressing function. Defaults to simple zlib/unpickle decompressor.
    compression_threshold:  int, optional
        Upper size (len) limit to keep objects uncompressed.
    expiry_array: sequence or None, optional
        Number of accesses per object before deletion. Reassigning reverts the counter to its original value.

    """

    @staticmethod
    def _DEFAULT_COMPRESSOR(value):
        return zlib.compress(pickle.dumps(value))

    @staticmethod
    def _DEFAULT_DECOMPRESSOR(value):
        return pickle.loads(zlib.decompress(value))

    def __init__(self, size, class_type=object, compressor=_DEFAULT_COMPRESSOR.__func__,
                 decompressor=_DEFAULT_DECOMPRESSOR.__func__,
                 compression_threshold=1000, expiry_array=None):
        """
        Create and initialize a TransientSequence.

        Parameters
        ----------
        size: int
            Amount of objects to be stored (fixed).
        class_type: class, optional
            Type of objects to be stored.
        compressor: function, optional
            Compressing function. Defaults to simple pickle/zlib compressor.
        decompressor: function, optional
            Decompressing function. Defaults to simple zlib/unpickle decompressor.
        compression_threshold:  int, optional
            Upper size (len) limit to keep objects uncompressed.
        expiry_array: sequence or None, optional
            Number of accesses per object before deletion. Reassigning reverts the counter to its original value.

        """
        self._data = [None] * size
        self._compressed = [False] * size
        self._ct = compression_threshold
        self._compressor = compressor
        self._decompressor = decompressor
        self._class_type = class_type
        self._expiry = expiry_array
        if expiry_array is not None:
            self._expiry_original = expiry_array.copy()

    def __setitem__(self, index, value):
        """
        Assign value to position 'index'.

        Parameters
        ----------
        index : int
            A position in the TransientSequence.
        value : object
            An object or object of class_type.

        Returns
        -------
        None

        Notes
        -----
        Transparently compresses the object if length > compression_threshold.

        """
        if value is None:
            self._data[index] = None
            return
        if len(value) == 0:
            self._data[index] = None
        if not isinstance(value, self._class_type):
            value = self._class_type(value)
        if len(value) > self._ct:
            self._data[index] = self._compressor(value)
            self._compressed[index] = True
        else:
            self._data[index] = value
            self._compressed[index] = False
        if self._expiry is not None:
            self._expiry[index] = self._expiry_original[index]

    def __getitem__(self, index):
        """
        Return the object at position 'index'.

        Parameters
        ----------
        index : int
            A position in the TransientSequence.

        Returns
        -------
        object : object
            Object or object of class_type.

        Notes
        -----
        Transparently decompresses the object if needed and deletes the reference if compression_threshold
        is exceeded.

        """
        if self._data[index] is None:
            out = self._class_type()
        elif self._compressed[index]:
            out = self._decompressor(self._data[index])
        else:
            out = self._data[index]
        if self._expiry is not None:
            self._expiry[index] -= 1
            if self._expiry[index] == 0:
                self._data[index] = None
        return out

    def __len__(self):
        """
        Return the length of the TransientSequence.

        Returns
        -------
        length : int
            Number of objects in the TransientSequence (length)

        """
        return len(self._data)
