import common as C
import sttmanager as STT
import datamanager as DATA
if __name__ == '__main__':
    C.P('start')

    stt_manager = STT.STTManager()
    #audio = stt_manager.get_voice_recognition()
    #text = stt_manager.request_kakao(audio)
    #C.P(f"text [{text}]")

    data_manager = DATA.DataManager()
    data_manager.request_weather()

    C.P('end')
    del data_manager
    del stt_manager
