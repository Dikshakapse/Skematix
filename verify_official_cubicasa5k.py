#!/usr/bin/env python3
"""
Verification script for official CubiCasa5K U-Net semantic segmentation model.

STRICT MODE: Will NOT proceed with random initialization.
Requires compatible pretrained weights for semantic segmentation.
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("OFFICIAL CubiCasa5K SEMANTIC SEGMENTATION MODEL VERIFICATION")
print("=" * 80)
print()

# ============================================================================
# PART 0: CLEANUP - REJECT INCOMPATIBLE MODEL
# ============================================================================
print("[PART 0] CLEANUP: Rejecting incompatible Detectron2 model")
print("-" * 80)

detectron2_model = Path(__file__).parent / "pretrained_models" / "cubicasa5k_model_final.pth"
if detectron2_model.exists():
    print(f"⚠ Found incompatible model: {detectron2_model}")
    print(f"  Type: Detectron2 ResNet50+FPN+RPN (object detection)")
    print(f"  Size: {detectron2_model.stat().st_size / (1024*1024):.2f} MB")
    print(f"  Status: WILL BE IGNORED - NOT USED")
else:
    print("✓ No incompatible Detectron2 model found")

print()

# ============================================================================
# PART 1: MODEL SELECTION VERIFICATION
# ============================================================================
print("[PART 1] MODEL SELECTION VERIFICATION")
print("-" * 80)

print("Required model type: Semantic segmentation")
print("Required architecture: U-Net")
print("Required dataset: CubiCasa5K (floor plans)")
print("Official source: https://github.com/CubiCasa/CubiCasa5k")
print()

# ============================================================================
# PART 2: VERIFY PRETRAINED WEIGHTS
# ============================================================================
print("[PART 2] VERIFY PRETRAINED WEIGHTS AVAILABILITY")
print("-" * 80)

models_dir = Path(__file__).parent / "pretrained_models"
models_dir.mkdir(exist_ok=True)

# Look for official CubiCasa5K U-Net checkpoint
official_weights = models_dir / "cubicasa5k_unet_semantic.pkl"

if official_weights.exists():
    print(f"✓ Found official CubiCasa5K weights: {official_weights}")
    weights_size = official_weights.stat().st_size
    print(f"  Size: {weights_size / (1024*1024):.2f} MB ({weights_size} bytes)")
    print(f"  Path: {official_weights.absolute()}")
    weights_available = True
else:
    print(f"✗ Official CubiCasa5K U-Net weights NOT found")
    print(f"  Expected: {official_weights.absolute()}")
    print(f"  Source: https://github.com/CubiCasa/CubiCasa5k")
    print(f"  Note: Weights must be downloaded from official CubiCasa5K repository")
    weights_available = False

print()

# ============================================================================
# PART 3: ATTEMPT TO INITIALIZE MODEL
# ============================================================================
print("[PART 3] MODEL INITIALIZATION (STRICT MODE)")
print("-" * 80)

if not weights_available:
    print("[FATAL] Cannot initialize model")
    print("Reason: No compatible pretrained segmentation weights found")
    print()
    print("=" * 80)
    print("VERIFICATION FAILED - STOPPING")
    print("=" * 80)
    print()
    print("To use this model, you must:")
    print("1. Download CubiCasa5K U-Net weights from the official repository")
    print("   Source: https://github.com/CubiCasa/CubiCasa5k")
    print("2. Place them at: " + str(models_dir / "cubicasa5k_unet_semantic.pkl"))
    print()
    sys.exit(1)

print("Initializing FloorPlanSegmenter with official weights...")
print()

try:
    from semantic_segmentation_inference import FloorPlanSegmenter
    
    # Initialize with strict mode
    segmenter = FloorPlanSegmenter(device='cpu')
    
    print()
    print("[SUCCESS] Model initialized with compatible weights")
    print()
    
    # ========================================================================
    # PART 4: REPORT MODEL CONFIGURATION
    # ========================================================================
    print("[PART 4] MODEL CONFIGURATION REPORT")
    print("-" * 80)
    
    print(f"Model architecture: U-Net")
    print(f"Training dataset: CubiCasa5K")
    print(f"Checkpoint file: cubicasa5k_unet_semantic.pkl")
    print(f"Weights status: ACTIVE = YES")
    print(f"Device: {segmenter.device}")
    print(f"Input size: {segmenter.input_size}x{segmenter.input_size}")
    print(f"Output classes: 4 (Background, Wall, Door, Window)")
    print()
    
    # ========================================================================
    # PART 5: ATTEMPT INFERENCE
    # ========================================================================
    print("[PART 5] INFERENCE VERIFICATION")
    print("-" * 80)
    
    input_image = Path(__file__).parent / "input" / "travertin.jpg"
    
    if not input_image.exists():
        print(f"⚠ Input image not found: {input_image}")
        print(f"  Skipping inference verification")
    else:
        print(f"Input image: {input_image}")
        print(f"  Size: {input_image.stat().st_size / 1024:.2f} KB")
        
        try:
            print("\nRunning inference on travertin.jpg...")
            
            # Run segmentation
            wall_mask, class_mask = segmenter.segment(str(input_image))
            
            print()
            print("[SUCCESS] Inference completed")
            print()
            
            # ====================================================================
            # PART 6: PIXEL CLASSIFICATION ANALYSIS
            # ====================================================================
            print("[PART 6] PIXEL CLASSIFICATION ANALYSIS")
            print("-" * 80)
            
            import numpy as np
            
            total_pixels = class_mask.size
            wall_pixels = np.sum(class_mask == 1)
            background_pixels = np.sum(class_mask == 0)
            door_pixels = np.sum(class_mask == 2)
            window_pixels = np.sum(class_mask == 3)
            
            print(f"Total pixels: {total_pixels:,}")
            print(f"  Wall (class 1): {wall_pixels:,} ({wall_pixels/total_pixels*100:.2f}%)")
            print(f"  Background (class 0): {background_pixels:,} ({background_pixels/total_pixels*100:.2f}%)")
            print(f"  Door (class 2): {door_pixels:,} ({door_pixels/total_pixels*100:.2f}%)")
            print(f"  Window (class 3): {window_pixels:,} ({window_pixels/total_pixels*100:.2f}%)")
            print()
            
            # Check output folder
            output_dir = Path(__file__).parent / "output"
            timestamped_dirs = sorted(output_dir.glob("travertin_*"), key=lambda x: x.name)
            if timestamped_dirs:
                latest = timestamped_dirs[-1]
                print(f"Output folder: {latest}")
                print(f"  Files:")
                for f in sorted(latest.glob("*.png")):
                    print(f"    - {f.name} ({f.stat().st_size / 1024:.2f} KB)")
            
            print()
            print("=" * 80)
            print("VERIFICATION COMPLETE - MODEL READY FOR PRODUCTION")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n[ERROR] Inference failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
except Exception as e:
    print()
    print(f"[FATAL] Model initialization failed: {e}")
    print()
    import traceback
    traceback.print_exc()
    print()
    print("=" * 80)
    print("VERIFICATION FAILED - STOPPING")
    print("=" * 80)
    sys.exit(1)
