#!/usr/bin/env python
"""
GETTING STARTED GUIDE
Object Detection and Tracking System
"""

QUICK_START = """
╔════════════════════════════════════════════════════════════════════════════╗
║                          GETTING STARTED GUIDE                            ║
║              Object Detection and Tracking System                          ║
╚════════════════════════════════════════════════════════════════════════════╝


🚀 FASTEST WAY TO START (30 SECONDS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Open terminal/command prompt in Object Detector folder

Step 2: Run interactive menu:
        python quick_test.py

Step 3: Select option 1 (Default Webcam)

Step 4: Press 'q' to exit

That's it! You'll see:
  ✓ Live webcam feed
  ✓ Bounding boxes around detected objects
  ✓ Tracking IDs (unique number for each object)
  ✓ Motion trails showing where objects moved
  ✓ FPS counter and object count


📋 ALL COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Interactive Testing:
  python quick_test.py              # Menu-driven testing (RECOMMENDED)
  python demo.py                    # 6 demo scenarios

Command Line:
  python main.py                    # Default: webcam
  python main.py --help             # Show all options

Video Processing:
  python main.py --source videos/sample.mp4
  python main.py --source 0 --output output/tracked.mp4

Model Selection:
  python main.py --model yolov8n.pt # Nano (fastest)
  python main.py --model yolov8m.pt # Medium (better accuracy)
  python main.py --model yolov8l.pt # Large (high accuracy)

Adjustment:
  python main.py --conf 0.3         # More detections
  python main.py --conf 0.7         # Fewer detections
  python main.py --no-display       # Faster (no window)
  python main.py --no-resize        # Higher quality

Batch Processing:
  python main.py --batch videos/    # Process all videos

Validation:
  python validate.py                # System health check


🎯 COMMON USE CASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

USE CASE 1: Test with Webcam
  Command: python quick_test.py
           Select option 1
  Result: Live webcam with object tracking

USE CASE 2: Process Video File
  Command: python main.py --source videos/traffic.mp4 \\
           --output output/traffic_tracked.mp4
  Result: Saved video with tracking

USE CASE 3: Detect Specific Objects Only
  Edit config.py: TARGET_CLASSES = ['person', 'car']
  Command: python main.py
  Result: Only tracks people and cars

USE CASE 4: Higher Accuracy (Slower)
  Command: python main.py --model yolov8l.pt
  Result: Better accuracy, slower FPS

USE CASE 5: Speed Optimized (CPU)
  Command: python main.py --model yolov8n.pt --conf 0.6 --no-resize
  Result: Maximum speed on CPU

USE CASE 6: Batch Process Videos
  1. Place videos in videos/ folder
  2. Command: python main.py --batch videos/
  3. Check output/ folder for results


📊 WHAT YOU SEE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

On Screen:
  ✓ Bounding boxes (colored rectangles around objects)
  ✓ Tracking IDs (e.g., "ID: 1", "ID: 2")
  ✓ Motion trails (lines showing where objects moved)
  ✓ FPS counter (frames processed per second)
  ✓ Object count (number of objects being tracked)

Console Output:
  ✓ Frame number progress
  ✓ FPS statistics
  ✓ Processing information
  ✓ Summary statistics at end


🔑 KEYBOARD SHORTCUTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

While running:
  'q'     Exit/Quit
  'p'     Pause/Resume


⚙️ PARAMETERS EXPLAINED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Confidence Threshold (--conf):
  0.1-0.3 = Very sensitive (many false positives)
  0.4-0.6 = Balanced (default: 0.5)
  0.7-0.9 = Conservative (fewer, more reliable detections)

Model Size (--model):
  yolov8n = Nano (fastest, ~6 MB)
  yolov8s = Small (fast, ~22 MB)
  yolov8m = Medium (balanced, ~49 MB)
  yolov8l = Large (accurate, ~94 MB)
  yolov8x = XLarge (most accurate, ~168 MB)

Resize (--resize or --no-resize):
  --resize      = Smaller frames (default, faster)
  --no-resize   = Keep original size (slower, higher quality)

Display (--display or --no-display):
  --display     = Show window (default)
  --no-display  = Faster (no visualization)

Tracking Parameters:
  --max-age     = How long to remember disappeared objects (default: 30)
  --min-hits    = Min detections before starting track (default: 3)
  --iou-threshold = Matching sensitivity (default: 0.3)


💾 OUTPUT FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When you use --output flag:
  Input:  videos/sample.mp4
  Output: output/sample_tracked.mp4 (or your custom path)

Files are saved in output/ directory:
  output/webcam_tracked.mp4
  output/traffic_tracked.mp4
  output/sample_tracked.mp4
  etc.


🎨 COLORS AND VISUALIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Each tracked object gets:
  ✓ Unique color (automatically assigned)
  ✓ Tracking ID (e.g., "ID: 5")
  ✓ Motion trail (line showing movement history)
  ✓ Current bounding box

Colors cycle through 100 distinct colors to help distinguish objects


📂 FILE ORGANIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Add input videos to:  videos/ folder
Output videos go to:  output/ folder
Models download to:   yolov8n.pt (in current directory)

Example:
  Object Detector/
    ├── videos/
    │   ├── sample.mp4
    │   ├── traffic.mp4
    │   └── street.mp4
    ├── output/
    │   ├── sample_tracked.mp4
    │   ├── traffic_tracked.mp4
    │   └── street_tracked.mp4
    └── (other files)


🎓 LEARNING PATH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Beginner:
  1. Run: python quick_test.py → Option 1
  2. Try: python main.py
  3. Explore: python demo.py

Intermediate:
  1. Process video files
  2. Adjust confidence threshold
  3. Try different models
  4. Read README_COMPLETE.md

Advanced:
  1. Batch process multiple videos
  2. Customize tracking parameters
  3. Modify config.py
  4. Use API directly in Python scripts


🔍 DEBUGGING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: No webcam detected
  Solution: python main.py --source 1 (try different ID)

Problem: Very slow FPS
  Solution: python main.py --model yolov8n.pt --no-resize

Problem: Missing objects
  Solution: python main.py --conf 0.3 (lower threshold)

Problem: False positives
  Solution: python main.py --conf 0.7 (raise threshold)

Problem: Can't find video file
  Solution: python main.py --source "C:\\full\\path\\to\\video.mp4"

Problem: Out of memory
  Solution: python main.py --model yolov8n.pt --resize


📞 QUICK REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Start with: python quick_test.py
View help: python main.py --help
Validate: python validate.py
Read docs: Open README_COMPLETE.md


═════════════════════════════════════════════════════════════════════════════════
Ready to go! Type: python quick_test.py
═════════════════════════════════════════════════════════════════════════════════
"""

if __name__ == '__main__':
    print(QUICK_START)
