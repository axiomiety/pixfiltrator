import numpy as np
from extract_data import convertBGRToHexScale, PALETTE_RGB_WIDTH, blockify, weigh_blocks, convertToPaletteScale, combine_half_bytes

class MockImage(object):

    def __init__(self, arr):
        # this returns height, width, num channels
        self.shape = len(arr), len(arr[0]), 3
        self.arr = arr

    def __getitem__(self, key):
        return self.arr[key]

def test_img_to_scale():
    """"Given a mock image, extracts the corresponding hexadecimal values"""

    img1 = [
        [ (255,255,0), (255,255,0), (255,255,0), (255,255,0) ],
        [ (255,255,0), (255,0,0), (255,0,0), (255,255,0) ],
        [ (255,255,0), (255,0,0), (255,0,0), (255,255,0) ],
        [ (255,255,0), (255,255,0), (255,255,0), (255,255,0)],
    ]

    SIZE = 4
    blocks = blockify(MockImage(img1), SIZE)
    # we're expecting a single block
    assert len(blocks) == 1
    extract = weigh_blocks(blocks, SIZE, sum_values=True)
    assert [convertToPaletteScale(ex) for ex in extract] == [5]

    img2 = [
        # block 1
        [ (255,255,0), (255,255,0), (255,255,0), (255,255,0) ],
        [ (255,255,0), (255,0,0), (255,0,0), (255,255,0) ],
        [ (255,255,0), (255,0,0), (255,0,0), (255,255,0) ],
        [ (255,255,0), (255,255,0), (255,255,0), (255,255,0)],
        # block 2
        [ (255,255,0), (255,255,0), (255,255,0), (255,255,0) ],
        [ (255,255,0), (PALETTE_RGB_WIDTH*2,0,0), (PALETTE_RGB_WIDTH*2,0,0), (255,255,0) ],
        [ (255,255,0), (PALETTE_RGB_WIDTH*2,0,0), (PALETTE_RGB_WIDTH*2,0,0), (255,255,0) ],
        [ (255,255,0), (255,255,0), (255,255,0), (255,255,0)],
    ]

    blocks = blockify(MockImage(img2), SIZE)
    # we're expecting two blocks
    assert len(blocks) == 2
    extract = weigh_blocks(blocks, SIZE, sum_values=True)
    assert [convertToPaletteScale(ex) for ex in extract] == [5,2]

def test_combine_half_bytes():
    half_bytes1 = [5,2]
    assert combine_half_bytes(half_bytes1) == [0x52]    
    
def test_scale_conversion():
    assert 0 == convertBGRToHexScale([0,0,0])
    # below threshold
    assert 1 == convertBGRToHexScale([PALETTE_RGB_WIDTH + PALETTE_RGB_WIDTH//2,0,0])
    # above threshold
    assert 2 == convertBGRToHexScale([PALETTE_RGB_WIDTH + PALETTE_RGB_WIDTH//2+1,0,0])
    assert 15 == convertBGRToHexScale([255,255,200])

def test_blockify():
    img1 = [
        [ (1,1,1), (1,1,1) ],
        [ (1,1,1), (1,1,1) ],
    ]
    assert [[3], [3], [3], [3]] == blockify(MockImage(img1), 1)
    assert [[3, 3, 3, 3]] == blockify(MockImage(img1), 2)

    img2 = [
        [ (1,1,1), (1,1,1), (4,4,4), (4,4,4) ],
        [ (1,1,1), (1,1,1), (4,4,4), (4,4,4) ],
        [ (3,3,3), (3,3,3), (2,2,2), (2,2,2) ],
        [ (3,3,3), (3,3,3), (2,2,2), (2,2,2) ],
    ]
    assert [[3, 3, 3, 3], [12, 12, 12, 12], [9, 9, 9, 9], [6, 6, 6, 6]] == blockify(MockImage(img2), 2)

def test_weight_fns():
    # 2x2x4 block size
    tally1 = [
        [1,1,1,1], [2,2,2,2], [3,3,3,3], [4,4,4,4]
    ]
    assert tally1 == weigh_blocks(tally1, 2) # width < 3, so it's a no-op
    # 3x3x1 block size
    tally2 = [
        [1,1,1,
         1,2,1,
         1,1,1],
    ]
    expected2 = [np.array(
        [0,0,0,
         0,2,0,
         0,0,0])
    ]
    ret = weigh_blocks(tally2, 3)
    comp = [np.array_equal(act, exp) for (act, exp) in zip(ret, expected2)]
    assert all(comp)
    # 3x3x4 block size
    tally3 = [
        [1,1,1,
         1,2,1,
         1,1,1],
        [1,1,1,
         1,3,1,
         1,1,1],
        [1,1,1,
         1,4,1,
         1,1,1],
        [1,1,1,
         1,5,1,
         1,1,1],
    ]
    expected3 = [np.array(
        [0,0,0,
         0,2,0,
         0,0,0]),
         np.array(
        [0,0,0,
         0,3,0,
         0,0,0]),
         np.array(
        [0,0,0,
         0,4,0,
         0,0,0]),
         np.array(
        [0,0,0,
         0,5,0,
         0,0,0])
    ]
    ret = weigh_blocks(tally3, 3)
    comp = [np.array_equal(act, exp) for (act, exp) in zip(ret, expected3)]
    assert all(comp)
    # 4x4x1 block size
    tally4 = [
        [1,1,1,1,
         1,2,2,1,
         1,2,2,1,
         1,1,1,1],
    ]
    expected4 = [np.array(
        [0,0,0,0,
         0,0.5,0.5,0,
         0,0.5,0.5,0,
         0,0,0,0]),
    ]
    ret = weigh_blocks(tally4, 4)
    comp = [np.array_equal(act, exp) for (act, exp) in zip(ret, expected4)]
    assert all(comp)