#!/usr/bin/env python3
"""
Quick reference script for text artifact removal
Demonstrates how to use the remove_text_artifacts module
"""

from pathlib import Path
from remove_text_artifacts import remove_text_artifacts


def clean_single_mask(mask_path, output_dir="output_clean"):
    """
    Clean a single wall mask and save results
    
    Args:
        mask_path (str or Path): Path to binary wall mask PNG
        output_dir (str): Directory for output files
    
    Returns:
        bool: Success status
    """
    mask_path = Path(mask_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate output paths
    image_stem = mask_path.stem.replace("_walls_mask", "")
    clean_mask = output_dir / f"{image_stem}_walls_mask_clean.png"
    clean_overlay = output_dir / f"{image_stem}_walls_overlay_clean.png"
    
    # Run cleanup
    return remove_text_artifacts(
        str(mask_path),
        str(clean_mask),
        str(clean_overlay)
    )


def clean_all_masks_in_folder(folder_path):
    """
    Clean all wall masks in a directory
    
    Args:
        folder_path (str or Path): Directory containing *_walls_mask.png files
    """
    folder = Path(folder_path)
    mask_files = sorted(folder.glob("*_walls_mask.png"))
    
    print(f"\nFound {len(mask_files)} mask(s) in {folder}")
    print()
    
    for idx, mask_file in enumerate(mask_files, 1):
        print(f"[{idx}/{len(mask_files)}] Processing {mask_file.name}")
        
        output_folder = mask_file.parent
        image_stem = mask_file.stem.replace("_walls_mask", "")
        
        clean_mask = output_folder / f"{image_stem}_walls_mask_clean.png"
        clean_overlay = output_folder / f"{image_stem}_walls_overlay_clean.png"
        
        success = remove_text_artifacts(
            str(mask_file),
            str(clean_mask),
            str(clean_overlay)
        )
        
        if success:
            print(f"   ✓ Saved: {clean_mask.name}")
            print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("TEXT ARTIFACT REMOVAL - QUICK REFERENCE")
        print()
        print("Usage:")
        print("  python text_cleanup_quick.py <mask_path> [output_dir]")
        print("  python text_cleanup_quick.py --folder <folder_path>")
        print()
        print("Examples:")
        print("  # Clean single mask:")
        print("  python text_cleanup_quick.py image1_walls_mask.png")
        print()
        print("  # Clean all masks in a folder:")
        print("  python text_cleanup_quick.py --folder input/")
        print()
        print("Output:")
        print("  • <image>_walls_mask_clean.png")
        print("  • <image>_walls_overlay_clean.png")
        sys.exit(0)
    
    if sys.argv[1] == "--folder" and len(sys.argv) > 2:
        # Batch folder processing
        clean_all_masks_in_folder(sys.argv[2])
    else:
        # Single file processing
        mask_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        
        if output_dir:
            clean_single_mask(mask_path, output_dir)
        else:
            clean_single_mask(mask_path)
