
import subprocess,sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'transformers','torch','soundfile','torchaudio','selenium','pytest'])
from transformers import *
import torch
import soundfile as sf
import pathlib
import os
import torchaudio
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
device = "cuda:0" if torch.cuda.is_available() else "cpu"




def load_model():

    wav2vec2_model_name = "facebook/wav2vec2-base-960h" # 360MB
    wav2vec2_processor = Wav2Vec2Processor.from_pretrained(wav2vec2_model_name)
    wav2vec2_model = Wav2Vec2ForCTC.from_pretrained(wav2vec2_model_name).to(device)
    return wav2vec2_processor,wav2vec2_model

def execute_captcha(driver):
    driver.refresh()
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
    
    time.sleep(2)
    recaptche=driver.find_elements(By.XPATH, "//span[@id='recaptcha-anchor']")
    recaptche[0].send_keys("\n")
    
    time.sleep(2)
    driver.switch_to.default_content()
    
    time.sleep(2)
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")))

    time.sleep(2)

    button=driver.find_elements(By.XPATH, "//button[@id='recaptcha-audio-button']")
    time.sleep(2)
    button[0].click()
    
    time.sleep(3)
    if driver.find_elements(By.XPATH,"//div[@class='rc-doscaptcha-body-text']"):
        execute_captcha(driver)

    time.sleep(3)
    src = driver.find_element(By.CLASS_NAME,"rc-audiochallenge-tdownload-link").get_attribute("href")
    print(src)
    
    return driver,src
    
def Save_audio(Audio_Dir,src):

    path=str(Audio_Dir)+"\\test"+str(datetime.now().strftime("%Y-%m-%d-%I_%M_%p"))+".mp3"
    with open(path, 'wb') as a:
        resp = requests.get(src)
        if resp.status_code == 200:
            a.write(resp.content)
            print('downloaded')
        else:
            print(resp.reason)
            exit(1)

    return path


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
    print (transcription)
    return transcription.lower()


def submit_response(driver,text):

    answer=driver.find_elements(By.XPATH,"//input[@id='audio-response']")
    answer[0].send_keys(text)
    time.sleep(3)
    verify=driver.find_elements(By.XPATH,"//button[@id='recaptcha-verify-button']")
    verify[0].click()
    time.sleep(5)
    driver.switch_to.default_content()
    Submit_button=driver.find_elements(By.XPATH,"//button[@type='submit']")
    Submit_button[0].click()
    
    time.sleep(60)
    
    return driver


def Recaptcha(fetch_url):
    wav2vec2_processor,wav2vec2_model=load_model()
    options = webdriver.ChromeOptions() 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
    driver.get(fetch_url)
    
    driver,src=execute_captcha(driver)
    
    Data_path=str(os.getcwd())+"\\Audio_Data\\"
    Audio_Dir = pathlib.Path(os.getcwd(), Data_path)
    Audio_Dir.mkdir(parents=True, exist_ok=True)  
    path=Save_audio(Audio_Dir,src)
    text=get_transcription_wav2vec2(path, wav2vec2_model,wav2vec2_processor)
    driver=submit_response(driver,text)
    driver.close()


if __name__ == "__main__":
    fetch_url='https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox-explicit.php'
    Recaptcha(fetch_url)
