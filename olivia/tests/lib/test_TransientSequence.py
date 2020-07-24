from olivia.lib.transientsequence import TransientSequence


def test_create_simple():
    size = 10
    s = TransientSequence(size)
    assert len(s) == size, 'Wrong size'
    for n in range(size):
        assert isinstance(s[n], object), 'Not initialized value in new TransientSequence'
    # list
    for n in range(size):
        s[n] = [s for s in range(n)]
    for n in range(size):
        assert s[n] == [s for s in range(n)], 'Diff. in simple lists'
    # set
    for n in range(size):
        s[n] = {s for s in range(n)}
    for n in range(size):
        assert s[n] == {s for s in range(n)}, 'Diff in simple sets'


def test_create_typed():
    s = TransientSequence(2, class_type=set)
    s[0] = None
    assert isinstance(s[0], set), 'Empty object not created from None assignment'
    s[0] = [1, 2, 3]
    assert isinstance(s[0], set), 'Wrong object type'
    assert s[0] == {1, 2, 3}, 'Object not matching'


def test_compress_dict():
    threshold = 10
    s = TransientSequence(2, class_type=dict,
                          compression_threshold=threshold, expiry_array=None)
    d0 = {n: n + 1 for n in range(threshold)}  # not compressed
    d1 = {n: n + 1 for n in range(threshold + 1)}  # compressed
    s[0] = d0
    s[1] = d1
    assert s[0] == d0, 'Non matching dicts'
    assert s[1] == d1, 'Non matching dicts'
    # a quirky access to internal list to check compression
    assert s._data[0] == d0, 'Non matching dict'
    assert s._data[1] != d1, 'Dict not compressed'


def test_expiry_compress_set():
    threshold = 2
    s = TransientSequence(10, class_type=set,
                          compression_threshold=threshold, expiry_array=[1, 2])
    s[0] = {1, 2, 3, 4}
    s[1] = {1, 2, 3}
    assert s[0] == {1, 2, 3, 4}, 'Non matching set'  # live
    assert len(s[0]) == 0, 'Not expired'  # expired
    assert s[1] == {1, 2, 3}, 'Non matching set'  # live
    assert s[1] == {1, 2, 3}, 'Non matching set'  # live
    assert len(s[1]) == 0, 'Not expired'  # expired


def test_custom_compressor():

    s = TransientSequence(10, class_type=list, compressor=lambda i: ''.join(i),
                          decompressor=lambda o: list([*o]), compression_threshold=1)
    test_list = ['a', 'b', 'c', 'd']
    s[0] = test_list
    assert s._data[0] != test_list, 'Not compressed'
    assert s[0] == test_list, 'Non matching decompressed get_item'