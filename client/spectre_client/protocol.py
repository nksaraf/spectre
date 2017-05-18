import subprocess
import base64

class ClientProtocolHandler():
    
    @staticmethod
    def handle_response(client, response):
        if 'audio' in response:
            with open('audio.mp3', 'w') as file:
                file.write(base64.b64decode(response["audio"]))
            subprocess.Popen(['mpg123', '-q', 'audio.mp3']).wait()
            