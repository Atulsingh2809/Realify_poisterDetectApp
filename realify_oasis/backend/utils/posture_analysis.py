import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

def left_toe_x(landmarks):
    return landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x

def analyze_posture(video_capture):
    feedback = []
    pose = mp_pose.Pose()

    frame_count = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_count += 1
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            try:
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
                left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
                toe_x = left_toe_x(landmarks)

                # Calculate back angle
                back_angle = calculate_angle(
                    [left_shoulder.x, left_shoulder.y],
                    [left_hip.x, left_hip.y],
                    [left_knee.x, left_knee.y]
                )

                if back_angle < 150:
                    feedback.append(f"Frame {frame_count}: Squat ({back_angle:.2f}°)")

                if left_knee.x > toe_x:
                    feedback.append(f"Frame {frame_count}: Desk Sitting")

            except Exception as e:
                feedback.append(f"Frame {frame_count}: Landmark extraction error - {str(e)}")

    video_capture.release()
    return feedback
