from PIL import Image


def invert_color(fname):
    im = Image.open(fname)
    im_inverted = im.point(lambda _: 255-_)
    im_inverted.save(fname.replace('.', '_inverted.'))
    return im_inverted


if __name__ == '__main__':
    invert_color('ICONS/win_set.png')
