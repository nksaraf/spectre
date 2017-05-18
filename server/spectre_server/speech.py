import gtts
import io
import base64

def audio(text):
	spoken= gtts.gTTS(text, lang='en-uk', slow=False)
	spoken.save('voice.mp3')
	st = ''
	with open('voice.mp3', 'r') as file:
		st = file.read()
	return base64.b64encode(st)