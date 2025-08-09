# Dự án Tự động hóa Tạo PPTX từ Markdown

## Tính năng chính

- **Quản lý API Key an toàn:** Cho phép lưu trữ nhiều Google API Key trong file `.streamlit/secrets.toml` dưới các tên định danh (profile) như "Giáo viên A", "Giáo viên B".
- **Lựa chọn Profile:** Người dùng có thể dễ dàng chuyển đổi giữa các API key bằng cách chọn profile từ danh sách thả xuống.
- **Tải lên file Markdown:** Cho phép người dùng tải lên một file `.md` chứa nội dung cho các slide.
- **Lựa chọn mô hình động:** Tự động tải và hiển thị danh sách các mô hình sinh văn bản và sinh ảnh tương thích với API key của profile được chọn.
- **Tối ưu hóa nội dung thông minh:**
    - Tự động tinh chỉnh tiêu đề slide cho hấp dẫn và ngắn gọn.
    - Phân tích nội dung, chuyển đổi các ý thành các điểm chính có **biểu tượng (emoji)** và mô tả cực ngắn gọn.
    - Giữ nguyên các nội dung là định nghĩa hoặc khái niệm.
- **Tạo prompt cho ảnh:** Dựa vào thẻ `[Visual Idea]` trong Markdown, hệ thống tự động tạo ra một prompt chi tiết bằng tiếng Anh để sinh ảnh.
- **Sinh ảnh bằng Gemini:** Sử dụng mô hình tạo ảnh được người dùng lựa chọn (ví dụ: `imagen-3.0`) để sinh ảnh trực tiếp từ prompt đã tạo, thông qua thư viện `google-genai`.
- **Chuyển văn bản thành giọng nói (Text-to-Speech) - Hỗ trợ song song:**
    - Cung cấp lựa chọn giữa hai dịch vụ TTS: **Google Cloud TTS** và **Google AI Studio (Gemini)**.
    - **Với Google Cloud TTS:**
        - Sử dụng mô hình Gemini để phân tích "Chỉ dẫn phong cách" và chuyển đổi ghi chú thành mã **SSML (Speech Synthesis Markup Language)**, giúp kiểm soát chi tiết ngữ điệu, nhịp độ.
        - Hỗ trợ các giọng đọc Wavenet và Neural2.
    - **Với Google AI Studio (Gemini):**
        - Kết hợp trực tiếp "Chỉ dẫn phong cách" và nội dung ghi chú để mô hình Gemini TTS tự diễn giải và tạo ra giọng đọc tự nhiên.
        - Hỗ trợ các mô hình `tts-001`, `tts-002` và các giọng đọc chuyên biệt của Gemini.
    - Giao diện tự động thay đổi để hiển thị các tùy chọn phù hợp với dịch vụ được chọn.
- **Tạo bản trình bày PowerPoint:** Tự động tạo một file `.pptx` hoàn chỉnh với nội dung đã được tối ưu, hình ảnh đã được sinh ra và **âm thanh thuyết minh được chèn sẵn**.
- **Tải xuống:** Cung cấp nút để người dùng tải về file `.pptx` đã hoàn thành.

## Luồng hoạt động của dự án

1.  **Khởi động và Cấu hình (`app.py`):
    - Ứng dụng đọc file `.streamlit/secrets.toml` để lấy danh sách các profile và API key tương ứng.
    - Giao diện hiển thị một danh sách thả xuống để người dùng chọn một profile.

2.  **Tải mô hình (`app.py`):
    - Dựa trên API key của profile được chọn, ứng dụng kết nối đến Google và lấy danh sách các mô hình tạo văn bản và tạo ảnh có sẵn.
    - Hai danh sách thả xuống khác được hiển thị để người dùng chọn mô hình cụ thể cho văn bản và hình ảnh.

3.  **Tải lên và Phân tích Markdown (`app.py`):
    - Người dùng tải lên một file Markdown.
    - Hàm `parse_markdown` đọc file và chia nội dung thành một danh sách các đối tượng slide (tiêu đề, nội dung, ý tưởng hình ảnh, ghi chú).

4.  **Vòng lặp xử lý từng Slide (`app.py`):
    - Hệ thống duyệt qua từng slide.
    - **Tối ưu hóa nội dung (`utils/content_generator.py`):**
        - Gọi hàm `generate_slide_content` để gửi tiêu đề và nội dung thô đến mô hình Gemini văn bản đã chọn.
        - API trả về một cấu trúc JSON với tiêu đề đã tối ưu và nội dung được chia thành các điểm có emoji, tiêu đề điểm và mô tả ngắn gọn.
    - **Sinh ảnh (`utils/gemini_image_generator.py`):**
        - Nếu slide có `visual_idea`, hàm `generate_image_prompt` được gọi để tạo prompt chi tiết.
        - Sau đó, hàm `generate_image_with_gemini` được gọi, truyền vào đó **mô hình tạo ảnh đã chọn** và prompt để sinh ra hình ảnh.
    - **Sinh âm thanh từ Ghi chú (Lựa chọn kép):**
        - Người dùng chọn dịch vụ TTS mong muốn (`Google Cloud TTS` hoặc `Google AI Studio`).
        - **Nếu chọn Google Cloud TTS:** Hệ thống sẽ chạy luồng `utils/ssml_generator.py` -> `utils/tts_generator.py` để tạo âm thanh từ SSML.
        - **Nếu chọn Google AI Studio:** Hệ thống sẽ chạy luồng mới qua `utils/gemini_tts_generator.py`, gửi thẳng văn bản và chỉ dẫn phong cách đến API Gemini TTS.

5.  **Tạo file PowerPoint (`utils/pptx_creator.py`):
    - Sau khi xử lý tất cả các slide, hàm `create_presentation` được gọi.
    - Hàm này sử dụng thư viện `python-pptx` để tạo bản trình bày, chèn nội dung đã được định dạng, hình ảnh đã sinh ra và **file âm thanh thuyết minh** vào từng slide tương ứng.

6.  **Hoàn thành và Tải xuống (`app.py`):
    - File `.pptx` được lưu vào thư mục output.
    - Giao diện hiển thị thông báo thành công và một nút để người dùng tải file về máy.

## Ý tưởng phát triển trong tương lai

- **Xem trước kết quả tức thì:**
    - Hiển thị hình ảnh (`st.image`) và trình phát âm thanh (`st.audio`) cho mỗi slide ngay sau khi chúng được tạo, thay vì đợi đến cuối quy trình. Điều này cung cấp phản hồi trực quan ngay lập tức cho người dùng.

- **Tái cấu trúc thành bộ công cụ đa năng:**
    - Chuyển đổi giao diện sang sử dụng các tab (`st.tabs`) để tách biệt các chức năng:
        - **Tab 1: Tạo bài giảng đầy đủ:** Giữ nguyên luồng hoạt động cốt lõi.
        - **Tab 2: Công cụ tạo ảnh:** Một giao diện độc lập để nhập ý tưởng và tạo ra một hình ảnh duy nhất.
        - **Tab 3: Công cụ tạo âm thanh:** Một giao diện độc lập để nhập văn bản và tạo ra một tệp âm thanh duy nhất.

- **Tăng cường tính linh hoạt của quy trình:**
    - Thêm các nút hoặc tùy chọn để chạy các phần cụ thể của quy trình tạo bài giảng, ví dụ:
        - Một nút để "Chỉ tạo âm thanh cho tất cả các slide".
        - Một nút để "Chỉ tạo prompt ảnh và hình ảnh".
