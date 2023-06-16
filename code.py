

## Code to use selenium and Auto-click Google Captcha using Speech to text

!pip install torch
!pip install transformers
!pip install datasets
!pip install torch
!pip install transformers
!pip install datasets
!pip install transformers==4.28.1 soundfile sentencepiece torchaudio pydub
from transformers import *
import torch
import soundfile as sf
# import librosa
import os
import torchaudio
from bs4 import BeautifulSoup

device = "cuda:0" if torch.cuda.is_available() else "cpu"

def load_model():

    wav2vec2_model_name = "facebook/wav2vec2-base-960h" # 360MB
    wav2vec2_processor = Wav2Vec2Processor.from_pretrained(wav2vec2_model_name)
    wav2vec2_model = Wav2Vec2ForCTC.from_pretrained(wav2vec2_model_name).to(device)
    return wav2vec2_processor,wav2vec2_model
wav2vec2_processor,wav2vec2_model=load_model()
fetch_url='https://kcmohrd.mwdbe.com/FrontEnd/SearchCertifiedDirectory.asp?XID=4600&TN=kcmohrd'

# fetch_url='https://ny.newnycontracts.com/FrontEnd/searchcertifieddirectory.asp'
# fetch_url='https://columbus.diversitycompliance.com/FrontEnd/searchcertifieddirectory.asp'


def beauty(driver):
    text=driver.page_source
    return BeautifulSoup(text, "html.parser")

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
options = webdriver.ChromeOptions() 
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
driver.get(fetch_url)

#https://stackoverflow.com/questions/65813792/recaptcha-download-audio-file
time.sleep(5)
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))

time.sleep(5)
recaptche=driver.find_elements(By.XPATH, "//span[@id='recaptcha-anchor']")
recaptche[0].send_keys("\n")
time.sleep(5)

driver.switch_to.default_content()
time.sleep(5)

WebDriverWait(driver, 20).until(
    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")))
#driver.refresh()
time.sleep(10)

button=driver.find_elements(By.XPATH, "//button[@id='recaptcha-audio-button']")
button[0].click()

time.sleep(10)
src = driver.find_element(By.CLASS_NAME,"rc-audiochallenge-tdownload-link").get_attribute("href")
print(src)

import requests
import wave

c=1
path="C:/Users/skyatham/Downloads/test"+str(c)+".mp3"
with open(path, 'wb') as a:
    resp = requests.get(src)
    if resp.status_code == 200:
        a.write(resp.content)
        print('downloaded')
    else:
        print(resp.reason)
        exit(1)
c=c+1

def load_audio(audio_path):
    """Load the audio file & convert to 16,000 sampling rate"""
  # load our wav file
    speech, sr = torchaudio.load(audio_path)
    resampler = torchaudio.transforms.Resample(sr, 16000)
    speech = resampler(speech[1])
    return speech.squeeze()
 
def get_transcription_wav2vec2(audio_path, model, processor):
    speech = load_audio(audio_path)
    input_features = processor(speech, return_tensors="pt", sampling_rate=16000)["input_values"].to(device)
    # perform inference
    logits = model(input_features)["logits"]
    # use argmax to get the predicted IDs
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    return transcription.lower()

text=get_transcription_wav2vec2(path, 
                           wav2vec2_model, 
                           wav2vec2_processor)
print(text)

answer=driver.find_elements(By.XPATH,"//input[@id='audio-response']")
answer[0].send_keys(text)

verify=driver.find_elements(By.XPATH,"//button[@id='recaptcha-verify-button']")
verify[0].click()
time.sleep(5)
driver.switch_to.default_content()

#beauty(driver)
time.sleep(10)
Download_Button=driver.find_elements(By.XPATH,"//input[@id='ButtonDownloadEntireDirectory']")
Download_Button[0].click()

time.sleep(5)
ButtonDownloadtoCSV=driver.find_elements(By.XPATH,"//input[@id='ButtonDownloadtoCSV']")
ButtonDownloadtoCSV[0].click()
