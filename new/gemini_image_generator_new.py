from google import genai
import os
from google.genai import types

def generate_image_with_gemini(api_key: str, model_name: str, prompt: str, output_path: str, aspect_ratio: str = "4:3") -> bool:
    """
    Generates an image using a Google AI Studio Imagen model.

    Args:
        api_key: The Google AI Studio API key.
        model_name: The name of the Imagen model to use (e.g., 'models/imagen-3.0-generate-002').
        prompt: The text prompt for image generation.
        output_path: The path to save the generated image.
        aspect_ratio: The desired aspect ratio (e.g., "16:9", "1:1", "9:16", "3:4", "4:3").

    Returns:
        True if image generation is successful, False otherwise.
    """
    print(f"--- Initializing Gemini Client for Image Generation ---")
    print(f"Using model: {model_name}")

    try:
        client = genai.Client(api_key=api_key)

        print(f"Generating image with prompt: {prompt}")
        
        config = dict(
            number_of_images=1,
            output_mime_type="image/jpeg",
            person_generation="ALLOW_ADULT",
            aspect_ratio=aspect_ratio,
        )

        response = client.models.generate_images(
            model=model_name,
            prompt=prompt,
            config=config,
        )

        if response.generated_images:
            # The generated_image object directly has a save method
            response.generated_images[0].image.save(output_path)
            print(f"Successfully generated and saved image to {output_path}")
            return True
        else:
            print("Image generation failed: The API response did not contain any images.")
            return False

    except Exception as e:
        print(f"An error occurred during Gemini image generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_image_with_gemini_2_5(api_key: str, model_name: str, prompt: str, output_path: str) -> bool:
    """
    Generates an image using the Gemini 2.5 Flash Image model by mirroring the exact
    API call method from the official Google AI Studio code sample.

    Args:
        api_key: The Google AI Studio API key.
        model_name: The name of the Gemini model (e.g., 'gemini-2.5-flash-image').
        prompt: The text prompt for image generation.
        output_path: The path to save the generated image.

    Returns:
        True if image generation is successful, False otherwise.
    """
    print(f"--- ✅ Final Attempt: Aligning with AI Studio Exact API Call ---")
    print(f"Using model: {model_name}")

    try:
        client = genai.Client(api_key=api_key)
        
        print(f"Generating image with prompt: {prompt}")

        contents_payload = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            )
        ]
        
        generate_content_config = types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        )

        # *** ĐÂY LÀ THAY ĐỔI QUAN TRỌNG NHẤT ***
        # Gọi trực tiếp client.models.generate_content_stream thay vì model.generate_content
        # và truyền model_name như một tham số.
        stream = client.models.generate_content_stream(
            model=model_name,
            contents=contents_payload,
            config=generate_content_config,
        )

        image_found = False
        # Vòng lặp xử lý stream giữ nguyên vì đã chính xác
        for chunk in stream:
            if (chunk.candidates 
                and chunk.candidates[0].content 
                and chunk.candidates[0].content.parts
                and chunk.candidates[0].content.parts[0].inline_data):
                
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                image_data = inline_data.data
                
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                print(f"✅ Successfully generated and saved image to {output_path}")
                image_found = True
                break
        
        if not image_found:
             print("❌ Image generation failed: No image data found in the response stream.")
        
        return image_found

    except Exception as e:
        print(f"❌ An error occurred during Gemini 2.5 streaming image generation: {e}")
        import traceback
        traceback.print_exc()
        return False