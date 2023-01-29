"""
class image modifier for Gnapper
"""
from PIL import Image, ImageDraw

class ImgModifier:
    """
    Class for modifying images.

    Attributes
    ----------
    outer_img : img
    inner_img : img
    padding : int

    Methods
    -------
    paste_img()
        inner_image on top of outer_image
    add_corners()
        adds corner to the image

    """
    def __init__(self, outer_img, inner_img, padding):
        self.outer_img = outer_img
        self.inner_img = inner_img
        self.padding =  padding

    def paste_img(self, rounded_corners=False):
        """

        Parameters
        ----------
        outer_img : img
            background image.
        inner_img : img
            foreground img.
        padding : int
            thickness of border
        rounded_corners: bool
            If TRUE, inner image will have curved corners.

        Returns
        -------
        img
             inner_image on top of outer_image
        """
        if rounded_corners and isinstance(rounded_corners, int):
            self.inner_img = self.add_corners(self.inner_img, rounded_corners)
        inner_img_w, inner_img_h = self.inner_img.size
        outer_img = self.outer_img.resize(
            (inner_img_w + (self.padding*2), inner_img_h + (self.padding*2))
            )
        outer_img.paste(self.inner_img, (self.padding, self.padding), self.inner_img)
        return outer_img


    @staticmethod
    def add_corners(image_old, rad):
        """
        add corners to image
        """
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new('L', image_old.size, 255)
        image_width_old, image_height_old = image_old.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, image_height_old - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (image_width_old - rad, 0))
        alpha.paste(
            circle.crop((
                rad, rad, rad * 2, rad * 2)),
                (image_width_old - rad, image_height_old - rad)
                )
        image_old.putalpha(alpha)
        return image_old
