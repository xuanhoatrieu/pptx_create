import requests
import base64
import os
import wave

def write_wav(path, audio_bytes, rate=24000):
    """Writes the audio bytes to a WAV file."""
    try:
        with wave.open(path, "wb") as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(rate)
            wf.writeframes(audio_bytes)
        print(f"Successfully wrote WAV file to {path}")
        return True
    except Exception as e:
        print(f"Error writing WAV file: {e}")
        return False

def generate_audio_with_gemini(
    api_key: str,
    model_name: str,
    voice_name: str,
    text_to_speak: str,
    output_path: str
) -> bool:
    """
    Generates an audio file using the Gemini REST API and saves it as a properly
    formatted WAV file.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{"text": text_to_speak}]
        }],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice_name
                    }
                }
            }
        }
    }

    print(f"--- Calling Gemini TTS (generateContent) REST API ---")
    print(f"Model: {model_name}, Voice: {voice_name}")

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

        if response_json.get("candidates") and \
           response_json["candidates"][0].get("content") and \
           response_json["candidates"][0]["content"].get("parts") and \
           response_json["candidates"][0]["content"]["parts"][0].get("inlineData"):
            
            audio_data_base64 = response_json["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
            audio_content_bytes = base64.b64decode(audio_data_base64)
            
            wav_output_path = os.path.splitext(output_path)[0] + ".wav"
            
            # Write the bytes to a correctly formatted WAV file
            if write_wav(wav_output_path, audio_content_bytes):
                return True
            else:
                # Fallback to writing raw bytes if wave fails, for debugging
                print("Fallback: Writing raw bytes to file.")
                with open(wav_output_path, "wb") as out:
                    out.write(audio_content_bytes)
                return False
        else:
            print(f"TTS generation failed. Unexpected response format: {response_json}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        if e.response is not None:
            print(f"Response body: {e.response.text}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False
