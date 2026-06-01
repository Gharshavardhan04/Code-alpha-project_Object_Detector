# Object Detection and Tracking System

A real-time object detection and tracking system built with YOLO (You Only Look Once) and SORT (Simple Online and Realtime Tracking) algorithms. This system can process video files or live webcam feeds, detecting objects and tracking them across frames.

## Features

✓ **Real-time Object Detection** - Uses YOLOv8 for fast and accurate object detection
✓ **Multi-Object Tracking** - Implements SORT algorithm for tracking multiple objects
✓ **Live Webcam Support** - Process live video streams from webcam
✓ **Video File Processing** - Process video files in various formats
✓ **Bounding Box Visualization** - Displays detected objects with bounding boxes
✓ **Track ID Assignment** - Each object gets a unique tracking ID
✓ **Track History** - Shows motion trails for tracked objects
✓ **Performance Metrics** - Real-time FPS and object count display
✓ **Batch Processing** - Process multiple videos automatically
✓ **Output Video Saving** - Save processed videos with tracking results

## Project Structure

```
Object Detector/
├── main.py                    # Main entry point with CLI support
├── quick_test.py             # Interactive quick test script
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
│
├── src/
│   ├── __init__.py          # Package initialization
│   ├── detector.py          # YOLO object detection module
│   ├── tracker.py           # SORT tracking algorithm implementation
│   ├── utils.py             # Visualization and utility functions
│   └── video_processor.py    # Main video processing pipeline
│
├── models/                   # Pre-trained models directory
├── videos/                   # Input video files directory
├── output/                   # Output videos directory
└── README.md                # This file
```

## Installation

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Webcam (for live video) or video files

### 2. Setup Environment

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Installation time**: Usually 10-15 minutes (depends on internet speed and system)

### Dependencies

- **opencv-python**: Video processing and visualization
- **torch**: PyTorch for deep learning models
- **ultralytics**: YOLOv8 implementation
- **numpy**: Numerical computations
- **scipy**: Scientific computing
- **scikit-learn**: Machine learning utilities
- **Pillow**: Image processing
- **matplotlib**: Plotting and visualization

## Quick Start

### Option 1: Interactive Quick Test (Easiest)

```bash
python quick_test.py
```

This opens an interactive menu where you can:
1. Test with default webcam
2. Test with specific webcam ID
3. Select video files from the `videos/` folder
4. Enter custom video file path
5. Batch process all videos

### Option 2: Using Command Line

#### Test with Webcam

```bash
# Use default webcam
python main.py

# Specify webcam ID
python main.py --source 0

# Save output video
python main.py --source 0 --output output/webcam_tracked.mp4
```

#### Process Video File

```bash
python main.py --source videos/sample.mp4 --output output/sample_tracked.mp4
```

#### With Different YOLO Models

```bash
# Nano (fastest, default)
python main.py --model yolov8n.pt --source 0

# Small (balanced)
python main.py --model yolov8s.pt --source 0

# Medium (better accuracy)
python main.py --model yolov8m.pt --source 0

# Large (high accuracy)
python main.py --model yolov8l.pt --source 0

# Extra Large (highest accuracy)
python main.py --model yolov8x.pt --source 0
```

#### Adjust Parameters

```bash
# Lower confidence threshold (detect more objects)
python main.py --source 0 --conf 0.3

# Higher confidence threshold (detect only confident objects)
python main.py --source 0 --conf 0.7

# Adjust tracking parameters
python main.py --source 0 --max-age 50 --min-hits 5 --iou-threshold 0.4

# No display (faster processing)
python main.py --source videos/sample.mp4 --no-display

# No resizing (higher quality, slower)
python main.py --source 0 --no-resize
```

#### Batch Processing

```bash
# Process all videos in videos/ folder
python main.py --batch videos --output output/
```

## Configuration

Edit `config.py` to modify default settings:

```python
# Model Configuration
MODEL_CONFIG = {
    'model_name': 'yolov8n.pt',  # YOLO model size
    'conf_threshold': 0.5,        # Confidence threshold
}

# Tracking Configuration
TRACKING_CONFIG = {
    'max_age': 30,               # Max frames to keep track alive
    'min_hits': 3,               # Min detections to start tracking
    'iou_threshold': 0.3,        # IOU threshold for association
}

# Video Processing Configuration
VIDEO_CONFIG = {
    'display': True,             # Display video during processing
    'resize': True,              # Resize frames for faster processing
    'max_width': 1280,
    'max_height': 720,
}
```

## Keyboard Controls

While the application is running:

- **'q'** - Quit/Exit
- **'p'** - Pause/Resume video

## Usage Examples

### Example 1: Real-time Webcam Detection

```bash
python main.py
```

Press 'q' to exit.

### Example 2: Process Video File with Custom Settings

```bash
python main.py \
    --source videos/traffic.mp4 \
    --model yolov8m.pt \
    --conf 0.4 \
    --output output/traffic_tracked.mp4
```

### Example 3: Low-Power Mode (For slower systems)

