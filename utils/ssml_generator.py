import google.generativeai as genai
import re

def generate_ssml_from_notes(
    client: genai.GenerativeModel,
    model_name: str,
    notes: str,
    style_instruction: str
) -> str:
    """
    Uses a Gemini model to convert speaker notes and a style instruction
    into SSML (Speech Synthesis Markup Language).

    Args:
        client: The initialized Gemini API client.
        model_name: The name of the text generation model to use.
        notes: The raw text from the speaker notes.
        style_instruction: The user's instruction for the audio style
                           (e.g., "clear, enthusiastic teaching voice").

    Returns:
        A string containing the SSML markup.
    """
    prompt = f"""
    Based on the following style instruction, convert the speaker notes into SSML (Speech Synthesis Markup Language) for Google Cloud Text-to-Speech.

    **Style Instruction:** "{style_instruction}"

    **Speaker Notes:**
    ---
    {notes}
    ---

    **Rules:**
    1.  Wrap the entire output in `<speak>` tags.
    2.  Use SSML tags like `<break>`, `<emphasis>`, `<prosody>` (for rate, pitch, volume), and `<say-as>` to make the speech sound natural and match the style instruction.
    3.  Do NOT include any explanation, just the raw SSML code.
    4.  Ensure all special characters like '&', '<', '>' are properly escaped (e.g., use '&').

    **Example Output:**
    <speak>
        <prosody rate="medium">Here is the first point.</prosody>
        <break time="1s" />
        <emphasis level="strong">And here is an emphasized second point.</emphasis>
    </speak>

    **SSML Output:**
    """

    try:
        model = client.get_generative_model(model_name)
        response = model.generate_content(prompt)
        
        # Clean up the response to get only the SSML code block
        ssml_content = response.text
        match = re.search(r'<speak>.*</speak>', ssml_content, re.DOTALL)
        if match:
            return match.group(0)
        else:
            # If no <speak> tag is found, wrap the plain text as a fallback
            escaped_notes = notes.replace('&', '&').replace('<', '<').replace('>', '>')
            return f"<speak>{escaped_notes}</speak>"
            
    except Exception as e:
        print(f"An error occurred during SSML generation: {e}")
        # Fallback to basic SSML if the API fails
        escaped_notes = notes.replace('&', '&').replace('<', '<').replace('>', '>')
        return f"<speak>{escaped_notes}</speak>"
