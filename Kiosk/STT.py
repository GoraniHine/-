import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import io
from google.cloud import texttospeech
import random

# 인증된 서비스 계정의 키 파일 경로
credentials_file_path = "/home/minschoi/ttspeak-425308-a6418acbe631.json"

def speak(text):
    # Text-to-Speech 클라이언트 생성
    client = texttospeech.TextToSpeechClient.from_service_account_json(credentials_file_path)

    # TTS 입력 설정
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # TTS 출력 설정
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",  # 한국어로 설정
        name="ko-KR-Wavenet-A"  # 한국어 음성 모델 선택
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # MP3로 출력 설정
    )

    # Text-to-Speech API 호출
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # TTS 결과를 재생
    audio = AudioSegment.from_file(io.BytesIO(response.audio_content), format="mp3")
    play(audio)

class DrinkKiosk:
    def __init__(self):
        self.drink_prices = {"불고기버거": 5000, "치킨버거": 4000, "치즈버거": 6000}
        self.orders = {}

    def take_order(self):
        while True:
            recognizer = sr.Recognizer()
            
            # 메뉴 선택
            with sr.Microphone() as source:
                print("주문하실 햄버거를 말씀해주세요:")
                speak("주문하실 햄버거를 말씀해주세요")
                audio = recognizer.listen(source)

            try:
                menu = recognizer.recognize_google(audio, language="ko-KR")
                print("주문할 햄버거:", menu)
                # 만약 주문에 '불고기 버거', '치킨버거', '치즈버거' 중 하나가 있으면 계속 진행
                if any(keyword in menu for keyword in ['불고기 버거', '치킨버거', '치즈버거']):
                    quantity = self.get_quantity()
                    self.process_order(menu, quantity)
                else:
                    print("주문할 햄버거가 아닙니다. 다시 말씀해주세요.")
                    speak("주문할 햄버거가 아닙니다. 다시 말씀해주세요.")
                    continue  # 주문이 아닌 경우 다시 음성 인식을 시도
            except sr.UnknownValueError:
                print("음성을 인식할 수 없습니다.")
                speak("음성을 인식할 수 없습니다. 다시 말씀해주세요.")
                continue  # 음성 인식 실패 시 다시 음성 인식을 시도
            except sr.RequestError as e:
                print("Google Speech Recognition에 오류가 발생했습니다:", e)
                speak("Google Speech Recognition에 오류가 발생했습니다.")
                continue  # 음성 인식 요청 오류 시 다시 음성 인식을 시도

            # 추가 주문 여부 확인
            while True:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    print("추가 주문을 원하시나요? (예/아니요)")
                    speak("추가 주문을 원하시나요?")
                    audio = recognizer.listen(source)

                try:
                    response = recognizer.recognize_google(audio, language="ko-KR")
                    print(response)
                    if any(keyword in response for keyword in ['네', '내', '예', '예스']):
                        break
                    elif any(keyword in response for keyword in ['아니요', '노']):
                        self.show_total_order()
                        self.show_total_price()
                        return
                    else:
                        print("다시 말씀해주세요.")
                        speak("다시 말씀해주세요.")
                except sr.UnknownValueError:
                    print("음성을 인식할 수 없습니다.")
                    speak("음성을 인식할 수 없습니다. 다시 말씀해주세요.")
                except sr.RequestError as e:
                    print("Google Speech Recognition에 오류가 발생했습니다:", e)
                    speak("Google Speech Recognition에 오류가 발생했습니다.")

    def get_quantity(self):
        while True:
            recognizer = sr.Recognizer()
            # 수량 선택
            with sr.Microphone() as source:
                speak("몇 개를 주문하시겠습니까?")
                print("몇 개를 주문하시겠습니까?")
                audio = recognizer.listen(source)

            try:
                quantity_text = recognizer.recognize_google(audio, language="ko-KR")
                print("인식된 텍스트:", quantity_text)
                quantity = self.parse_quantity(quantity_text)
                print("주문할 햄버거 수:", quantity)
                return quantity
            except sr.UnknownValueError:
                print("음성을 인식할 수 없습니다. 다시 말씀해주세요.")
                speak("음성을 인식할 수 없습니다. 다시 말씀해주세요.")
            except sr.RequestError as e:
                print("Google Speech Recognition에 오류가 발생했습니다:", e)
                speak("Google Speech Recognition에 오류가 발생했습니다.")

    def parse_quantity(self, quantity_text):
        print(quantity_text)
        if any(keyword in quantity_text for keyword in ['한', '하나']):
            return 1
        elif any(keyword in quantity_text for keyword in ['두', '둘']):
            return 2
        elif any(keyword in quantity_text for keyword in ['세', '삼', '새']):
            return 3
        elif any(keyword in quantity_text for keyword in ['네', '넷', '내']):
            return 4
        elif any(keyword in quantity_text for keyword in ['다섯', '오']):
            return 5
        else:
            words = quantity_text.split()
            for word in words:
                if word.isdigit():
                    return min(int(word), 5)
            return 1

    def process_order(self, menu, quantity):
        menu = menu.replace(" ", "")  # 메뉴명에서 공백 제거
        price_per_hamberger = self.drink_prices.get(menu)
        if price_per_hamberger is not None:
            total_price = price_per_hamberger * quantity
            self.orders[menu] = self.orders.get(menu, 0) + quantity
            print(f"{menu} {quantity}개 주문되었습니다. 가격은 {total_price}원 입니다.")
            speak(f"{menu} {quantity}개 주문되었습니다. 가격은 {total_price}원 입니다.")
            
            # 대화식 응답
            self.respond_to_order(menu, quantity)
        else:
            print("주문할 햄버거를 인식할 수 없거나 메뉴에 없습니다.")
            speak("주문할 햄버거를 인식할 수 없거나 메뉴에 없습니다.")

    def respond_to_order(self, menu, quantity):
        responses = [
            f"{menu} {quantity}개를 주문하셨습니다."
        ]
        response = random.choice(responses)
        print(response)
        speak(response)

    def show_total_order(self):
        print("주문한 햄버거 목록:")
        for menu, quantity in self.orders.items():
            print(f"{menu}: {quantity}개")
            speak(f"{menu}: {quantity}개")
            

    def show_total_price(self):
        total_price = sum(self.drink_prices[menu] * quantity for menu, quantity in self.orders.items())
        print(f"총 가격은 {total_price}원 입니다.")
        speak(f"총 가격은 {total_price}원 입니다.")

def main():
    kiosk = DrinkKiosk()
    kiosk.take_order()

if __name__ == "__main__":
    main()
