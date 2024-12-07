import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    # 마이크로 입력 설정
    with sr.Microphone() as source:
        print("말씀해주세요...")

        # 마이크로부터 음성 입력을 듣습니다.
        audio_data = recognizer.listen(source)

        try:
            # 음성 데이터를 텍스트로 변환합니다.
            text = recognizer.recognize_google(audio_data, language="ko-KR")
            print("인식된 텍스트:", text)
        except sr.UnknownValueError:
            print("음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            print("Google Speech Recognition 서비스에 접근할 수 없습니다:", e)

# 음성 인식 실행
recognize_speech()
