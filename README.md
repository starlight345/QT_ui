# QT_ui
make qt program to show images/videos/text

# final.py
- 카메라 개수와 상관없이 실행되도록 수정
- 때때로 카메라가 연결되어도 NoneType 에러 발생(원인 불분명)
- 해결 방안: 다른 포트에 카메라 연결

# path.py
- 현재 연결된 카메라들의 path를 리스트로 반환

# chatgpt.py
- 간격 조정된 영상 3개, 이미지 3개, 등급
- 등급은 3초마다 1씩 증가

# check_cam.py
- 카메라 정상 연결 확인
