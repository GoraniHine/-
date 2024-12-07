from pydub import AudioSegment
from pydub.playback import play
import io
from google.cloud import texttospeech

# 인증된 서비스 계정의 키 파일 경로
credentials_file_path = "/home/minschoi/ttspeak-425308-a6418acbe631.json"

# TTS를 생성할 텍스트
input_text = "김규민 바보 븅신 새끼 저녁 뭐 먹을래 섹스!."

# TTS 출력 파일 경로
output_file_path = "output.mp3"

# Text-to-Speech 클라이언트 생성
client = texttospeech.TextToSpeechClient.from_service_account_json(credentials_file_path)

# TTS 입력 설정
synthesis_input = texttospeech.SynthesisInput(text=input_text)

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

# TTS 결과를 파일로 저장
with open(output_file_path, "wb") as out:
    out.write(response.audio_content)

print(f"TTS 생성이 완료되었습니다. 출력 파일: {output_file_path}")

# MP3 파일을 재생
audio = AudioSegment.from_file(output_file_path, format="mp3")
play(audio)

