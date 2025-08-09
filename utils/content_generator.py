
import json

PROMPT_THIET_KE_SLIDE = """
Bạn là một chuyên gia thiết kế nội dung thuyết trình (Instructional Designer). Tôi sẽ cung cấp cho bạn một outline thô cho một slide.
Nhiệm vụ của bạn là tinh chỉnh nó thành nội dung hiệu quả để trình bày, tuân thủ các quy tắc sau:
1. **Tối ưu hóa Tiêu đề:** Giữ lại ý chính nhưng làm cho tiêu đề ngắn gọn, hấp dẫn và chuyên nghiệp.
2. **Xử lý Nội dung:**
   * **Nếu nội dung là một khái niệm hoặc định nghĩa (ví dụ: có các từ 'là một', 'được định nghĩa là', v.v.), HÃY GIỮ NGUYÊN VÀ ĐẦY ĐỦ nội dung đó** trong phần "description" và để trống "point" và "emoji".
   * Với các nội dung khác, hãy chia thành các ý chính. Mỗi ý phải bao gồm:
     - **"emoji":** Một biểu tượng emoji duy nhất, phù hợp với nội dung của ý đó.
     - **"point":** Ý chính hoặc từ khóa, thật ngắn gọn.
     - **"description":** Mô tả cực kỳ ngắn gọn (dưới 10 từ) để làm rõ cho "point".
3. **Định dạng đầu ra:** Trả về kết quả dưới dạng một đối tượng JSON duy nhất, không có bất kỳ văn bản giải thích nào khác.

Dưới đây là outline thô:
---
**Tiêu đề:** {title}
**Nội dung:**
{content}
---
Cấu trúc JSON đầu ra bắt buộc:
{{
  "title": "Tiêu đề đã được tối ưu hóa",
  "bullets": [
    {{
      "emoji": "💡",
      "point": "Tên nội dung chính 1",
      "description": "Mô tả cực kỳ ngắn gọn cho nội dung 1."
    }},
    {{
      "emoji": "🚀",
      "point": "Tên nội dung chính 2",
      "description": "Mô tả cực kỳ ngắn gọn cho nội dung 2."
    }},
    {{
      "emoji": "",
      "point": "",
      "description": "Giữ nguyên đầy đủ một khái niệm hoặc định nghĩa ở đây."
    }}
  ]
}}
"""

PROMPT_TAO_ANH = """
Bạn là một Art Director chuyên viết prompt cho AI tạo ảnh. Tôi sẽ cung cấp một ý tưởng hình ảnh đơn giản.
Nhiệm vụ của bạn là phát triển ý tưởng đó thành một prompt chi tiết, giàu mô tả bằng tiếng Anh.
Prompt phải bao gồm: Chủ thể, bối cảnh, phong cách (ví dụ: minimalist icon, 3D render, photorealistic), ánh sáng, và màu sắc.
Dưới đây là ý tưởng hình ảnh:
---
**Visual Idea:** {visual_idea}
---
Hãy trả về duy nhất một chuỗi prompt hoàn chỉnh bằng tiếng Anh.
"""

def generate_slide_content(client, model_name, title, content):
    """Generates optimized slide content using the Gemini API."""
    prompt = PROMPT_THIET_KE_SLIDE.format(title=title, content=content)
    model = client.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    
    try:
        # The response might be in a markdown code block
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error decoding JSON from response: {e}")
        print(f"Raw response: {response.text}")
        # Return a default structure in case of error
        return {"title": title, "bullets": [{"point": "", "description": content}]}

def generate_image_prompt(client, model_name, visual_idea):
    """Generates a detailed image prompt from a visual idea."""
    prompt = PROMPT_TAO_ANH.format(visual_idea=visual_idea)
    model = client.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text.strip()
