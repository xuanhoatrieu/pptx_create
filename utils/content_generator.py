
import json
import time
from google.api_core import exceptions as google_exceptions

PROMPT_THIET_KE_SLIDE = """
Bạn là một chuyên gia Thiết kế Nội dung Giảng dạy (Instructional Designer) với nhiệm vụ biên soạn nội dung cho các bài giảng đại học. Tôi sẽ cung cấp cho bạn một dàn ý thô cho một slide.
**Nhiệm vụ của bạn là:** Chuyển hóa dàn ý đó thành nội dung slide hấp dẫn, chuyên nghiệp và dễ hiểu cho sinh viên, tuân thủ nghiêm ngặt các quy tắc sau:
1.  **Đối tượng:** Sinh viên đại học. Nội dung cần có chiều sâu chuyên môn nhưng phải được diễn giải một cách dễ tiếp cận.
2.  **Mục tiêu:** Tối ưu hóa để giữ sự tập trung, khuyến khích tư duy và giúp sinh viên ghi nhớ kiến thức cốt lõi.
3.  **Tiêu đề:** Giữ nguyên tiêu đề `{title}` được cung cấp.
4.  **Xử lý Nội dung:**
    * **Quy tắc Vàng (Ưu tiên số 1):** Nếu nội dung là một **định nghĩa, khái niệm cốt lõi, hoặc một trích dẫn trực tiếp** (ví dụ: có các từ 'là', 'được định nghĩa là', 'bao gồm',...), **BẠN PHẢI GIỮ NGUYÊN VĂN VÀ ĐẦY ĐỦ** nội dung đó trong phần "description". Các trường "emoji" và "point" phải để trống.
    * **Với các nội dung khác:** Phân tách thành các luận điểm rõ ràng. Mỗi luận điểm phải bao gồm:
        * **"emoji":** Chọn một biểu tượng emoji **tinh tế, mang tính học thuật** và liên quan trực tiếp đến nội dung. Tránh các emoji quá trẻ con hoặc gây xao nhãng.
        * **"point":** Rút ra **từ khóa (keyword) hoặc cụm từ cốt lõi** quan trọng nhất. Đây phải là thứ mà sinh viên cần ghi vào vở. Phải thật ngắn gọn.
        * **"description":** Diễn giải ngắn gọn (dưới 15 từ) cho "point". Sử dụng ngôn ngữ rõ ràng, có thể dùng phép ẩn dụ hoặc ví dụ đơn giản để sinh viên dễ hình dung.

5.  **Định dạng đầu ra:** Chỉ trả về một đối tượng JSON duy nhất, không thêm bất kỳ lời giải thích hay định dạng markdown nào khác.
**Dàn ý thô:**
---
**Tiêu đề:** {title}
**Nội dung:**
{content}
---
**Cấu trúc JSON đầu ra bắt buộc:**
{{
  "title": "Tiêu đề Slide",
  "bullets": [
    {{
      "emoji": "💡",
      "point": "Từ khóa hoặc ý chính 1",
      "description": "Diễn giải cực kỳ ngắn gọn, dễ hiểu cho sinh viên."
    }},
    {{
      "emoji": "📈",
      "point": "Từ khóa hoặc ý chính 2",
      "description": "Diễn giải cực kỳ ngắn gọn, dễ hiểu cho sinh viên."
    }},
    {{
      "emoji": "",
      "point": "",
      "description": "Giữ nguyên đầy đủ định nghĩa hoặc khái niệm cốt lõi ở đây."
    }}
  ]
}}
"""

