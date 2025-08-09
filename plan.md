Dự án: Tự động hóa Tạo pptx từ Markdown với Gemini
1. Tổng quan và Mục tiêu Dự án
Dự án này xây dựng một hệ thống tự động hóa sử dụng Google Apps Script để đọc nội dung từ một file văn bản có cấu trúc (Markdown), sau đó tự động tạo ra một bài trình bày pttx hoàn chỉnh.

Mục tiêu chính:
Tiết kiệm thời gian: Giảm thiểu tối đa thời gian và công sức tạo slide thủ công.
Tăng cường trí tuệ nhân tạo: Tận dụng sức mạnh của Gemini API để làm phong phú nội dung, hình ảnh và tối ưu hóa bố cục.
Đảm bảo tính nhất quán: Tạo ra các bài trình bày chuyên nghiệp, đồng bộ về mặt thiết kế và định dạng.
Tập trung vào nội dung: Cho phép người dùng chỉ cần tập trung vào việc soạn thảo nội dung trong Markdown, hệ thống sẽ lo phần còn lại.
2. Các Tính năng Nổi bật
Hệ thống được trang bị các tính năng thông minh và tự động hóa mạnh mẽ:
- Lựa chọn được API và model ở giao diện (các API được thêm trước)
- Phân tích Markdown: Tự động đọc và phân tích cấu trúc file .md để bóc tách các thành phần của từng slide (Tiêu đề, Phụ đề, Nội dung, Ghi chú cho diễn giả, Ý tưởng hình ảnh).
- Tạo Slide tự động: Dựng các slide trong pttx tương ứng với dữ liệu đã phân tích.
- Tùy chỉnh Ảnh nền: Khả năng sử dụng các ảnh nền khác nhau cho slide tiêu đề và các slide nội dung.
- Xử lý Ghi chú (Speaker Notes): Tự động chèn nội dung trong [Speaker Notes] vào phần ghi chú của slide tương ứng.
- Xử lý Hình ảnh Thông minh: Sinh  hình ảnh thật dựa trên mô tả trong [Visual Idea] bằng AI hệ thống tự động dùng mô hình sinh ảnh của Google để tạo ra một hình ảnh độc đáo từ chính mô tả đó.
- Quản lý ảnh: Các hình ảnh được tìm/tạo ra sẽ được lưu trữ trong một thư mục image để dễ dàng quản lý với cấu trúc tên là “Slide#.png”.
- Lựa chọn Bố cục (Layout) Thông minh: Hệ thống tự phân tích lượng văn bản, số gạch đầu dòng và sự hiện diện của hình ảnh để chọn ra layout phù hợp nhất từ các layout có sẵn trong theme của pttx.
Ví dụ: Tự động chọn layout 2 cột khi có cả văn bản và hình ảnh, hoặc layout chỉ có tiêu đề cho các slide phân mục.
Định dạng Chuyên nghiệp:
- Tự động áp dụng các quy tắc định dạng về font chữ, kích thước, màu sắc để đảm bảo tính nhất quán và chuyên nghiệp.
Title slide (slide 1) uses '1.png' as background with white text.
All content slides (from slide 2 onwards) use '2.png' as background.
For content slides:
Title: centered, 36px font size, white color.
Level 1 content: 32px font size, color '#3A664D'.
Level 2 content: 28px font size, color '#3A664D'.
Có khả năng yêu cầu Gemini tóm tắt hoặc định dạng lại văn bản dài cho phù hợp với không gian của slide.
Slide Nội dung bài học để mẫu sẵn, đầu đề mục đánh số thứ tự từ 1 đến hết
3. Luồng Hoạt động của Hệ thống
Đầu vào: Người dùng chuẩn bị file Markdown với cấu trúc định sẵn và các file ảnh nền.
Khởi chạy Script: Người dùng chạy hàm chính trong Google Apps Script.
Phân tích (Parsing): Script đọc và phân tích toàn bộ nội dung Markdown, chuyển nó thành một danh sách các đối tượng (mỗi đối tượng là một slide).
Tối ưu hóa nội dung:
Dựa vào các thông tin của slide bao gồm: **Slide 15: **, * **Title:**, * **Content:**, * **[Visual Idea]:** để dùng gemini tối ưu hóa nội dung trình bày cho slide. yêu cầu Có tiêu đề slide, tiêu đề nội dung có mô tả ngắn gọn, rõ ràng. Phần này có thể gọi prompt tạo nội dung:
PROMPT_THIET_KE_SLIDE = """
Bạn là một chuyên gia thiết kế nội dung thuyết trình (Instructional Designer). Tôi sẽ cung cấp cho bạn một outline thô cho một slide.
Nhiệm vụ của bạn là tinh chỉnh nó thành nội dung hiệu quả để trình bày, tuân thủ các quy tắc sau:
1. **Tối ưu hóa Tiêu đề:** Giữ lại ý chính nhưng làm cho tiêu đề ngắn gọn và hấp dẫn hơn.
2. **Xử lý Nội dung:**
\* \*\*Nếu nội dung là một khái niệm hoặc định nghĩa (ví dụ: có các từ 'là một', 'được định nghĩa là', v.v.), HÃY GIỮ NGUYÊN VÀ ĐẦY ĐỦ nội dung đó\*\* trong phần "description" và để trống phần "point".

\* Với các nội dung khác, hãy chia thành các ý chính. Mỗi ý bao gồm một "point" (ý chính, từ khóa) và một "description" (mô tả rất ngắn gọn, tường minh cho ý chính đó).

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

  "point": "Tên nội dung chính 1 (từ khóa)",

  "description": "Mô tả rất ngắn gọn cho nội dung 1."

}},

{{

  "point": "Tên nội dung chính 2 (từ khóa)",

  "description": "Mô tả rất ngắn gọn cho nội dung 2."

}},

{{

  "point": "",

  "description": "Giữ nguyên đầy đủ một khái niệm hoặc định nghĩa ở đây."

}}

]
}}
"""
Dựa vào các thông tin * **[Visual Idea]:** để tìm kiếm ảnh, nếu không tìm được ảnh phù hợp thì tạo prompt tạo ảnh dựa vào thông tin này với prompt:
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
Các ảnh tìm được lưu vào thư mục định sẵn trên drive, nếu không tìm được ảnh thì sinh ảnh mới. tất cả được lưu lại với cấu trúc tên là số thứ tự slide .png
Xử lý từng Slide (Vòng lặp):
a. Phân tích nội dung slide: Từ kế quả của 4.1 thì Đánh giá số lượng chữ, số dòng, sự tồn tại của hình ảnh...
b. Chọn Layout: Dựa trên phân tích, chọn layout phù hợp nhất.
c. Tạo Slide: Tạo một slide mới với layout đã chọn.
d. Thêm Nội dung: Chèn Tiêu đề, Nội dung, và Ghi chú diễn giả.
e. Đặt Nền: Áp dụng ảnh nền tương ứng.
f. Chèn ảnh được lưu ở thư mục: chèn ảnh vào slide và căn chỉnh.
g. Định dạng: Áp dụng các style chữ viết đã được định nghĩa.
Đầu ra: Một file pttx hoàn chỉnh, chuyên nghiệp, sẵn sàng để sử dụng.

Struction of project
.streamlit/secrets.toml
/pttx_create
├── .streamlit/
│   └── secrets.toml         # File quản lý tất cả API keys
├── utils/
│   ├── __init__.py          # File trống để Python nhận diện module
│   ├── api_manager.py       # Module quản lý API
│   ├── content_generator.py # Module tạo prompt và nội dung
│   └── pptx_creator.py      # Module tạo file PowerPoint
├── temp_images/             # Thư mục tạm chứa ảnh (sẽ tự tạo)
├── app.py                   # File chính để chạy Streamlit (đã được rút gọn)
├── 1.jpg                    # Ảnh nền
└── 2.png                    # Ảnh nền
└── Bai01/
    ├── images/
    └── bai01.pptx
    └── promt_create_image.txt


Create a beautiful, highly interactive web app for my partner, an
English speaker, to learn French.
- Track her daily progress.
. Use a highly engaging theme.
- Include a variety of activities (e.g., flashcards, quizzes, etc.).

One activity should be a snake-style game in which the snake is
replaced by a mouse and the apples are replaced by cheese. Each
time the mouse eats a piece of cheese, play a voice-over that
introduces a new French word so she can practice pronunciation
while playing Make it controllable with the arrow keys.

Think before answering. Render everything in canvas.