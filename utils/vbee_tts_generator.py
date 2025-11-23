import requests
import time

VBEE_TTS_ENDPOINT = "https://vbee.vn/api/v1/tts"
VBEE_VOICES_ENDPOINT = "https://vbee.vn/api/v1/voices"

def get_vbee_personal_voices(token: str) -> dict:
    """
    Fetches the list of available voices from Vbee and filters for personal voices.
    Returns a dictionary mapping voice names to voice codes.
    """
    headers = {"Authorization": f"Bearer {token}"}
    personal_voices = {}

    print("--- Fetching Vbee personal voices ---")
    try:
        response = requests.get(VBEE_VOICES_ENDPOINT, headers=headers)
        response.raise_for_status()
        response_json = response.json()

        if response_json.get("status") == 1 and "result" in response_json:
            # The result is a dictionary where keys are voice codes and values are voice details
            all_voices_dict = response_json["result"]
            for voice_code, voice_details in all_voices_dict.items():
                # Check if voice_details is a dictionary and has the 'voice_ownership' key
                if isinstance(voice_details, dict) and voice_details.get("voice_ownership") == "PERSONAL":
                    display_name = voice_details.get("name", voice_code)
                    personal_voices[display_name] = voice_code # Use the key as the voice_code
            print(f"Found {len(personal_voices)} personal voices.")
        else:
            print(f"Vbee Voices Error: Could not fetch voices. {response_json}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the Vbee voices API request: {e}")
        if e.response is not None:
            print(f"Response body: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching Vbee voices: {e}")
        
    return personal_voices


def generate_audio_with_vbee(
    token: str,
    app_id: str,
    text_to_speak: str,
    voice_name: str,
    output_path: str,
    audio_type: str = "mp3"
) -> bool:
    """
    Generates an audio file using the Vbee asynchronous TTS REST API by polling.
    """
    
    post_headers = {
        "Authorization": f"Bearer {token}", #
        "Content-Type": "application/json"
    }

    payload = {
        "app_id": app_id, #
        "input_text": text_to_speak, #
        "voice_code": voice_name, #
        "audio_type": audio_type, #
        "response_type": "indirect", #
        "callback_url": "https://example.com/dummy_callback", # Bắt buộc, nhưng chúng ta sẽ không dùng
        "speed_rate": 1.0 #
    }

    print(f"--- Calling Vbee TTS (Step 1: POST Request) ---")
    print(f"Voice: {voice_name}")

    try:
        # --- Bước 1: Gửi yêu cầu POST để bắt đầu tạo audio ---
        response = requests.post(VBEE_TTS_ENDPOINT, headers=post_headers, json=payload)
        response.raise_for_status()
        response_json = response.json()

        if response_json.get("status") == 1 and response_json.get("result"):
            request_id = response_json["result"].get("request_id") #
            if not request_id:
                print(f"Vbee TTS Error: POST request successful but no 'request_id'. {response_json}")
                return False
            print(f"Vbee TTS: Received request_id: {request_id}")
        else:
            print(f"Vbee TTS Error: POST request failed. {response_json}")
            return False

        # --- Bước 2: Poll bằng GET để kiểm tra trạng thái ---
        get_headers = {"Authorization": f"Bearer {token}"} #
        get_url = f"{VBEE_TTS_ENDPOINT}/{request_id}" #
        
        # Poll tối đa 30 giây (15 lần x 2 giây)
        for _ in range(15):
            print("Polling Vbee status...")
            get_response = requests.get(get_url, headers=get_headers)
            get_response.raise_for_status()
            get_json = get_response.json()
            
            if get_json.get("status") != 1 or not get_json.get("result"):
                print(f"Vbee TTS Error: GET poll failed. {get_json}")
                return False

            result_status = get_json["result"].get("status")
            print(f"Vbee TTS Status: {result_status}")

            if result_status == "SUCCESS": #
                audio_link = get_json["result"].get("audio_link") #
                if not audio_link:
                    print(f"Vbee TTS Error: Status is SUCCESS but no 'audio_link'. {get_json}")
                    return False
                
                print(f"Vbee TTS: SUCCESS. Downloading from {audio_link}")
                
                # --- Bước 3: Tải file audio ---
                audio_data = requests.get(audio_link)
                audio_data.raise_for_status()
                
                with open(output_path, "wb") as out:
                    out.write(audio_data.content)
                print(f"Successfully wrote Vbee audio file to {output_path}")
                return True
                
            elif result_status == "FAILURE": #
                print(f"Vbee TTS Error: Audio generation failed. {get_json}")
                return False
            
            # Nếu là "IN_PROGRESS" hoặc trạng thái khác, đợi 2 giây rồi thử lại
            time.sleep(2)

        print("Vbee TTS Error: Request timed out after 30 seconds.")
        return False

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the Vbee API request: {e}")
        if e.response is not None:
            print(f"Response body: {e.response.text}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
