import cv2 as cv
from datetime import datetime

video_capture = cv.VideoCapture(0)

if not video_capture.isOpened():
    print('Cannot open webcam.')
    exit()

fourcc = cv.VideoWriter_fourcc(*'XVID')
video_writer = None

record_mode = False
date_mode = False
record_count = 0

while video_capture.isOpened():
    valid, frame = video_capture.read()
    if not valid:
        print('Unable to read video')
        break

    flipped_frame = cv.flip(frame, 1)

    # Create a copy of the frame for displaying
    display_frame = flipped_frame.copy()

    # Record today's date in date mode(Similar to the data back function found in film cameras)
    if date_mode:
        current_date = datetime.now().strftime("%y %m %d")
        cv.putText(display_frame, current_date, (10, 20), cv.FONT_HERSHEY_TRIPLEX , 0.5, (0, 0, 0))
        cv.putText(flipped_frame, current_date, (10, 20), cv.FONT_HERSHEY_TRIPLEX , 0.5, (0, 0, 0))

    # Put a text to indicate recording mode only in preview mode
    if record_mode:
        cv.putText(display_frame, 'Recording :)', (10, 40), cv.FONT_HERSHEY_TRIPLEX , 0.5, (0, 0, 255))

    cv.imshow('Webcam Recorder', display_frame)

    key = cv.waitKey(1) & 0xFF

    # Press ENTER to toggle date mode
    if key == 13:
        date_mode = not date_mode

    # Press SPACE to toggle record mode
    if key == ord(' '):
        record_mode = not record_mode
        if record_mode:
            record_count += 1
            video_writer = cv.VideoWriter(f'video_{record_count}.avi', fourcc, 30.0, (640, 480))
        else:
            video_writer.release()
            video_writer = None

    # Write frames if in record mode
    if record_mode:
        video_writer.write(flipped_frame)

    # Press ESC to exit
    if key == 27:
        break

video_capture.release()
if video_writer is not None:
    video_writer.release()
cv.destroyAllWindows()