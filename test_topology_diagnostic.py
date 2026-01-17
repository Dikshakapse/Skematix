"""
Diagnostic: Check topology extraction with visualization
"""

import numpy as np
import cv2
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

# Create test floor plan
h, w = 300, 400
wall_mask = np.zeros((h, w), dtype=np.uint8)

# Outer walls
wall_thickness = 20
wall_mask[0:wall_thickness, :] = 1
wall_mask[h-wall_thickness:h, :] = 1
wall_mask[:, 0:wall_thickness] = 1
wall_mask[:, w-wall_thickness:w] = 1

# Internal walls
wall_mask[wall_thickness:h-wall_thickness, 150:170] = 1
wall_mask[140:160, wall_thickness:150] = 1

print(f"Wall mask: {wall_mask.shape}, pixel sum: {wall_mask.sum()}")
print(f"Wall pixels range: {wall_mask.min()}-{wall_mask.max()}")

# Test skeletonization
print("\n[Test] Skeletonization...")
skeleton = cv2.ximgproc.thinning((wall_mask * 255).astype(np.uint8))
print(f"Skeleton shape: {skeleton.shape}")
print(f"Skeleton pixels: {skeleton.sum()}")
print(f"Skeleton range: {skeleton.min()}-{skeleton.max()}")

# Find key points
if skeleton.sum() > 0:
    skeleton_points = np.argwhere(skeleton > 0)
    print(f"Skeleton points found: {len(skeleton_points)}")
    
    # Analyze connectivity
    for y, x in skeleton_points[:10]:  # First 10 points
        neighborhood = skeleton[max(0, y-1):y+2, max(0, x-1):x+2]
        neighbor_count = neighborhood.sum() - 1
        print(f"  Point ({x}, {y}): {neighbor_count} neighbors")
else:
    print("✗ No skeleton pixels found!")

# Now test with the actual stage
print("\n[Test] Full topology extraction...")
from pipeline.stage3_topology_extraction import TopologyExtractor

# Convert wall_mask to proper format
wall_mask_8bit = (wall_mask * 255).astype(np.uint8)

extractor = TopologyExtractor(wall_mask_8bit)
try:
    graph = extractor.extract()
    if graph:
        summary = graph.summary()
        print(f"✓ Topology extracted:")
        print(f"  - Vertices: {summary['vertex_count']}")
        print(f"  - Edges: {summary['edge_count']}")
    else:
        print("✗ Topology extraction returned None")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
