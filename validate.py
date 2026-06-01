#!/usr/bin/env python
"""
System validation and testing script
This script verifies that all components are working correctly
"""

import sys
from pathlib import Path


def check_imports():
    """Check if all required modules can be imported"""
    print("\n" + "="*60)
    print("CHECKING IMPORTS")
    print("="*60)
    
    modules = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'torch': 'PyTorch',
        'ultralytics': 'Ultralytics (YOLO)',
        'scipy': 'SciPy',
        'sklearn': 'Scikit-learn',
        'PIL': 'Pillow',
        'matplotlib': 'Matplotlib',
    }
    
    all_ok = True
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"✓ {name:30s} OK")
        except ImportError as e:
            print(f"✗ {name:30s} MISSING - {e}")
            all_ok = False
    
    return all_ok


def check_project_structure():
    """Check if all required files and directories exist"""
    print("\n" + "="*60)
    print("CHECKING PROJECT STRUCTURE")
    print("="*60)
    
    required_files = [
        'main.py',
        'quick_test.py',
        'config.py',
        'requirements.txt',
        'src/__init__.py',
        'src/detector.py',
        'src/tracker.py',
        'src/utils.py',
        'src/video_processor.py',
    ]
    
    required_dirs = [
        'src',
        'models',
        'videos',
        'output',
    ]
    
    all_ok = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path:40s} OK")
        else:
            print(f"✗ {file_path:40s} MISSING")
            all_ok = False
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ {dir_path:40s} OK (directory)")
        else:
            print(f"✗ {dir_path:40s} MISSING (creating...)")
            Path(dir_path).mkdir(exist_ok=True)
            print(f"  Created: {dir_path}")
    
    return all_ok


def check_src_modules():
    """Check if all source modules can be imported"""
    print("\n" + "="*60)
    print("CHECKING SOURCE MODULES")
    print("="*60)
    
    modules = {
        'src.detector': 'YOLODetector',
        'src.tracker': 'SORTTracker',
        'src.utils': 'TrackingVisualization, VideoHandler',
        'src.video_processor': 'VideoObjectDetectionTracker',
    }
    
    all_ok = True
    for module_name, class_names in modules.items():
        try:
            module = __import__(module_name, fromlist=[''])
            print(f"✓ {module_name:40s} OK ({class_names})")
        except Exception as e:
            print(f"✗ {module_name:40s} ERROR - {e}")
            all_ok = False
    
    return all_ok


def check_torch_cuda():
    """Check if CUDA is available"""
    print("\n" + "="*60)
    print("CHECKING TORCH/CUDA")
    print("="*60)
    
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            print(f"✓ CUDA available: YES")
            print(f"  GPU device: {torch.cuda.get_device_name(0)}")
            print(f"  CUDA version: {torch.version.cuda}")
        else:
            print(f"⚠ CUDA available: NO (CPU mode only)")
        
        return True
    except Exception as e:
        print(f"✗ Error checking CUDA: {e}")
        return False


def check_config():
    """Check configuration file"""
    print("\n" + "="*60)
    print("CHECKING CONFIGURATION")
    print("="*60)
    
    try:
        from config import get_config, MODEL_CONFIG, TRACKING_CONFIG
        config = get_config()
        
        print(f"✓ Config loaded successfully")
        print(f"  Model: {MODEL_CONFIG['model_name']}")
        print(f"  Confidence threshold: {MODEL_CONFIG['conf_threshold']}")
        print(f"  Max age: {TRACKING_CONFIG['max_age']}")
        print(f"  Min hits: {TRACKING_CONFIG['min_hits']}")
        
        return True
    except Exception as e:
        print(f"✗ Error loading config: {e}")
        return False


def check_yolo_model():
    """Check if YOLO model can be loaded"""
    print("\n" + "="*60)
    print("CHECKING YOLO MODEL")
    print("="*60)
    
    try:
        print("Attempting to load YOLOv8n model...")
        print("(This may take a moment on first run - it will download the model)")
        
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')
        
        print(f"✓ YOLO model loaded successfully")
        print(f"  Model: yolov8n.pt")
        print(f"  Classes: {len(model.names)}")
        
        return True
    except Exception as e:
        print(f"⚠ Error loading YOLO model: {e}")
        print(f"  This is normal if no internet connection. Model will download on first use.")
        return False


def check_webcam():
    """Check if webcam is available"""
    print("\n" + "="*60)
    print("CHECKING WEBCAM")
    print("="*60)
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            print(f"✓ Webcam available")
            print(f"  Resolution: {width}x{height}")
            print(f"  FPS: {fps}")
            
            cap.release()
            return True
        else:
            print(f"⚠ Webcam not available (this is OK if no webcam connected)")
            return False
    
    except Exception as e:
        print(f"⚠ Error checking webcam: {e}")
        return False


def run_all_checks():
    """Run all checks"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  OBJECT DETECTION & TRACKING SYSTEM - VALIDATION".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Run checks
    results.append(("Imports", check_imports()))
    results.append(("Project Structure", check_project_structure()))
    results.append(("Source Modules", check_src_modules()))
    results.append(("Torch/CUDA", check_torch_cuda()))
    results.append(("Configuration", check_config()))
    results.append(("YOLO Model", check_yolo_model()))
    results.append(("Webcam", check_webcam()))
    
    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "⚠ WARN"
        print(f"{status:10s} {check_name}")
    
    critical_checks = ["Imports", "Project Structure", "Source Modules", "Configuration"]
    critical_pass = all(result for name, result in results if name in critical_checks)
    
    print("\n" + "="*60)
    if critical_pass:
        print("✓ SYSTEM READY")
        print("\nYou can now run:")
        print("  - python quick_test.py       (Interactive testing)")
        print("  - python main.py             (Default webcam)")
        print("  - python demo.py             (Demo scripts)")
    else:
        print("✗ SYSTEM NOT READY")
        print("\nPlease fix the errors above and run validation again.")
    
    print("="*60 + "\n")
    
    return critical_pass


if __name__ == '__main__':
    try:
        success = run_all_checks()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nValidation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\nValidation error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
