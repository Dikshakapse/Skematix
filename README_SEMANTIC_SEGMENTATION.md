# SEMANTIC SEGMENTATION INFERENCE FOR FLOOR PLANS

Semantic segmentation module for 2D floor plan wall detection using pretrained PyTorch DeepLabV3+.

## Quick Overview

**Input:** 2D floor plan image (PNG/JPG)  
**Output:** Binary wall mask image (`walls_mask.png`)  
**Model:** DeepLabV3+ ResNet50 (pretrained on COCO)  
**Framework:** PyTorch  
**Device:** CPU or CUDA GPU  

## Files

```
semantic_segmentation_inference.py     Main inference module (single file)
test_semantic_segmentation.py          Test script with visualization
install_dependencies.bat               Windows dependency installer
install_dependencies.sh                Linux/Mac dependency installer
SEMANTIC_SEGMENTATION_SETUP.md         Detailed setup guide
```

## Installation

### Step 1: Install Dependencies

**Windows:**
```bash
install_dependencies.bat
```

**Linux/Mac:**
```bash
bash install_dependencies.sh
```

**Manual (all platforms):**
```bash
pip install torch torchvision opencv-python numpy pillow
```

### Step 2: Verify Installation

```bash
python -c "import torch; print('PyTorch:', torch.__version__)"
```

## Usage

### Command Line

```bash
python semantic_segmentation_inference.py <input_image> [output_dir]
```

**Example:**
```bash
python semantic_segmentation_inference.py input/blueprint.png output/
```

**Output:**
- `blueprint_walls_mask.png` - Binary wall mask
- `blueprint_walls_overlay.png` - Visualization overlay

### Python API

```python
from semantic_segmentation_inference import FloorPlanSegmenter
import numpy as np

# Initialize
segmenter = FloorPlanSegmenter(device='cpu')

# Segment
wall_mask = segmenter.segment(
    image_path='input/blueprint.png',
    output_path='output/walls_mask.png'
)

# Process results
wall_coverage = 100.0 * np.sum(wall_mask > 128) / wall_mask.size
print(f"Wall coverage: {wall_coverage:.1f}%")
```

### Test Script

```bash
python test_semantic_segmentation.py
```

This automatically:
1. Finds test images in `input/` folder
2. Generates wall masks
3. Creates overlay visualizations
4. Saves all outputs to `output/` folder

## Output Formats

### walls_mask.png
- **Format:** PNG (8-bit grayscale)
- **Value 255:** Wall/structure detected
- **Value 0:** Background/empty space
- **Size:** Same as input image

### walls_overlay.png
- **Format:** PNG (color RGB)
- **Red regions:** Detected walls
- **Green contours:** Wall boundaries
- **Background:** Original image at 60% opacity

## Model Details

| Property | Value |
|----------|-------|
| **Architecture** | DeepLabV3+ with ResNet50 encoder |
| **Training Data** | COCO (80 object classes) |
| **Input Resolution** | 512×512 (auto-resized) |
| **Output Classes** | 21 (COCO) → adapted for walls |
| **Framework** | PyTorch |
| **Device Support** | CPU, CUDA GPU |

## Configuration

### Device Selection

```python
# CPU (default, slower but works everywhere)
segmenter = FloorPlanSegmenter(device='cpu')

# GPU (faster, requires NVIDIA GPU)
segmenter = FloorPlanSegmenter(device='cuda')

# Auto-detect
device = 'cuda' if torch.cuda.is_available() else 'cpu'
segmenter = FloorPlanSegmenter(device=device)
```

### Input Size

```python
# Default 512×512
segmenter = FloorPlanSegmenter(input_size=512)

# Smaller (faster)
segmenter = FloorPlanSegmenter(input_size=256)

# Larger (more detail)
segmenter = FloorPlanSegmenter(input_size=768)
```

## Performance

### CPU (Intel i7/Ryzen 5)
- First run: ~5-10 seconds (model download + inference)
- Subsequent runs: ~3-5 seconds

### GPU (NVIDIA RTX 2060)
- First run: ~2-3 seconds
- Subsequent runs: ~0.5-1 second

## Troubleshooting

### ModuleNotFoundError: No module named 'torch'
Install PyTorch:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### CUDA out of memory
Use CPU instead:
```python
segmenter = FloorPlanSegmenter(device='cpu')
```

### Slow performance on CPU
- Use GPU (if available)
- Reduce input_size: `FloorPlanSegmenter(input_size=256)`

### Poor wall detection
The current model uses COCO pretrained weights adapted for floor plans. For better results on specific floor plan types, fine-tuning with domain-specific data would be needed (beyond inference-only scope).

## Technical Notes

1. **Inference Only:** No model training or fine-tuning
2. **Pretrained:** Uses publicly available COCO-pretrained weights
3. **Post-Processing:** Adaptive thresholding (top 30% confidence as walls)
4. **Single File:** All code in one module with no external configuration
5. **CPU Compatible:** Works on any machine with Python 3.7+

## Architecture Overview

```
Input Image
    ↓
Resize to 512×512
    ↓
Normalize (ImageNet statistics)
    ↓
DeepLabV3+ Encoder-Decoder
    ↓
Per-pixel class probabilities (21 classes)
    ↓
Extract structural confidence
    ↓
Adaptive threshold (top 30%)
    ↓
Resize to original resolution
    ↓
Binary wall mask (255/0)
    ↓
Output: walls_mask.png
```

## Scope

✅ **Included:**
- Semantic segmentation inference
- Pretrained model loading
- Wall mask generation
- Visualization overlay

❌ **Not Included:**
- Model training
- Fine-tuning
- 3D generation
- Interactive annotation

## Next Steps

The semantic segmentation inference module is now ready for use. For integration with other pipeline stages, see the main project documentation.

---

**Version:** 1.0  
**Date:** January 2026  
**Status:** Ready for inference
