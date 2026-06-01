"""
SORT (Simple Online and Realtime Tracking) Algorithm Implementation
"""
import numpy as np
from scipy.optimize import linear_sum_assignment
from collections import defaultdict


class KalmanTracker:
    """Kalman Filter for tracking bounding boxes"""
    
    def __init__(self, bbox):
        """
        Initialize Kalman tracker with detection
        
        Args:
            bbox: [x1, y1, x2, y2] bounding box
        """
        # State: [x, y, width, height, vx, vy, vw, vh]
        self.state = np.array([
            (bbox[0] + bbox[2]) / 2,  # x (center)
            (bbox[1] + bbox[3]) / 2,  # y (center)
            bbox[2] - bbox[0],         # width
            bbox[3] - bbox[1],         # height
            0, 0, 0, 0                 # velocities (initialized to 0)
        ], dtype=np.float32)
        
        # Covariance matrix
        self.covariance = np.eye(8, 8) * 10.0
        self.covariance[4:, 4:] *= 1000.0  # High uncertainty in velocities
        
        # Process and measurement noise
        self.process_noise = np.eye(8, 8) * 0.01
        self.process_noise[4:, 4:] *= 0.01
        self.measurement_noise = np.eye(4, 4) * 10.0
        
        self.time_since_update = 0
    
    def predict(self):
        """Predict next state using constant velocity model"""
        # Update state with velocity
        self.state[:4] += self.state[4:]
        
        # Increase uncertainty
        self.covariance += self.process_noise
        self.time_since_update += 1
    
    def update(self, bbox):
        """Update state with new measurement"""
        # Measurement: [x, y, width, height]
        measurement = np.array([
            (bbox[0] + bbox[2]) / 2,
            (bbox[1] + bbox[3]) / 2,
            bbox[2] - bbox[0],
            bbox[3] - bbox[1]
        ], dtype=np.float32)
        
        # Measurement matrix (extracts position/size from 8D state)
        H = np.eye(4, 8)
        
        # Innovation covariance: S = H @ P @ H.T + R
        S = H @ self.covariance @ H.T + self.measurement_noise
        
        # Kalman gain: K = P @ H.T @ inv(S)
        K = self.covariance @ H.T @ np.linalg.inv(S)
        
        # Innovation
        innovation = measurement - H @ self.state
        
        # Update state: x = x + K @ innovation
        self.state += (K @ innovation).flatten()
        
        # Update covariance: P = (I - K @ H) @ P
        self.covariance = (np.eye(8, 8) - K @ H) @ self.covariance
        
        self.time_since_update = 0
    
    def get_bbox(self):
        """Get bounding box from state"""
        x, y, w, h = self.state[:4]
        return np.array([x - w/2, y - h/2, x + w/2, y + h/2])
    
    def get_centroid(self):
        """Get centroid from state"""
        return self.state[:2]


class SORTTracker:
    """SORT: Simple Online and Realtime Tracking"""
    
    def __init__(self, max_age=30, min_hits=3, iou_threshold=0.3):
        """
        Initialize SORT tracker
        
        Args:
            max_age: Maximum number of frames to keep alive a track
            min_hits: Minimum number of detections to start tracking
            iou_threshold: IOU threshold for association
        """
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        
        self.trackers = []  # Active trackers
        self.next_id = 1
        self.frame_count = 0
    
    def update(self, detections):
        """
        Update tracker with new detections
        
        Args:
            detections: Array of [x1, y1, x2, y2, conf, class_id]
        
        Returns:
            tracks: Array of [x1, y1, x2, y2, track_id]
        """
        self.frame_count += 1
        
        # Predict positions
        for tracker in self.trackers:
            tracker.predict()
        
        # Get predicted positions
        predicted_boxes = np.array([t.get_bbox() for t in self.trackers])
        
        # Association
        if len(detections) > 0 and len(self.trackers) > 0:
            # Calculate IOUs
            iou_matrix = self._compute_iou_matrix(predicted_boxes, detections[:, :4])
            
            # Hungarian algorithm for assignment
            matched, unmatched_dets, unmatched_trks = self._linear_assignment(iou_matrix)
        else:
            matched = []
            unmatched_dets = list(range(len(detections)))
            unmatched_trks = list(range(len(self.trackers)))
        
        # Update matched trackers
        for d, t in matched:
            self.trackers[t].update(detections[d, :4])
        
        # Create new trackers for unmatched detections
        for d in unmatched_dets:
            tracker = KalmanTracker(detections[d, :4])
            self.trackers.append(tracker)
        
        # Remove old trackers
        self.trackers = [t for t in self.trackers if t.time_since_update < self.max_age]
        
        # Get output tracks
        output_tracks = []
        for i, tracker in enumerate(self.trackers):
            # Only output if minimum hits reached
            if self.frame_count - i > self.min_hits:
                bbox = tracker.get_bbox()
                output_tracks.append([
                    bbox[0], bbox[1], bbox[2], bbox[3],
                    self.next_id + i
                ])
        
        return np.array(output_tracks) if output_tracks else np.empty((0, 5))
    
    def _compute_iou_matrix(self, predicted, detected):
        """Compute IOU matrix between predicted and detected boxes"""
        iou_matrix = np.zeros((len(predicted), len(detected)))
        
        for i, pred_box in enumerate(predicted):
            for j, det_box in enumerate(detected):
                iou_matrix[i, j] = self._iou(pred_box, det_box)
        
        return iou_matrix
    
    def _iou(self, box1, box2):
        """Calculate IOU between two boxes"""
        x1_inter = max(box1[0], box2[0])
        y1_inter = max(box1[1], box2[1])
        x2_inter = min(box1[2], box2[2])
        y2_inter = min(box1[3], box2[3])
        
        if x2_inter < x1_inter or y2_inter < y1_inter:
            return 0.0
        
        inter_area = (x2_inter - x1_inter) * (y2_inter - y1_inter)
        
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
        
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0.0
    
    def _linear_assignment(self, iou_matrix):
        """Hungarian algorithm for assignment"""
        # Convert to cost matrix (negative IOU)
        cost_matrix = 1.0 - np.clip(iou_matrix, 0, 1)
        
        # Set high cost for low IOU
        cost_matrix[iou_matrix < self.iou_threshold] = 1e6
        
        if cost_matrix.size == 0:
            return [], list(range(cost_matrix.shape[1])), list(range(cost_matrix.shape[0]))
        
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        matched = []
        unmatched_dets = list(range(cost_matrix.shape[1]))
        unmatched_trks = list(range(cost_matrix.shape[0]))
        
        for r, c in zip(row_ind, col_ind):
            if cost_matrix[r, c] < 1e5:
                matched.append([c, r])
                unmatched_dets.remove(c)
                unmatched_trks.remove(r)
        
        return matched, unmatched_dets, unmatched_trks
        unmatched_trks = list(range(cost_matrix.shape[0]))
        
        for r, c in zip(row_ind, col_ind):
            if cost_matrix[r, c] < 1e5:
                matched.append((c, r))
                if c in unmatched_dets:
                    unmatched_dets.remove(c)
                if r in unmatched_trks:
                    unmatched_trks.remove(r)
        
        return matched, unmatched_dets, unmatched_trks
