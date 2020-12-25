import time
import pyttsx3
WAITING_SEC = 3
engine = pyttsx3.init()
engine.say('开始听写，每隔' + str(WAITING_SEC) +'秒听写下一个')
i = 1
with open('wordsOfGrade3.txt', 'r', encoding='gb18030', errors='ignore') as f:
    for line in f:
        engine.say('第' + str(i) +'个词：' + line)
        i+=1
        engine.runAndWait()
        time.sleep(WAITING_SEC)
engine.say('听写完毕, Break a leg!')
engine.runAndWait()
engine.stop()



