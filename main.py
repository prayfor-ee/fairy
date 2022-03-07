import common as C
import sttmanager as STT

if __name__ == '__main__':
    C.P('start')

    stt_manager = STT.STTManager()
    audio = stt_manager.get_voice_recognition()
    text = stt_manager.request_kakao(audio)
    C.P(f"text [{text}]")

    C.P('end')
