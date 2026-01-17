"""
SEMANTIC SEGMENTATION INFERENCE - INSTALLATION & USAGE GUIDE
=============================================================

This module performs semantic segmentation on 2D floor plan images using
a pretrained DeepLabV3+ ResNet50 model (COCO dataset).

OUTPUT: Binary wall mask images (walls_mask.png)
"""

# ============================================================================
# INSTALLATION
# ============================================================================

# Step 1: Install required packages
# ===================================

# Option A: Using pip (recommended)
pip install torch torchvision opencv-python numpy pillow

# Option B: Specific versions for CPU (lightweight)
pip install torch==2.0.0 torchvision==0.15.0 --index-url https://download.pytorch.org/whl/cpu
pip install opencv-python==4.8.0.76 numpy==1.26.4 pillow==10.0.0

# Option C: With CUDA support (GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install opencv-python numpy pillow

# ============================================================================
# QUICK START
# ============================================================================

# 1. Place floor plan images in 'input/' folder
#    Example: input/blueprint.png

# 2. Run segmentation
python semantic_segmentation_inference.py input/blueprint.png

# 3. Check output
#    - output/blueprint_walls_mask.png (binary mask)
#    - output/blueprint_walls_overlay.png (visualization)

# ============================================================================
# PYTHON API
# ============================================================================

from semantic_segmentation_inference import FloorPlanSegmenter
import cv2
import numpy as np

# Initialize segmenter
segmenter = FloorPlanSegmenter(device='cpu')

# Segment image
wall_mask = segmenter.segment(
    image_path='input/blueprint.png',
    output_path='output/blueprint_walls_mask.png'
)

# wall_mask is numpy array [H, W], uint8:
#   255 = wall/structure detected
#   0 = background/empty space

# You can process the mask further
wall_pixels = np.sum(wall_mask > 128)
total_pixels = wall_mask.size
wall_coverage = 100.0 * wall_pixels / total_pixels
print(f"Wall coverage: {wall_coverage:.1f}%")

# ============================================================================
# TEST SCRIPT
# ============================================================================

# Run comprehensive test with visualization
python test_semantic_segmentation.py

# This will:
# 1. Load all images from 'input/' folder
# 2. Generate wall masks
# 3. Create overlay visualizations
# 4. Save to 'output/' folder

# ============================================================================
# OUTPUT FORMATS
# ============================================================================

# Output file: walls_mask.png
# ├─ Format: PNG (8-bit grayscale)
# ├─ Value 255: Wall/structure detected
# ├─ Value 0: Background/empty space
# └─ Size: Same as input image

# Output file: walls_overlay.png
# ├─ Format: PNG (color RGB)
# ├─ Red regions: Detected walls
# ├─ Green contours: Wall boundaries
# └─ Original image: 60% opacity blend

# ============================================================================
# CONFIGURATION
# ============================================================================

# Input size (default 512x512, can be adjusted):
segmenter = FloorPlanSegmenter(device='cpu', input_size=512)

# Device selection:
#   device='cpu'   → CPU inference (slower, works everywhere)
#   device='cuda'  → GPU inference (requires NVIDIA GPU with CUDA)

# ============================================================================
# DETAILS
# ============================================================================

# Model: DeepLabV3+ with ResNet50 encoder
# Training data: COCO dataset (80 object classes)
# Input resolution: 512x512 (internally resized)
# Output: Per-pixel classification
# Post-processing: Percentile thresholding (top 30% confidence as walls)

# Architecture flow:
# Input image → Resize to 512x512 → Normalize (ImageNet stats)
#   → DeepLabV3+ encoder-decoder → Class probabilities [21 classes]
#   → Extract structural confidence → Threshold to binary
#   → Resize to original resolution → Output mask

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# Problem: ModuleNotFoundError: No module named 'torch'
# Solution: Install PyTorch → pip install torch torchvision

# Problem: CUDA out of memory
# Solution: Use CPU instead → segmenter = FloorPlanSegmenter(device='cpu')

# Problem: Poor wall detection quality
# Solution: Fine-tuning may be needed (beyond scope of inference-only module)
#           Current: Pretrained COCO model adapted to floor plans
#           Note: Better results with floor-plan-specific training data

# Problem: Slow on CPU
# Solution: Use GPU (requires CUDA-compatible NVIDIA GPU)
#           Or reduce input_size → FloorPlanSegmenter(input_size=256)

# ============================================================================
# NOTES
# ============================================================================

# 1. This is INFERENCE ONLY - no model training
# 2. Uses publicly available DeepLabV3+ pretrained on COCO
# 3. Adapted for floor plan wall detection via post-processing
# 4. CPU compatible, but GPU recommended for speed
# 5. Single file with no external dependencies beyond PyTorch

# ============================================================================
