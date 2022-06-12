#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque

import cv2 as cv
import numpy as np
import mediapipe as mp

from utils import CvFpsCalc
from model import KeyPointClassifier

import test
import os
import tensorflow as tf

tf.debugging.set_log_device_placement(True)
def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)
    parser.add_argument("--output_frame",
                        help="Output one classfied result for every X frames (default 1)",
                        type=int,
                        default=5)
    parser.add_argument("--video_dir",
                        help="Directory containing the input videos, specify yes or no in the end of dir_name",
                        type=str)
    
    args = parser.parse_args()

    return args


def main():
    # Argument parsing #################################################################
    args = get_args()

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence
    output_frame = args.output_frame
    video_dir = args.video_dir
    answer = 'Y' if video_dir[-3:] == 'yes' else 'N'

    # Model load #############################################################
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=2,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    keypoint_classifier = KeyPointClassifier()

    # Read labels ###########################################################
    with open('model/keypoint_classifier/keypoint_classifier_label.csv',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]

    # Start processing videos #############################################################
    # Initialize variables
    total_case = 0
    success_case = 0
    fail_case = 0

    # Read input videos one by one
    for filename in os.listdir(video_dir):

        # Video preparation ###############################################################
        cap = cv.VideoCapture(os.path.join(video_dir, filename))
        
        # Initialize variables and list
        cur_frame_count = 0
        output_result_left = []
        output_result_right = []

        # Loop through the whole video
        while cap.isOpened():
            ret, image = cap.read()
            if not ret:
                break
            output_this_frame = True if cur_frame_count % output_frame == 0 else False

            # Update the frame_count
            cur_frame_count += 1

            # If this frame is not necessary, just skip it.
            if not output_this_frame:
                continue

            # Detection implementation ####################################################
            image = cv.flip(image, 1)  # Mirror display
            debug_image = copy.deepcopy(image)

            
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True


            # Processing the data from mediapipe, and use it to classify ##################

            # Initialize variables
            found_right_hand = False
            found_left_hand = False
            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                    results.multi_handedness):
                    # Landmark calculation
                    landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                    # Conversion to relative coordinates / normalized coordinates
                    pre_processed_landmark_list = pre_process_landmark(
                        landmark_list)

                    # Hand sign classification
                    hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                    # If this frame should be output, and the current hand haven't be found
                    if output_this_frame:
                        if not(found_right_hand) and handedness.classification[0].label[0:] == 'Right':
                            found_right_hand = True
                            output_result_right.append(keypoint_classifier_labels[hand_sign_id])
                        elif not(found_left_hand):
                            found_left_hand = True
                            output_result_left.append(keypoint_classifier_labels[hand_sign_id])
            
            # If this frame should be output, and there're some hands not found by above procedure.
            if output_this_frame:
                if not(found_right_hand):
                    output_result_right.append('X')
                if not(found_left_hand):
                    output_result_left.append('X')


        cap.release()
        
        # Write result list to result.csv
        with open('result.csv', 'w') as f:
            f.write('L: ')
            for data in output_result_left:
                f.write(data + ' ')
            f.write('\n')
            f.write('R: ')
            for data in output_result_right:
                f.write(data + ' ')
            f.write('\n')

        # Get the 5-4-0 prediction result from test.test()
        classified_result = 'Y' if test.test() else 'N' 

        # Update case counts
        total_case += 1
        if classified_result == answer:
            success_case += 1
        else:
            fail_case += 1
        
        # Output the result for current video
        print(f'{total_case}: Filename = {filename}, Answer = {answer}, Result = {classified_result}', end='')
        print(f'   ========>  {"Correct" if classified_result == answer else "Incorrect"}')

    print(f'Total cases: {total_case}, Success: {success_case}, Fail: {fail_case}')
    print(f'Accuracy = {round((success_case/total_case) * 100, 2)} %')



def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


if __name__ == '__main__':
    main()
