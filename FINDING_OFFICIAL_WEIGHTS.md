# FINDING OFFICIAL CubiCasa5K WEIGHTS

## Why We Need Official Weights

The previously downloaded model (`JessiP23/cubicasa-5k-2` from HuggingFace) is:
- **Detectron2-based** for object detection
- **ResNet50+FPN+RPN** architecture (incompatible)
- **NOT semantic segmentation**
- **REJECTED in strict mode**

We require official CubiCasa5K weights for:
- **U-Net** architecture (semantic segmentation)
- **4-class output** (background, wall, door, window)
- **Floor-plan trained** (architecture drawings)
- **Compatible** with our implementation

---

## Sources for Official Weights

### 1. Official CubiCasa5K GitHub Repository
**URL:** https://github.com/CubiCasa/CubiCasa5k

**Repository Contents:**
- Official dataset (5,000+ floor-plan images)
- Semantic segmentation training code
- Trained model checkpoints
- Baseline benchmarks

**To find weights:**
1. Visit https://github.com/CubiCasa/CubiCasa5k
2. Look for:
   - `releases/` section (may contain checkpoints)
   - `weights/` or `checkpoints/` directory
   - Google Drive links in README
   - Training documentation

### 2. Look for Google Drive Links
The official repository often provides Google Drive links to:
- Pre-trained models
- Training checkpoints
- Dataset downloads

**Search for:**
```
drive.google.com
model_best
semantic
checkpoint
```

### 3. CubiCasa5K Paper References
The CubiCasa5K paper may include:
- Model availability statements
- Links to supplementary materials
- Weight repository information
- Author contacts for model access

---

## Expected Weight File Properties

When you find the official weights, verify:

✓ **Format**: PyTorch `.pth` or `.pkl` file
✓ **Architecture**: U-Net semantic segmentation
✓ **Classes**: 4 (background, wall, door, window)
✓ **Dataset**: Trained on CubiCasa5K
✓ **Input**: 256×256 floor-plan images
✓ **Task**: Semantic segmentation (NOT object detection)

---

## Installation Instructions

Once you obtain official CubiCasa5K weights:

### Step 1: Download Weights
Download the weights file (likely 50-150 MB)

### Step 2: Place in Correct Location
```
C:\Users\Avani\Desktop\Skematix\
  ├── pretrained_models/
  │   └── cubicasa5k_unet_semantic.pkl  ← Place file here
  ├── semantic_segmentation_inference.py
  └── verify_official_cubicasa5k.py
```

### Step 3: Verify Installation
```bash
python verify_official_cubicasa5k.py
```

Expected output:
```
✓ Official CubiCasa5K weights found
✓ Model initialized with compatible weights
[SUCCESS] Inference completed
```

---

## If You Cannot Find Official Weights

If the CubiCasa5K GitHub repository doesn't provide downloadable weights:

### Option 1: Contact Authors
- Visit https://github.com/CubiCasa/CubiCasa5k
- Submit issue requesting model weights
- Check repository issues for similar requests

### Option 2: Check Academic Resources
- Search: "CubiCasa5K pretrained model"
- Check: PapersWithCode, ModelZoo, etc.
- Look for community-shared weights

### Option 3: Alternative Approach
If official weights cannot be obtained:
- Review whether the task requires pre-trained weights
- Consider training a U-Net on CubiCasa5K dataset
- Use dataset from: https://github.com/CubiCasa/CubiCasa5k

---

## Verification Process

Once weights are in place, run:

```bash
python verify_official_cubicasa5k.py
```

This will:
1. [PART 0] Confirm Detectron2 model is rejected
2. [PART 1] Verify U-Net + CubiCasa5K selection
3. [PART 2] Check weights exist at correct location
4. [PART 3] Initialize model with weights
5. [PART 4] Report model configuration
6. [PART 5] Run inference on travertin.jpg
7. [PART 6] Report pixel classification results

Expected final output:
```
[SUCCESS] Inference completed
Pixel Classification Analysis:
  Wall: XXX pixels (XX%)
  Background: YYY pixels (YY%)
  Door: ZZZ pixels (ZZ%)
  Window: WWW pixels (WW%)

VERIFICATION COMPLETE - MODEL READY FOR PRODUCTION
```

---

## Code Changes Made (STRICT MODE)

### Modified Files:
1. **semantic_segmentation_inference.py**
   - `_download_pretrained_weights()`: Now rejects HuggingFace Detectron2 model
   - `_load_model()`: Requires compatible weights, STOPS without them
   - Error messages: Clear indication of what's needed

2. **verify_official_cubicasa5k.py** (NEW)
   - 6-part verification process
   - Explicit cleanup of incompatible model
   - Strict mode enforcement

### Enforcement Rules:
- ✗ NO random initialization
- ✗ NO silent fallbacks
- ✗ NO Detectron2 models
- ✓ STRICT error reporting
- ✓ EXPLICIT weight requirements

---

## Questions to Answer

Before proceeding, ask yourself:

1. **Have you visited** https://github.com/CubiCasa/CubiCasa5k?
2. **Did you find** official weight downloads?
3. **Is the model** U-Net-based (not Detectron2)?
4. **Is it trained on** CubiCasa5K (floor plans)?
5. **Do you have access** to the weight file?

If all answers are YES, proceed with installation.
If any are NO, investigate further before continuing.
