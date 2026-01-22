finger_tips = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_count = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            if lm[finger_tips[0]].x < lm[finger_tips[0] - 1].x:
                finger_count += 1

            for tip in finger_tips[1:]:
                if lm[tip].y < lm[tip - 2].y:
                    finger_count += 1

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    label = f"Fingers: {finger_count}"

    (text_width, text_height), _ = cv2.getTextSize(
        label,
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        3
    )
