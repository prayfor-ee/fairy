import common as C
import apikey as API_KEY
import requesturl as REQUEST_URL

import requests
import json
import speech_recognition as SR #https://pypi.org/project/SpeechRecognition/2.1.3/

class STTManager:

    def __init__(self):
        pass

    def request_kakao(self, audio):
        """request kakao server (Speech to Text)

        Args:
            audio (bytes): speech data (raw_data(bytes) of voicerecognition)

        Returns:
            str, list: text from stt, nbest list of voicerecognition
        """
        text = ""
        nbestlist = []

        if API_KEY.REST_API_KEY == "":
            C.P("ERROR : REST_API_KEY is not exist.")
            return text

        headers = {
            "Content-Type": "application/octet-stream",
            "Authorization": "KakaoAK " + API_KEY.REST_API_KEY,
        }

        # kakao rest api url
        kakao_rest_api_url = REQUEST_URL.KAKAO_REST_API
        # requests kakao
        res = requests.post(kakao_rest_api_url, headers=headers, data=audio)
        #res_json_data = json.loads(res.text)
        if res.status_code == 200:
            #C.P(f"Full type [{type(res.text)}]")
            #C.P(f"Full response [{res.text}]")
            #print(f"result text [{res.text}]")
            start_position_for_split = res.text.index('{"type":"finalResult"')
            end_position_for_split = res.text.rindex('}')+1
            res_result = res.text[start_position_for_split:end_position_for_split]
            #C.P(f"result : {res_result}")
            text = json.loads(res_result).get("value")
            C.P(f"text : {text}")
            nbest = json.loads(res_result).get("nBest")
            #C.P(f"nbest list : {nbest}")
            data = sorted(nbest, reverse = True, key=(lambda nbest: nbest["score"]))
            for d in data:
                #C.P(f"d [{d}]")
                nbestlist.append(d["value"])

            #debug
            #for n in nbestlist:
            #   C.P(f"nbest : [{n}]")

            #C.P("result : ", res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1])
            #result = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}') + 1]
            #text = json.loads(result).get("value")
        else:   # != 200 error
            C.P("error! because ")#, res.json())

        return text, nbestlist

    def get_voice_recognition(self):
        """get raw_data(bytes) of voicerecognition
        """
        # 음성 데이터는 Mono channel, 16000 Hz samplerate, 16 bit depth인 RAW PCM 포맷만 지원합니다.
        recognizer = SR.Recognizer()    #speech
        microphone = SR.Microphone(sample_rate=16000) #set mic
        audio = None

        #mic noise
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            C.P("mic noise value {}".format(recognizer.energy_threshold))
            result = recognizer.listen(source)
            audio = result.get_raw_data()

        # 음성 수집
       # with microphone as source:
        #    print("Say something!")
        #    result = recognizer.listen(source)
        #    audio = result.get_raw_data()

        #try:
        #    C.P(f"I said [{recognizer.recognize(audio)}]")  # recognize speech using Google Speech Recognition
        #except LookupError:  # speech is unintelligible
        #    C.P("Could not understand audio")

        return audio