```bash
python main.py --source 0 --model yolov8n.pt --no-resize --conf 0.6
```

### Example 4: High-Accuracy Mode

```bash
python main.py --source 0 --model yolov8x.pt --no-resize --conf 0.3
```

## YOLO Model Comparison

| Model | Speed | Accuracy | GPU Memory |
|-------|-------|----------|-----------|
| **yolov8n** | ⚡⚡⚡ Fastest | Good | ~1GB |
| **yolov8s** | ⚡⚡ Fast | Better | ~2GB |
| **yolov8m** | ⚡ Moderate | Very Good | ~3GB |
| **yolov8l** | Slow | High | ~4GB |
| **yolov8x** | ⚡ Slowest | Highest | ~5GB |

**Recommendation**: Start with `yolov8n.pt` for development, use `yolov8m.pt` or `yolov8l.pt` for production.

## Advanced Features

### Custom Object Detection

Modify the confidence threshold to detect specific types of objects:

- High threshold (0.7-0.9): Only confident detections
- Medium threshold (0.4-0.6): Balanced (default)
- Low threshold (0.1-0.3): Sensitive, may have false positives

### Tracking Parameters

- **max_age**: Increase to keep tracks alive longer (smoother tracking)
- **min_hits**: Increase to require more detections before starting track (fewer false tracks)
- **iou_threshold**: Increase for stricter matching (better for crowded scenes)

### Batch Processing

Process multiple videos in a folder:

```bash
python main.py --batch videos/
```

Output videos will be saved to `output/` directory.

## Troubleshooting

### Issue: "No module named 'ultralytics'"

**Solution**: Install dependencies again
```bash
pip install -r requirements.txt
```

### Issue: "Cannot open video source"

**Solution**: 
- Verify video file exists
- Check video file format is supported (mp4, avi, mov, mkv)
- For webcam, try different IDs: `--source 0`, `--source 1`, etc.

### Issue: Low FPS / Slow Processing

**Solution**:
- Use smaller YOLO model: `--model yolov8n.pt`
- Enable frame resizing: `--resize` (default enabled)
- Lower confidence threshold: `--conf 0.7`
- Disable display: `--no-display`

### Issue: Missing Detections

**Solution**:
- Lower confidence threshold: `--conf 0.3`
- Use larger YOLO model: `--model yolov8m.pt` or `--model yolov8l.pt`
- Ensure good lighting for video input

### Issue: CUDA/GPU not being used

**Solution**:
- Ensure NVIDIA GPU drivers are installed
- Verify PyTorch is installed with CUDA support
- Check available GPU: `torch.cuda.is_available()` in Python

## Performance Tips

1. **For Real-time Processing**:
   - Use `yolov8n.pt` or `yolov8s.pt`
   - Enable frame resizing
   - Increase confidence threshold

2. **For High Accuracy**:
   - Use `yolov8l.pt` or `yolov8x.pt`
   - Disable frame resizing
   - Lower confidence threshold

3. **For Long Videos**:
   - Use `--no-display` flag
   - Enable multi-threading in VideoHandler
   - Consider batch processing on GPU

## Output

The system generates:

1. **Console Output**: Real-time statistics and frame count
2. **Video Window**: Live visualization with bounding boxes and tracking IDs
3. **Output Video** (optional): Saved video file with tracking results
4. **Statistics**: Processing time, average FPS, min/max FPS

## API Usage

Use the modules in your own Python code:

```python
from src.video_processor import VideoObjectDetectionTracker

# Create pipeline
pipeline = VideoObjectDetectionTracker(
    model_name='yolov8m.pt',
    conf_threshold=0.5,
    max_age=30,
    min_hits=3,
    iou_threshold=0.3
)

# Process video
pipeline.process_video(
    source='videos/sample.mp4',
    output_path='output/tracked.mp4',
    display=True,
    resize=True
)
```

## System Requirements

### Minimum (CPU only)
- Intel i5 / AMD Ryzen 5
- 8GB RAM
- 2GB disk space for models

### Recommended (GPU)
- Intel i7 / AMD Ryzen 7
- 16GB RAM
- NVIDIA GTX 1060 or better
- 4GB disk space for models

### Optimal (High Performance)
- Intel i9 / AMD Ryzen 9
- 32GB RAM
- NVIDIA RTX 2080 or better
- 8GB disk space

## License

This project uses YOLOv8 (Ultralytics) which is licensed under AGPL-3.0.
For commercial use, please check the license requirements.

## References

- **YOLOv8**: https://github.com/ultralytics/ultralytics
- **SORT Algorithm**: https://github.com/abewley/sort
- **Kalman Filter**: https://en.wikipedia.org/wiki/Kalman_filter

## Future Enhancements

- [ ] Multi-GPU support
- [ ] GPU batch processing
- [ ] Custom model training
- [ ] Person re-identification
- [ ] Crowd counting
- [ ] Anomaly detection
- [ ] Web interface
- [ ] Mobile app support

---

**Created**: May 2026
**Version**: 1.0.0
