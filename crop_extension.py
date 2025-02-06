import os, sys
from PIL import Image 
import random

def random_crop_containing_bbox(image, bbox, crop_size=(512,512)):
    """
    Randomly crops an image such that the bounding box is fully contained within the crop.
    """
    width, height = image.size
    # Convert bbox from [x,y,w,h] to [x1,y1,x2,y2]
    x, y, w, h = bbox
    bbox_x1, bbox_y1, bbox_x2, bbox_y2 = x, y, x + w, y + h

    # Ensure the bounding box is within the image dimensions
    if (bbox_x1 < 0 or bbox_y1 < 0 or bbox_x2 > width or bbox_y2 > height):
        raise ValueError("Bounding box is out of image bounds")

    # Calculate the maximum x and y coordinates for the top-left corner of the crop
    max_x = min(bbox_x1, width - crop_size[0])
    max_y = min(bbox_y1, height - crop_size[1])

    # Ensure the crop size does not exceed image dimensions
    if max_x <= 0 or max_y <= 0:
        raise ValueError("Crop size is larger than image dimensions")

    # Randomly select a top-left corner for the crop
    x = random.randint(0, max_x)
    y = random.randint(0, max_y)

    # Adjust the crop to ensure it contains the bounding box
    x = max(x, bbox_x1)
    y = max(y, bbox_y1)

    # Ensure the crop does not exceed image dimensions
    if x + crop_size[0] > width:
        x = width - crop_size[0]
    if y + crop_size[1] > height:
        y = height - crop_size[1]

    # Crop the image
    cropped_image = image.crop((x, y, x + crop_size[0], y + crop_size[1]))

    return cropped_image


def crop_to_grid(image, tile_size=(512, 512)):
    """
    Crops an image into a grid of specified size. 
    Zero-pad the image if necessary to make it divisible by the grid size.
    """
    width, height = image.size
    tile_width, tile_height = tile_size

    # Calculate the number of crops needed in each dimension
    num_crops_x = (width + tile_width - 1) // tile_width
    num_crops_y = (height + tile_height - 1) // tile_height

    # Create a list to store the cropped images
    crops = []

    # Crop the image into a grid
    for i in range(num_crops_x):
        for j in range(num_crops_y):
            left = i * tile_width
            upper = j * tile_height
            right = min(left + tile_width, width)
            lower = min(upper + tile_height, height)

            # Crop the image
            crop = image.crop((left, upper, right, lower))

            # If the crop is smaller than the grid size, pad it with zeros
            if crop.size != (tile_width, tile_height):
                padded_crop = Image.new("RGB", (tile_width, tile_height))
                padded_crop.paste(crop, (0, 0))
                crops.append(padded_crop)
            else:
                crops.append(crop)

    return crops


def crop_to_grid_with_offset(image, tile_size=(512, 512), offset=(256, 256)):
    """
    Crops an image into a grid of specified size with an offset. 
    Pass for the remaining pixels if the image is not divisible by the grid size.
    """
    width, height = image.size
    tile_width, tile_height = tile_size
    offset_x, offset_y = offset

    # Calculate the number of crops needed in each dimension
    num_crops_x = (width - offset_x - 1) // tile_width
    num_crops_y = (height- offset_y- 1) // tile_height

    # Create a list to store the cropped images
    crops = []
    # Crop the image into a grid
    for i in range(num_crops_x):
        for j in range(num_crops_y):
            left = i * tile_width
            upper = j * tile_height
            right = min(left + tile_width, width)
            lower = min(upper + tile_height, height)

            # Crop the image
            crop = image.crop((left, upper, right, lower))
            crops.append(crop)
    return crops



