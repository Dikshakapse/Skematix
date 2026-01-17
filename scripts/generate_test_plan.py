"""Generate a simple synthetic floorplan image for testing the pipeline.

Creates `input/test_plan.png` with thick lines/rectangles representing walls.
"""
import cv2
import numpy as np
import os


def make_test_plan(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    W, H = 1200, 800
    img = 255 * np.ones((H, W, 3), dtype=np.uint8)

    # Draw outer walls
    thickness = 12
    cv2.rectangle(img, (50, 50), (W - 50, H - 50), (0, 0, 0), thickness)

    # Interior room dividers
    cv2.line(img, (300, 50), (300, 450), (0, 0, 0), thickness)
    cv2.line(img, (300, 450), (1100, 450), (0, 0, 0), thickness)
    cv2.line(img, (600, 50), (600, 300), (0, 0, 0), thickness)

    # Door gaps (erase small sections)
    cv2.rectangle(img, (290, 420), (330, 450), (255, 255, 255), -1)

    cv2.imwrite(path, img)
    print('Wrote test plan to', path)


if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..')
    out = os.path.normpath(os.path.join(base, 'input', 'test_plan.png'))
    make_test_plan(out)
