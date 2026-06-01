"""
Main entry point for Object Detection and Tracking application
"""
import argparse
import os
from pathlib import Path
from src.video_processor import VideoObjectDetectionTracker, BatchVideoProcessor


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Real-time Object Detection and Tracking with YOLO and SORT'
    )
    
    parser.add_argument(
        '--source',
        type=str,
        default='0',
        help='Video source: webcam index (0, 1, ...) or video file path'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='yolov8n.pt',
        choices=['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt'],
        help='YOLO model size: nano, small, medium, large, xlarge'
    )
    
    parser.add_argument(
        '--conf',
        type=float,
        default=0.5,
        help='Confidence threshold for detections (0-1)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output video path (optional)'
    )
    
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Do not display video during processing'
    )
    
    parser.add_argument(
        '--no-resize',
        action='store_true',
        help='Do not resize frames (slower but higher quality)'
    )
    
    parser.add_argument(
        '--max-age',
        type=int,
        default=30,
        help='Maximum frames to keep track alive'
    )
    
    parser.add_argument(
        '--min-hits',
        type=int,
        default=3,
        help='Minimum detections to start tracking'
    )
    
    parser.add_argument(
        '--iou-threshold',
        type=float,
        default=0.3,
        help='IOU threshold for tracking association'
    )
    
    parser.add_argument(
        '--batch',
        type=str,
        default=None,
        help='Directory containing multiple videos for batch processing'
    )
    
    args = parser.parse_args()
    
    # Parse source
    try:
        source = int(args.source)  # Try to parse as webcam index
    except ValueError:
        source = args.source  # Use as file path
    
    # Create pipeline
    pipeline = VideoObjectDetectionTracker(
        model_name=args.model,
        conf_threshold=args.conf,
        max_age=args.max_age,
        min_hits=args.min_hits,
        iou_threshold=args.iou_threshold
    )
    
    # Batch processing
    if args.batch:
        print(f"Batch processing videos from: {args.batch}")
        video_files = []
        for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv']:
            video_files.extend(Path(args.batch).glob(ext))
        
        if not video_files:
            print("No video files found in batch directory")
            return
        
        batch_processor = BatchVideoProcessor(args.model, args.conf)
        batch_processor.process_batch(video_files, args.output)
    
    else:
        # Single video processing
        print("\n" + "="*60)
        print("OBJECT DETECTION AND TRACKING")
        print("="*60)
        print(f"Source: {source if isinstance(source, int) else source}")
        print(f"Model: {args.model}")
        print(f"Confidence threshold: {args.conf}")
        print(f"Max age: {args.max_age}")
        print(f"Min hits: {args.min_hits}")
        print(f"IOU threshold: {args.iou_threshold}")
        if args.output:
            print(f"Output: {args.output}")
        print("="*60 + "\n")
        
        # Process video
        pipeline.process_video(
            source=source,
            output_path=args.output,
            display=not args.no_display,
            resize=not args.no_resize
        )


if __name__ == '__main__':
    main()
    
    # Batch processing
    if args.batch:
        if not os.path.isdir(args.batch):
            print(f"Batch directory not found: {args.batch}")
            return
        
        video_files = [
            os.path.join(args.batch, f)
            for f in os.listdir(args.batch)
            if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
        ]
        
        if not video_files:
            print(f"No video files found in {args.batch}")
            return
        
        batch_processor = BatchVideoProcessor(args.model, args.conf)
        batch_processor.process_batch(video_files, 'output')
    else:
        # Single video processing
        pipeline.process_video(
            source=source,
            output_path=args.output,
            display=not args.no_display,
            resize=not args.no_resize
        )


if __name__ == '__main__':
    main()
