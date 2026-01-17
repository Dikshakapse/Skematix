#!/usr/bin/env python3
"""
Batch Semantic Segmentation Evaluation
Processes multiple floor-plan images using CubiCasa5K model.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))

from cubicasa5k_segmenter import CubiCasa5KSegmenter


def evaluate_batch():
    """Evaluate segmentation on all images in test_floorplans folder"""
    
    print("=" * 80)
    print("BATCH SEMANTIC SEGMENTATION EVALUATION")
    print("=" * 80)
    print()
    
    # Initialize model
    try:
        models_dir = Path(__file__).parent / "pretrained_models"
        model_path = models_dir / "model_best_val_loss_var.pkl"
        segmenter = CubiCasa5KSegmenter(model_path=model_path)
    except Exception as e:
        print(f"\n[FATAL] Model initialization failed: {e}")
        print("\nTo proceed:")
        print("1. Download: https://drive.google.com/file/d/1gRB7ez1e4H7a9Y09lLqRuna0luZO5VRK/view?usp=sharing")
        print("2. Place at: pretrained_models/model_best_val_loss_var.pkl")
        print("3. Re-run this script")
        return
    
    print()
    print("[EVALUATION] Processing images from test_floorplans/")
    print("-" * 80)
    print()
    
    # Find all images
    test_folder = Path(__file__).parent / "test_floorplans"
    if not test_folder.exists():
        print(f"ERROR: Folder not found: {test_folder}")
        return
    
    # Get all image files
    image_files = sorted([f for f in test_folder.glob("*") if f.suffix.lower() in [".png", ".jpg", ".jpeg"]])
    
    if not image_files:
        print(f"No images found in {test_folder}")
        return
    
    print(f"Found {len(image_files)} image(s)")
    print()
    
    # Process each image
    results = []
    for idx, image_path in enumerate(image_files, 1):
        print(f"[{idx}/{len(image_files)}] Processing: {image_path.name}")
        
        try:
            # Run segmentation
            wall_mask, class_mask = segmenter.segment(str(image_path))
            
            # Calculate statistics
            total_pixels = class_mask.size
            wall_pixels = np.sum(class_mask == 1)
            wall_percentage = (wall_pixels / total_pixels) * 100 if total_pixels > 0 else 0
            
            # Get output folder (from the segment method, find latest)
            output_base = Path(__file__).parent / "output"
            output_dirs = sorted([d for d in output_base.glob(f"{image_path.stem}_*")], 
                               key=lambda x: x.name)
            output_folder = output_dirs[-1] if output_dirs else None
            
            # Store results
            results.append({
                'image': image_path.name,
                'wall_pct': wall_percentage,
                'total_pixels': total_pixels,
                'wall_pixels': wall_pixels,
                'output_folder': output_folder,
                'status': 'SUCCESS'
            })
            
            print(f"   ✓ Wall pixels: {wall_pixels:,} ({wall_percentage:.2f}%)")
            print(f"   ✓ Output: {output_folder.name if output_folder else 'N/A'}")
            print()
            
        except Exception as e:
            print(f"   ✗ ERROR: {e}")
            results.append({
                'image': image_path.name,
                'status': 'FAILED',
                'error': str(e)
            })
            print()
    
    # Print summary
    print("=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    print()
    
    successful = [r for r in results if r['status'] == 'SUCCESS']
    failed = [r for r in results if r['status'] == 'FAILED']
    
    print(f"Total images: {len(results)}")
    print(f"Successful:   {len(successful)}")
    print(f"Failed:       {len(failed)}")
    print()
    
    if successful:
        print("Results:")
        print("-" * 80)
        print(f"{'Image':<20} {'Wall %':<12} {'Pixels':<15} {'Output Folder':<30}")
        print("-" * 80)
        for r in successful:
            folder_name = r['output_folder'].name if r['output_folder'] else "N/A"
            print(f"{r['image']:<20} {r['wall_pct']:>10.2f}% {r['wall_pixels']:>14,} {folder_name:<30}")
        print()
    
    if failed:
        print("Failed images:")
        print("-" * 80)
        for r in failed:
            print(f"{r['image']:<20} ERROR: {r.get('error', 'Unknown')}")
        print()
    
    print("=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    evaluate_batch()
