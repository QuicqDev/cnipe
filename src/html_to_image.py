"""
HTML 2 Image
@author : Ashutosh | created on : 23-12-2022
"""
import os
from html2image import Html2Image


def make_gradient_image(store_dir, gradient_name):
    """
    Make gradients
    :param gradient_name:
    :param store_dir:
    :return:
    """
    hti = Html2Image(output_path=store_dir)

    html = """<!DOCTYPE html>
    <html>
    <head>
    <style> 
    #grad1 {
       height: 1080px; width: 1920px;
      background-image: linear-gradient( 189.6deg,  rgba(247,253,166,1) 11.2%, rgba(128,255,221,1) 57.8%, rgba(255,128,249,1) 85.9% );
    }
    </style>
    </head>
    <body>
    <div id="grad1"></div>
    
    </body>
    </html>
    """

    hti.screenshot(html_str=html, save_as=gradient_name)

    return os.path.join(store_dir, gradient_name)