PROMPT_TAO_ANH = """
You are a master Art Director specializing in writing prompts for image generation AI. Your task is to expand a simple visual idea into a detailed, descriptive prompt in English.

The prompt must be structured to maximize image quality and adhere to user requests, especially regarding text.

**Instructions:**
1.  **Core Concept:** Develop the user's '{visual_idea}'.
2.  **Detailed Description:** Include the main subject, the background/setting, mood, and atmosphere.
3.  **Artistic Style:** Specify a style (e.g., photorealistic, cinematic, 3D render, oil painting).
4.  **Lighting & Color:** Describe the lighting (e.g., cinematic lighting, soft morning light, neon glow) and the color palette.
5.  **Text Control (Crucial):**
    * **The final image must be completely free of any text, letters, numbers, or characters.**
    * Add a strong negative prompt section at the end, like: `--no text, typography, letters, words, numbers, signature, watermark`. This is a common syntax for telling the AI what to avoid.

**Visual Idea:**
---
{visual_idea}
---
Return ONLY the complete English prompt, ready for the image generation model.
"""

PROMPT_TAO_ANH = """
You are an expert Educational Art Director specialized in creating visuals for lecture slides.

Your task is to create a clear, accurate, and visually consistent image that illustrates the following concept:
---
{visual_idea}
---

### 🔹 Purpose
Create an **educational illustration** (not abstract art) that directly visualizes the described idea for teaching programming.

### 🔹 Visual Style
- Prefer: *flat 2D infographic*, *diagram*, *minimalist educational style*.
- For code or syntax: use *IDE-style windows*, *syntax highlighting*, *indentation marks*, and *language-appropriate icons*.
- For conceptual ideas: use *clear icons*, *logical layout*, and *color grouping*.
- For real-world metaphors: use *simple realistic scenes* (e.g., computer, classroom, network diagram).

### 🔹 Text Handling
- **Do NOT include any text** unless it is *essential* to understanding the concept.
- If text genuinely helps clarify meaning (e.g., showing "Python" vs "Java", "Hello, World!", or short code labels), include it clearly.
- Limit to **1–2 short words or phrases**, ≤25 characters each.
- Use simple fonts (sans-serif or monospace).
- Avoid decorative typography.

Examples when text is allowed:
- Comparing languages → "Python" / "Java"
- Showing output → "Hello, World!"
- Slide summary → "Lesson Summary"

In all other cases: **no text, just icons or visuals.**

### 🔹 Lighting & Color
- Soft classroom lighting, neutral background.
- Color palette: clear contrast, educational tone (blue, orange, gray, white).

### 🔹 Avoid
--no watermark, --no handwriting, --no distorted text, --no abstract shapes, --no glowing cubes, --no sci-fi, --no cinematic lighting
--no text in the picture unless essential as described above.
"""

def generate_slide_content(client, model_name, title, content):
    """Generates optimized slide content using the Gemini API with retry logic."""
    prompt = PROMPT_THIET_KE_SLIDE.format(title=title, content=content)
    model = client.GenerativeModel(model_name)
    
    retries = 3
    delay = 5  # seconds
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_response)
        except google_exceptions.InternalServerError as e:
            print(f"Attempt {attempt + 1} failed with internal server error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error decoding JSON from response: {e}")
            try:
                print(f"Raw response: {response.text}")
            except (NameError, AttributeError):
                print("Could not get raw response text.")
            # Return a default structure in case of JSON error, no retry needed.
            return {"title": title, "bullets": [{"point": "", "description": content}]}

    print("Failed to generate slide content after several retries.")
    # Return a default structure if all retries fail
    return {"title": title, "bullets": [{"point": "", "description": content}]}

def generate_image_prompt(client, model_name, visual_idea):
    """Generates a detailed image prompt from a visual idea with retry logic."""
    prompt = PROMPT_TAO_ANH.format(visual_idea=visual_idea)
    model = client.GenerativeModel(model_name)
    
    retries = 3
    delay = 5  # seconds
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except google_exceptions.InternalServerError as e:
            print(f"Attempt {attempt + 1} failed with internal server error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            
    print("Failed to generate image prompt after several retries.")
    return f"Error: Failed to generate prompt for '{visual_idea}'"
