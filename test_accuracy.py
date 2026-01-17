import time
import os
from backend.image_processing import process_image

images = ['input/images (1).png', 'input/images.png', 'input/test_plan.png']
results = []

for img in images:
    if os.path.exists(img):
        start = time.time()
        walls = process_image(img, None, debug=False)
        end = time.time()
        results.append((img, len(walls), end - start))
        print(f'{img}: {len(walls)} walls, {end-start:.2f}s')
    else:
        print(f'{img}: not found')

print('\nSummary:')
for img, walls, time_taken in results:
    print(f'{img}: {walls} walls, {time_taken:.2f}s')
