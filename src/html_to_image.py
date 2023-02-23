"""
HTML 2 Image
@author : Ashutosh | created on : 23-12-2022
"""
import os
import random

from html2image import Html2Image


def make_gradient_image(store_dir, gradient_name, colors):
    """
    Make gradients
    :param gradient_name:
    :param store_dir:
    :param colors:
    :return:
    """
    if colors is None:
        colors = list()
        for _ in range(3):
            colors.append((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255), 1))

    hti = Html2Image(output_path=store_dir)
    degree = random.randint(45, 360)

    grad_strings = [
        f"{degree}deg,  rgba{colors[0]} 11.2%, rgba{colors[1]} 57.8%, rgba{colors[2]} 85.9%",
        f"{degree}deg,  rgba{colors[0]} 11.2%, rgba{colors[1]} 57.8%",
        f"{degree}deg,  rgba{colors[0]} 11.2%, rgba{colors[1]} 57.8%, rgba{colors[2]} 11.9%"
    ]
    grad_strings = random.choice(grad_strings)

    html = f"""<!DOCTYPE html>
    <html>
    <head>
    <style>
    #grad1 {{
       height: 1080px; width: 1920px;
      background-image: linear-gradient({grad_strings});
    }}
    </style>
    </head>
    <body>
    <div id="grad1"></div>

    </body>
    </html>
    """

    # html = f"""
    # <!DOCTYPE html>
    # <html>
    # <head>
    # <style>
    # #grad1 {{
    #    height: 1080px; width: 1920px;
    #   background-image: linear-gradient({grad_strings});
    # }}
    # </style>
    # </head>
    # <body>
    # <div id="grad1"></div>
    #
    # </body>
    # </html>
    # """

    hti.screenshot(html_str=html, save_as=gradient_name)

    return os.path.join(store_dir, gradient_name), colors
