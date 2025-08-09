from google.cloud import texttospeech
from google.api_core.client_options import ClientOptions

def generate_audio_from_ssml(
    api_key: str,
    ssml_text: str,
    output_path: str,
    voice_name: str = "vi-VN-Wavenet-D",
    language_code: str = "vi-VN"
):
    """
    Generates an audio file from SSML text using Google Cloud Text-to-Speech.

    Args:
        api_key: The Google API Key to use for authentication.
        ssml_text: The SSML formatted string to synthesize.
        output_path: The path to save the generated MP3 audio file.
        voice_name: The name of the voice to use (e.g., "vi-VN-Wavenet-D").
        language_code: The language code (e.g., "vi-VN").
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        # Use the API key for authentication
        client_options = ClientOptions(api_key=api_key)
        client = texttospeech.TextToSpeechClient(client_options=client_options)

        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        print(f"Synthesizing speech for: {output_path}")
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            print(f"Audio content written to file {output_path}")
        
        return True

    except Exception as e:
        print(f"An error occurred during Text-to-Speech synthesis: {e}")
        import traceback
        traceback.print_exc()
        return False
