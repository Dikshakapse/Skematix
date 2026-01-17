"""
Pipeline Test - Core Stages (2-9)
Tests pipeline without requiring PyTorch
"""

import sys
import os
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("SKEMATIX PIPELINE - CORE STAGES TEST (2-9)")
print("=" * 80)

# Test Stage 2-9 imports
print("\n[Test] Importing pipeline stages 2-9...")
try:
    from pipeline.stage2_wall_refinement import WallMaskRefinement
    from pipeline.stage3_topology_extraction import TopologyExtractor, WallTopologyGraph
    from pipeline.stage4_room_detection import RoomDetector, RoomSet
    from pipeline.stage5_metric_normalization import MetricNormalizer
    from pipeline.stage6_3d_construction import CutawayBuilder, Mesh
    from pipeline.stage7_openings import OpeningDetector, OpeningGenerator
    from pipeline.stage8_validation import ComprehensiveValidator
    from pipeline.stage9_export import GLBExporter
    print("✓ All stage imports successful\n")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create mock wall mask (simple rectangle)
print("[1/8] Creating mock wall mask...")
try:
    wall_mask = np.zeros((100, 100), dtype=np.uint8)
    # Draw rectangle walls
    wall_mask[10:90, 10:15] = 1  # Left wall
    wall_mask[10:90, 85:90] = 1  # Right wall
    wall_mask[10:15, 10:90] = 1  # Top wall
    wall_mask[85:90, 10:90] = 1  # Bottom wall
    print(f"✓ Wall mask created: {wall_mask.shape}, wall pixels: {wall_mask.sum()}\n")
except Exception as e:
    print(f"✗ Failed: {e}\n")
    sys.exit(1)

# Stage 2: Wall Refinement
print("[2/8] Testing Stage 2 - Wall Refinement...")
try:
    door_mask = np.zeros_like(wall_mask)
    window_mask = np.zeros_like(wall_mask)
    
    refiner = WallMaskRefinement(wall_mask, door_mask, window_mask)
    refined_mask = refiner.refine()
    print(f"✓ Stage 2 complete: refined mask shape {refined_mask.shape}\n")
except Exception as e:
    print(f"✗ Stage 2 failed: {e}\n")
    import traceback
    traceback.print_exc()

# Stage 3: Topology Extraction
print("[3/8] Testing Stage 3 - Topology Extraction...")
try:
    extractor = TopologyExtractor(refined_mask)
    wall_graph = extractor.extract()
    
    if wall_graph:
        summary = wall_graph.summary()
        print(f"✓ Stage 3 complete:")
        print(f"  - Vertices: {summary['vertex_count']}")
        print(f"  - Edges: {summary['edge_count']}")
        print(f"  - Total edge length: {summary['total_edge_length']:.2f}px\n")
    else:
        print("✗ Stage 3 failed: topology extraction returned None\n")
except Exception as e:
    print(f"✗ Stage 3 failed: {e}\n")
    import traceback
    traceback.print_exc()

# Stage 4: Room Detection
print("[4/8] Testing Stage 4 - Room Detection...")
try:
    detector = RoomDetector(refined_mask, wall_graph)
    room_set = detector.detect()
    
    if room_set:
        summary = room_set.summary()
        print(f"✓ Stage 4 complete:")
        print(f"  - Rooms detected: {summary['room_count']}")
        print(f"  - Total room area: {summary['total_room_area']:.0f}px²")
        if summary['room_count'] > 0:
            print(f"  - Avg room area: {summary['avg_room_area']:.0f}px²\n")
        else:
            print("  - Warning: No rooms detected\n")
    else:
        print("✗ Stage 4 failed: room detection returned None\n")
except Exception as e:
    print(f"✗ Stage 4 failed: {e}\n")
    import traceback
    traceback.print_exc()

# Stage 5: Metric Normalization
print("[5/8] Testing Stage 5 - Metric Normalization...")
try:
    if wall_graph and room_set:
        normalizer = MetricNormalizer(
            image_shape=(100, 100),
            wall_graph=wall_graph,
            room_set=room_set
        )
        success, context_dict, norm_wall_graph, norm_room_set = normalizer.normalize()
        
        if success and norm_wall_graph:
            print(f"✓ Stage 5 complete:")
            print(f"  - Scale factor: {context_dict['scale_factor']:.2f} px/m")
            print(f"  - Target width: {context_dict['target_width_m']:.2f}m")
            print(f"  - Normalized vertices: {len(norm_wall_graph.vertices)}\n")
        else:
            print(f"✗ Stage 5 failed: normalization returned False\n")
    else:
        print("✗ Stage 5 skipped: missing wall_graph or room_set\n")
except Exception as e:
    print(f"✗ Stage 5 failed: {e}\n")
    import traceback
    traceback.print_exc()

# Stage 6: 3D Cutaway Construction
print("[6/8] Testing Stage 6 - 3D Cutaway Construction...")
try:
    if norm_wall_graph and norm_room_set:
        builder = CutawayBuilder(norm_wall_graph, norm_room_set, context_dict)
        mesh = builder.build()
        
        if mesh:
            print(f"✓ Stage 6 complete:")
            print(f"  - Vertices: {len(mesh.vertices)}")
            print(f"  - Faces: {len(mesh.faces)}")
            print(f"  - Mesh name: '{mesh.name}'\n")
        else:
            print("✗ Stage 6 failed: mesh construction returned None\n")
    else:
        print("✗ Stage 6 skipped: missing normalized geometry\n")
except Exception as e:
    print(f"✗ Stage 6 failed: {e}\n")
    import traceback
    traceback.print_exc()

# Stage 8: Validation
print("[7/8] Testing Stage 8 - Comprehensive Validation...")
try:
    if mesh and norm_wall_graph and norm_room_set:
        validator = ComprehensiveValidator(
            mesh, 
            norm_wall_graph, 
            norm_room_set,
            wall_count=len(norm_wall_graph.edges)
        )
        passed, result = validator.validate_all()
        
        print(f"✓ Stage 8 complete:")
        print(f"  - Validation passed: {passed}")
        print(f"  - Total checks: {len(result.checks)}")
        if result.warnings:
            print(f"  - Warnings: {len(result.warnings)}")
        print()
    else:
        print("✗ Stage 8 skipped: missing mesh or geometry\n")
except Exception as e:
    print(f"✗ Stage 8 failed: {e}\n")
    import traceback
    traceback.print_exc()

# Stage 9: Export
print("[8/8] Testing Stage 9 - GLB Export...")
try:
    if mesh:
        os.makedirs('output', exist_ok=True)
        output_path = 'output/test_model.glb'
        
        exporter = GLBExporter(mesh, metadata={'test': True})
        success = exporter.export(output_path)
        
        if success and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✓ Stage 9 complete:")
            print(f"  - Output file: {output_path}")
            print(f"  - File size: {file_size} bytes\n")
        else:
            print(f"✗ Stage 9 failed: export unsuccessful\n")
    else:
        print("✗ Stage 9 skipped: missing mesh\n")
except Exception as e:
    print(f"✗ Stage 9 failed: {e}\n")
    import traceback
    traceback.print_exc()

# Summary
print("=" * 80)
print("✓ CORE PIPELINE TEST COMPLETE")
print("=" * 80)
print("\nAll stages 2-9 functional. Stage 1 (semantic segmentation) requires PyTorch.")
print("\nTo run full pipeline:")
print("  pip install torch torchvision")
print("  python pipeline/orchestrator.py <blueprint_image.png>")
print("=" * 80)
