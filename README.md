# Object Detector - Real-time Object Detection and Tracking

A complete system for real-time object detection and tracking using YOLO and SORT algorithm.

## Features

✨ **Object Detection**
- YOLOv8 real-time object detection
- Multiple model sizes (nano to xlarge)
- Configurable confidence threshold
- Support for 80 COCO classes

📍 **Object Tracking**
- SORT (Simple Online and Realtime Tracking) algorithm
- Kalman Filter-based motion prediction
- Unique tracking IDs for each object
- Track history visualization

🎥 **Video Input/Output**
- Webcam support (real-time)
- Video file support (MP4, AVI, MOV, etc.)
- Real-time display with visualization
- Save processed video with tracking results

📊 **Visualization**
- Bounding boxes with object classes
- Unique colors for each track ID
- Track history lines showing object movement
- FPS and object count display
- Real-time statistics

⚙️ **Configuration**
- Easily adjustable parameters
- Batch processing support
- Command-line interface
- Quick-start scripts

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Webcam or video files

### Setup

1. **Clone or navigate to the project:**
   ```bash
   cd "Object Detector"
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Note: First run will download the YOLO model (~100MB for nano, ~200MB+ for larger models)

## Quick Start

### 1. Webcam Demo (Real-time)
```bash
python quick_start.py webcam
```
- Press 'q' to quit
- Press 'p' to pause/resume

### 2. Video Processing
Place a video in the `videos/` folder, then:
```bash
python quick_start.py video
```

### 3. Custom Video
```bash
python quick_start.py path/to/your/video.mp4
```

### 4. Command-line Usage
```bash
python main.py --source 0 --model yolov8n.pt --conf 0.5 --output output/result.mp4
```

## Command-line Arguments

```
--source          Video source: webcam index (0, 1, ...) or video file path
--model           YOLO model: yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
--conf            Confidence threshold (0-1, default: 0.5)
--output          Output video path (optional)
--no-display      Do not display video during processing
--no-resize       Do not resize frames (slower but higher quality)
--max-age         Maximum frames to keep track alive (default: 30)
--min-hits        Minimum detections to start tracking (default: 3)
--iou-threshold   IOU threshold for tracking (default: 0.3)
--batch           Directory for batch processing multiple videos
```

### Examples

**Webcam with large model:**
```bash
python main.py --source 0 --model yolov8l.pt --conf 0.6
```

**Video file with tracking output:**
```bash
python main.py --source videos/test.mp4 --output output/tracked.mp4
```

**Batch processing:**
```bash
python main.py --batch videos --output output
```

## Configuration

Edit `config.py` to customize:
- Model selection
- Confidence threshold
- Tracking parameters
- Video processing settings
- Visualization options

## Project Structure

```
Object Detector/
├── main.py                 # Main entry point
├── quick_start.py         # Quick start scripts
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── src/
│   ├── detector.py        # YOLO detection module
│   ├── tracker.py         # SORT tracking algorithm
│   ├── video_processor.py # Main processing pipeline
│   └── utils.py           # Utility functions
├── models/                # Downloaded YOLO models
├── videos/                # Input video files
└── output/                # Processed video output
```

## Performance Tips

1. **Speed vs Accuracy Trade-off:**
   - Fast: Use `yolov8n.pt` (nano)
   - Balanced: Use `yolov8s.pt` (small)
   - Accurate: Use `yolov8m.pt` or larger

2. **Processing Speed:**
   - Smaller models are faster
   - Resizing frames speeds up processing
   - GPU acceleration (if available) significantly improves performance

3. **Memory Usage:**
   - Nano model: ~100MB
   - Small model: ~200MB
   - Larger models: 500MB+

## Troubleshooting

### CUDA/GPU not found
The system will automatically fall back to CPU. For GPU support:
```bash
pip install torch torchvision torcuda
```

### Out of Memory
- Use smaller model (e.g., `yolov8n.pt`)
- Enable frame resizing with `--resize`
- Reduce input resolution

### Slow Performance
- Use GPU if available
- Use smaller model
- Enable frame resizing
- Reduce confidence threshold slightly

### Video codec errors
Install ffmpeg:
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

## Model Comparison

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| nano | ~40MB | ⚡⚡⚡ | ⭐⭐ | Real-time, low resources |
| small | ~80MB | ⚡⚡ | ⭐⭐⭐ | Good balance |
| medium | ~150MB | ⚡ | ⭐⭐⭐⭐ | Better accuracy |
| large | ~250MB | 🐢 | ⭐⭐⭐⭐⭐ | High accuracy |
| xlarge | ~350MB | 🐢🐢 | ⭐⭐⭐⭐⭐ | Maximum accuracy |

## Detectable Classes (COCO Dataset)

The model can detect 80 different object classes including:
- Persons, animals, vehicles
- Sports equipment, household items
- Tools, furniture, and much more

For detailed class list, see [COCO Classes](https://cocodataset.org/).

## Advanced Usage

### Custom Tracking Parameters
```python
from src.video_processor import VideoObjectDetectionTracker

pipeline = VideoObjectDetectionTracker(
    model_name='yolov8m.pt',
    conf_threshold=0.6,
    max_age=50,           # Keep tracks alive longer
    min_hits=2,           # Start tracking sooner
    iou_threshold=0.4     # More strict association
)

pipeline.process_video(source='video.mp4', output_path='output.mp4')
```

### Batch Processing
```python
from src.video_processor import BatchVideoProcessor

processor = BatchVideoProcessor('yolov8s.pt')
processor.process_batch(
    ['video1.mp4', 'video2.mp4', 'video3.mp4'],
    output_dir='output'
)
```

## Output Format

Tracked objects are displayed with:
- **Bounding Box**: Green/colored rectangle around object
- **Track ID**: Unique identifier for each tracked object
- **Class Label**: Type of detected object (if space allows)
- **Track History**: Lines showing object movement path
- **FPS**: Real-time processing speed
- **Object Count**: Number of currently tracked objects

## System Requirements

- **Processor**: Intel/AMD processor with SSE support
- **RAM**: 4GB minimum (8GB recommended)
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)
- **Storage**: 1GB for models + space for videos

## License

This project uses:
- YOLOv8 (Ultralytics) - AGPL-3.0
- OpenCV - Apache 2.0
- PyTorch - BSD

Ensure compliance with respective licenses.

## Future Enhancements

- [ ] Deep SORT with appearance features
- [ ] Multi-class specific tracking
- [ ] Heat map generation
- [ ] Object counting per zone
- [ ] Trajectory analysis
- [ ] Web interface
- [ ] Real-time streaming support

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review example scripts
3. Check model documentation

## References

- [YOLOv8 Documentation](https://github.com/ultralytics/ultralytics)
- [SORT Paper](https://arxiv.org/abs/1602.00763)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyTorch Documentation](https://pytorch.org/)
