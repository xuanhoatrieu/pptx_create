import streamlit as st
import os
import shutil
import time
import requests
from google import genai
from utils.pptx_creator import create_presentation
from utils.content_generator import generate_slide_content, generate_image_prompt
from utils.api_manager import get_gemini_client
from utils.gemini_image_generator import generate_image_with_gemini, generate_image_with_gemini_2_5
from utils.ssml_generator import generate_ssml_from_notes
from utils.tts_generator import generate_audio_from_ssml
from utils.gemini_tts_generator import generate_audio_with_gemini
from utils.vbee_tts_generator import generate_audio_with_vbee, get_vbee_personal_voices
import utils.auth as auth

# --- Initialize Auth ---
auth.setup_database()

# --- Constants ---
DEFAULT_TITLE_BG = "1.png"
DEFAULT_CONTENT_BG = "2.png"

# --- Data ---
CLOUD_TTS_VOICES = {
    "vi-VN": ["vi-VN-Neural2-A", "vi-VN-Neural2-D", "vi-VN-Wavenet-A", "vi-VN-Wavenet-B", "vi-VN-Wavenet-C", "vi-VN-Wavenet-D", "vi-VN-Standard-A", "vi-VN-Standard-B", "vi-VN-Standard-C", "vi-VN-Standard-D"],
    "en-US": ["en-US-Neural2-A", "en-US-Neural2-C", "en-US-Neural2-D", "en-US-Neural2-E", "en-US-Neural2-F", "en-US-Neural2-G", "en-US-Neural2-H", "en-US-Neural2-I", "en-US-Neural2-J"]
}
GEMINI_TTS_VOICES = {
    "Zephyr": "Nữ-Tươi sáng", "Puck": "Nam-Rộn ràng", "Charon": "Cung cấp nhiều thông tin", "Kore": "Chắc chắn", "Fenrir": "Dễ kích động", "Leda": "Trẻ trung", "Orus": "Chắc chắn", "Aoede": "Nhẹ nhàng", "Callirrhoe": "Dễ tính", "Autonoe": "Tươi sáng", "Enceladus": "Thì thầm", "Iapetus": "Rõ ràng", "Umbriel": "Dễ tính", "Algieba": "Mượt mà", "Despina": "Mượt mà", "Erinome": "Rõ ràng", "Algenib": "Trầm", "Rasalgethi": "Cung cấp nhiều thông tin", "Laomedeia": "Rộn ràng", "Achernar": "Mềm mại", "Alnilam": "Chắc chắn", "Schedar": "Đều đặn", "Gacrux": "Trưởng thành", "Pulcherrima": "Chuyển tiếp", "Achird": "Thân thiện", "Zubenelgenubi": "Bình thường", "Vindemiatrix": "Dịu dàng", "Sadachbia": "Sôi nổi", "Sadaltager": "Hiểu biết", "Sulafat": "Ấm áp"
}
KNOWN_PERSONAL_VOICES = {
    "Giọng - Triệu Hòa": "n_thainguyen_male_giangbaitrieuhoa_education_vc"
}

# --- Helper Functions ---
# def parse_markdown(md_content):
#     slides = []
#     for slide_block in md_content.strip().split("**Slide"):
#         if not slide_block.strip(): continue
#         lines = [line.strip() for line in slide_block.strip().split("\n") if line.strip()]
#         if not lines: continue
#         slide_data = {}
#         full_title_line = lines.pop(0)
#         for line in lines:
#             if line.startswith('* **Title:**'): slide_data['title'] = line.replace('* **Title:**', '').strip()
#             elif line.startswith('* **Subtitle:**'): slide_data['subtitle'] = line.replace('* **Subtitle:**', '').strip()
#             elif line.startswith('* **Content:**'):
#                 idx = lines.index(line)
#                 slide_data['content'] = "\n".join([l.lstrip("* ").strip() for l in lines[idx+1:] if l.strip().startswith("*")])
#             elif line.startswith('* **[Visual Idea]:**'): slide_data['visual_idea'] = line.replace('* **[Visual Idea]:**', '').strip()
#             elif line.startswith('* **[Speaker Notes]:**'): slide_data['notes'] = line.replace('* **[Speaker Notes]:**', '').strip()
#         if not slide_data.get('title'): slide_data['title'] = full_title_line.split(':', 1)[-1].replace('**','').strip()
#         if slide_data: slides.append(slide_data)
#     return slides

def parse_markdown(md_content):
    slides = []
    # Tách file thành các khối slide dựa trên từ khóa "**Slide"
    raw_slides = md_content.strip().split("**Slide")

    for slide_block in raw_slides:
        if not slide_block.strip():
            continue

        lines = slide_block.strip().split("\n")
        # Khởi tạo dữ liệu slide rỗng
        slide_data = {
            "title": "",
            "subtitle": "",
            "content": "",
            "visual_idea": "",
            "notes": ""
        }
        
        current_section = None # Biến trạng thái để biết đang đọc mục nào

        # Lấy tiêu đề dự phòng từ dòng đầu tiên (VD: "1: Title Slide")
        if lines:
            first_line = lines[0].strip()
            if ":" in first_line:
                slide_data['title'] = first_line.split(':', 1)[-1].replace('**', '').strip()

        for line in lines:
            line = line.strip()
            if not line: continue

            # --- 1. Kiểm tra xem dòng này có bắt đầu một mục mới không ---
            if line.startswith('* **Title:**'):
                slide_data['title'] = line.replace('* **Title:**', '').strip()
                current_section = "title"
            elif line.startswith('* **Subtitle:**'):
                slide_data['subtitle'] = line.replace('* **Subtitle:**', '').strip()
                current_section = "subtitle"
            elif line.startswith('* **Content:**'):
                current_section = "content"
                # Không lấy nội dung trên dòng này vì Content thường xuống dòng
            elif line.startswith('* **[Visual Idea]:**'):
                slide_data['visual_idea'] = line.replace('* **[Visual Idea]:**', '').strip()
                current_section = "visual_idea"
            elif line.startswith('* **[Speaker Notes]:**'):
                # Lấy nội dung ngay trên dòng (nếu có) và xóa dấu ngoặc kép thừa nếu cần
                initial_note = line.replace('* **[Speaker Notes]:**', '').strip()
                slide_data['notes'] = initial_note
                current_section = "notes"
            
            # --- 2. Nếu không phải mục mới, thì nối vào mục hiện tại (Xử lý xuống dòng) ---
            else:
                if current_section == "content":
                    # Với Content, giữ nguyên xuống dòng để phân tách các ý
                    slide_data["content"] += "\n" + line
                elif current_section == "notes":
                    # Với Notes, nối thêm vào chuỗi cũ, thêm dấu cách
                    # Xóa dấu " ở đầu dòng nếu do format cũ để lại
                    clean_line = line.replace('"', '') 
                    slide_data["notes"] += " " + clean_line
                elif current_section == "visual_idea":
                    slide_data["visual_idea"] += " " + line

        # --- 3. Làm sạch dữ liệu lần cuối ---
        slide_data['content'] = slide_data['content'].strip()
        # Xóa dấu ngoặc kép bao quanh notes nếu có (do format của bạn hay dùng "...")
        slide_data['notes'] = slide_data['notes'].strip().strip('"')

        if slide_data['title']: # Chỉ thêm slide nếu có tiêu đề
            slides.append(slide_data)

    return slides

# --- Main App Function ---
def main_app():
    st.sidebar.header(f"Xin chào, {st.session_state['username']}!")
    
    # --- API Key Management ---
    api_key = auth.get_api_key(st.session_state['username'])
    vbee_token, vbee_app_id = auth.get_vbee_credentials(st.session_state['username'])

    with st.sidebar.expander("Quản lý API Keys"):
        new_api_key = st.text_input("Nhập Google API Key:", value=api_key or "", type="password")
        if st.button("Lưu Google Key"):
            if new_api_key:
                auth.save_api_key(st.session_state['username'], new_api_key)
                st.success("Đã lưu Google API Key!")
                st.rerun()
            else:
                st.warning("Vui lòng nhập Google API Key.")

        st.markdown("---")
        
        new_vbee_token = st.text_input("Nhập Vbee Token:", value=vbee_token or "", type="password")
        new_vbee_app_id = st.text_input("Nhập Vbee App ID:", value=vbee_app_id or "")
        if st.button("Lưu Vbee Credentials"):
            if new_vbee_token and new_vbee_app_id:
                auth.save_vbee_credentials(st.session_state['username'], new_vbee_token, new_vbee_app_id)
                st.success("Đã lưu thông tin Vbee!")
                st.rerun()
            else:
                st.warning("Vui lòng nhập đầy đủ Vbee Token và App ID.")

    if st.sidebar.button("Đăng xuất"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.rerun()

    # --- Sidebar Configuration ---
    st.sidebar.header("Cấu hình chung")
    
    genai_client, text_models, image_models = None, [], []
    if api_key and "YOUR_API_KEY" not in api_key:
        try:
            genai_client = get_gemini_client(api_key)
            text_models = [m.name for m in genai_client.list_models() if "generateContent" in m.supported_generation_methods] or ["gemini-2.5-flash", "gemini-pro"]
            image_models = ["models/imagen-3.0-generate-002", "models/imagen-3.0-generate-003", "gemini-2.5-flash-image", "models/imagen-4.0-generate-001"]
        except Exception as e:
            st.sidebar.error(f"API Key không hợp lệ hoặc có lỗi: {e}")
    else:
        st.sidebar.warning("Vui lòng cung cấp một Gemini API Key hợp lệ.")

    st.sidebar.subheader("Cài đặt Sinh nội dung & Hình ảnh")
    default_text_model_name = "gemini-2.5-flash"
    try:
        default_text_index = text_models.index(default_text_model_name)
    except ValueError:
        default_text_index = 0
    text_model_name = st.sidebar.selectbox(
        "Chọn mô hình sinh văn bản:", 
        text_models, 
        index=default_text_index, 
        disabled=not genai_client
    )
    image_model_name = st.sidebar.selectbox("Chọn mô hình sinh ảnh:", image_models, disabled=not genai_client)

    st.sidebar.subheader("Cài đặt Âm thanh (Text-to-Speech)")
    tts_enabled = st.sidebar.checkbox("Bật tính năng chuyển văn bản thành giọng nói", value=True)
    tts_service = st.sidebar.selectbox(
        "Chọn dịch vụ TTS:",
        ["Google AI Studio (Gemini)", "Google Cloud TTS", "Vbee TTS"],
        disabled=not tts_enabled
    )
    tts_style_instruction = st.sidebar.text_area(
        "Chỉ dẫn phong cách âm thanh:",
        "Giọng đọc truyền cảm, rõ ràng, tốc độ vừa phải, nhấn mạnh vào các thuật ngữ kỹ thuật quan trọng.",
        disabled=not tts_enabled
    )

    if tts_service == "Google Cloud TTS":
        lang_options = {"Tiếng Việt (vi-VN)": "vi-VN", "Tiếng Anh (en-US)": "en-US"}
        selected_lang_name = st.sidebar.selectbox("Chọn ngôn ngữ:", list(lang_options.keys()), disabled=not tts_enabled)
        selected_lang_code = lang_options[selected_lang_name]
        tts_voice_name = st.sidebar.selectbox("Chọn giọng đọc (Cloud):", CLOUD_TTS_VOICES[selected_lang_code], disabled=not tts_enabled)
    elif tts_service == "Vbee TTS":
        # Bắt đầu với danh sách giọng đọc đã biết
        combined_voices = KNOWN_PERSONAL_VOICES.copy()

        if not vbee_token or not vbee_app_id:
            st.sidebar.warning("Vui lòng nhập và lưu Vbee Token & App ID để tải thêm giọng đọc.")
        else:
            # Tải danh sách giọng đọc cá nhân từ API và hợp nhất chúng
            with st.spinner("Đang tải danh sách giọng đọc Vbee..."):
                api_voices = get_vbee_personal_voices(vbee_token)
                combined_voices.update(api_voices) # Hợp nhất, ghi đè nếu có khóa trùng lặp
        
        if not combined_voices:
            st.sidebar.info("Không có giọng đọc cá nhân nào.")
            tts_voice_name = None
        else:
            # Sắp xếp danh sách giọng đọc theo tên để hiển thị nhất quán
            sorted_voice_names = sorted(combined_voices.keys())
            selected_vbee_voice_name = st.sidebar.selectbox(
                "Chọn giọng đọc cá nhân (Vbee):", 
                sorted_voice_names, 
                disabled=not (tts_enabled and vbee_token and vbee_app_id)
            )
            tts_voice_name = combined_voices.get(selected_vbee_voice_name)

    else: # Gemini TTS
        gemini_tts_model = st.sidebar.selectbox(
            "Chọn mô hình TTS (Gemini):",
            ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"],
            disabled=not tts_enabled
        )
        gemini_voice_display = {f'{k} ({v})': k for k, v in GEMINI_TTS_VOICES.items()}
        selected_gemini_voice_display = st.sidebar.selectbox("Chọn giọng đọc (Gemini):", list(gemini_voice_display.keys()), disabled=not tts_enabled)
        tts_voice_name = gemini_voice_display[selected_gemini_voice_display]

    # --- Main App Logic ---
    tab1, tab2, tab3 = st.tabs(["Tạo bài giảng đầy đủ", "Công cụ tạo ảnh", "Công cụ tạo âm thanh"])

    with tab1:
        st.header("1. Tải lên file Markdown của bạn")
        uploaded_file = st.file_uploader("Chọn một file .md", type=["md", "slide.md"], key="uploader_tab1")

        if uploaded_file is not None:
            try:
                base_name = os.path.splitext(uploaded_file.name)[0].replace('.slide','')
                output_dir = os.path.join(os.getcwd(), base_name)
                output_pptx_path = os.path.join(output_dir, f"{base_name}.pptx")
                st.info(f"Kết quả sẽ được lưu tại: {output_dir}")
                markdown_text = uploaded_file.getvalue().decode("utf-8")
                st.text_area("Nội dung Markdown", markdown_text, height=250)
                slides_data = parse_markdown(markdown_text)

                generation_mode = st.selectbox(
                    "Chọn chế độ tạo:",
                    ("Tạo bài giảng đầy đủ", "Chỉ tạo âm thanh", "Chỉ tạo ảnh"),
                    key="generation_mode_tab1"
                )

                if st.button(f"Bắt đầu: {generation_mode}", key="generate_presentation_tab1"):
                    if not genai_client:
                        st.error("Không thể tạo. Vui lòng cung cấp API Key hợp lệ.")
                        st.stop()

                    if os.path.exists(output_dir): shutil.rmtree(output_dir)
                    os.makedirs(os.path.join(output_dir, "images"))
                    if tts_enabled: os.makedirs(os.path.join(output_dir, "audio"))

                    progress_bar = st.progress(0)
                    processed_slides = []
                    image_prompts_list = []
                    st.subheader("Tiến trình tạo Slide")
                    for i, slide in enumerate(slides_data):
                        progress_bar.progress((i + 1) / len(slides_data))
                        
                        with st.expander(f"Slide {i+1}: {slide.get('title', 'Không có tiêu đề')}", expanded=True):
                            st.write("--- Bắt đầu xử lý ---")
                            
                            with st.spinner("Đang tối ưu hóa nội dung..."):
                                optimized_content = generate_slide_content(genai_client, text_model_name, slide.get("title", ""), slide.get("content", ""))
                                st.success("Tối ưu hóa nội dung thành công.")

                            image_path = None
                            if generation_mode != "Chỉ tạo âm thanh" and "visual_idea" in slide and i >= 2:
                                with st.spinner("Đang tạo ảnh..."):
                                    image_prompt = generate_image_prompt(genai_client, text_model_name, slide["visual_idea"])
                                    image_prompts_list.append(f"Slide {i+1}: {image_prompt}\n")
                                    image_path = os.path.join(output_dir, "images", f"slide_{i+1}.png")
                                    success = False
                                    if "gemini-2.5-flash-image" in image_model_name:
                                        success = generate_image_with_gemini_2_5(api_key, image_model_name, image_prompt, image_path)
                                    else:
                                        success = generate_image_with_gemini(api_key, image_model_name, image_prompt, image_path)

                                    if not success:
                                        shutil.copy(DEFAULT_CONTENT_BG, image_path)
                                        st.warning("Không thể tạo ảnh, đã sử dụng ảnh mặc định.")
                                    else:
                                        st.success("Tạo ảnh thành công.")
                                st.image(image_path, caption=f"Ảnh cho Slide {i+1}")

                            audio_path = None
                            if generation_mode != "Chỉ tạo ảnh" and tts_enabled and "notes" in slide and slide["notes"]:
                                with st.spinner(f"Đang tạo âm thanh bằng {tts_service}..."):
                                    if tts_service == "Google Cloud TTS":
                                        audio_path = os.path.join(output_dir, "audio", f"slide_{i+1}.mp3")
                                        ssml_text = generate_ssml_from_notes(genai_client, text_model_name, slide["notes"], tts_style_instruction)
                                        success = generate_audio_from_ssml(api_key, ssml_text, audio_path, tts_voice_name, selected_lang_code)
                                    elif tts_service == "Vbee TTS":
                                        audio_path = os.path.join(output_dir, "audio", f"slide_{i+1}.mp3")
                                        text_to_speak = slide["notes"]
                                        success = generate_audio_with_vbee(vbee_token, vbee_app_id, text_to_speak, tts_voice_name, audio_path)
                                    else: # Gemini TTS
                                        audio_path = os.path.join(output_dir, "audio", f"slide_{i+1}.wav")
                                        text_to_speak = slide["notes"]
                                        success = generate_audio_with_gemini(api_key, gemini_tts_model, tts_voice_name, text_to_speak, audio_path)
                                    
                                    if success:
                                        st.success("Tạo âm thanh thành công.")
                                        st.audio(audio_path)
                                    else:
                                        audio_path = None
                                        st.warning("Không thể tạo âm thanh.")

                            processed_slides.append({
                                "title": optimized_content.get("title"), "subtitle": slide.get("subtitle"),
                                "bullets": optimized_content.get("bullets"), "notes": slide.get("notes"),
                                "image_path": image_path, "audio_path": audio_path
                            })
                            st.write("--- Hoàn thành xử lý Slide ---")

                    if image_prompts_list:
                        prompts_file_path = os.path.join(output_dir, f"{base_name}_image_prompts.txt")
                        with open(prompts_file_path, "w", encoding="utf-8") as f:
                            f.write("\n".join(image_prompts_list))
                        st.info(f"Đã lưu các prompt tạo ảnh vào: {prompts_file_path}")

                    with st.spinner("Đang tạo file PowerPoint..."):
                        create_presentation(output_pptx_path, processed_slides, DEFAULT_TITLE_BG, DEFAULT_CONTENT_BG)
                    
                    st.success("Tạo bài giảng thành công!")
                    
                    archive_path_base = os.path.join(os.getcwd(), f"{base_name}_lecture_package")
                    archive_path_zip = shutil.make_archive(archive_path_base, 'zip', output_dir)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        with open(output_pptx_path, "rb") as f:
                            st.download_button(
                                label=f"Tải về {os.path.basename(output_pptx_path)}",
                                data=f.read(),
                                file_name=f"{base_name}.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                key="download_pptx_tab1"
                            )
                    with col2:
                        with open(archive_path_zip, "rb") as f:
                            st.download_button(
                                label="Tải về toàn bộ bài giảng (.zip)",
                                data=f.read(),
                                file_name=f"{base_name}_lecture_package.zip",
                                mime="application/zip",
                                key="download_zip_tab1"
                            )

            except Exception as e:
                st.error(f"Đã xảy ra lỗi không mong muốn trong Tab 1: {e}")
                import traceback
                st.error(traceback.format_exc())

    with tab2:
        st.header("Công cụ tạo ảnh riêng lẻ")
        image_prompt_text = st.text_area("Nhập ý tưởng hình ảnh (Visual Idea):", key="image_prompt_tab2")
        
        if st.button("Tạo ảnh", key="create_image_tab2"):
            if not genai_client or not image_prompt_text:
                st.warning("Vui lòng cung cấp API Key và nhập ý tưởng hình ảnh.")
            else:
                with st.spinner("Đang tạo ảnh..."):
                    single_images_dir = os.path.join(os.getcwd(), "single_images")
                    os.makedirs(single_images_dir, exist_ok=True)
                    timestamp = int(time.time())
                    output_image_path = os.path.join(single_images_dir, f"image_{timestamp}.png")
                    final_prompt = generate_image_prompt(genai_client, text_model_name, image_prompt_text)
                    success = False
                    if "gemini-2.5-flash-image" in image_model_name:
                        success = generate_image_with_gemini_2_5(api_key, image_model_name, final_prompt, output_image_path)
                    else:
                        success = generate_image_with_gemini(api_key, image_model_name, final_prompt, output_image_path)

                    if success:
                        st.success("Tạo ảnh thành công!")
                        st.image(output_image_path)
                        with open(output_image_path, "rb") as f:
                            st.download_button("Tải ảnh về", f.read(), os.path.basename(output_image_path), key="download_image_tab2")
                    else:
                        st.error("Tạo ảnh thất bại.")

    with tab3:
        st.header("Công cụ tạo âm thanh riêng lẻ")
        text_to_speak_tab3 = st.text_area("Nhập văn bản cần chuyển thành giọng nói:", key="text_to_speak_tab3")

        if st.button("Tạo âm thanh", key="create_audio_tab3"):
            if not genai_client or not text_to_speak_tab3:
                st.warning("Vui lòng cung cấp API Key và nhập văn bản.")
            else:
                with st.spinner(f"Đang tạo âm thanh bằng {tts_service}..."):
                    single_audio_dir = os.path.join(os.getcwd(), "single_audio")
                    os.makedirs(single_audio_dir, exist_ok=True)
                    timestamp = int(time.time())
                    
                    success = False
                    if tts_service == "Google Cloud TTS":
                        output_audio_path = os.path.join(single_audio_dir, f"audio_{timestamp}.mp3")
                        ssml_text = generate_ssml_from_notes(genai_client, text_model_name, text_to_speak_tab3, tts_style_instruction)
                        success = generate_audio_from_ssml(api_key, ssml_text, output_audio_path, tts_voice_name, selected_lang_code)
                    elif tts_service == "Vbee TTS":
                        if not vbee_token or not vbee_app_id:
                            st.error("Vui lòng cung cấp và lưu thông tin Vbee trước khi tạo âm thanh.")
                            st.stop()
                        output_audio_path = os.path.join(single_audio_dir, f"audio_{timestamp}.mp3")
                        success = generate_audio_with_vbee(vbee_token, vbee_app_id, text_to_speak_tab3, tts_voice_name, output_audio_path)
                    else: # Gemini TTS
                        output_audio_path = os.path.join(single_audio_dir, f"audio_{timestamp}.wav")
                        success = generate_audio_with_gemini(api_key, gemini_tts_model, tts_voice_name, text_to_speak_tab3, output_audio_path)

                    if success:
                        st.success("Tạo âm thanh thành công!")
                        st.audio(output_audio_path)
                        with open(output_audio_path, "rb") as f:
                            st.download_button("Tải âm thanh về", f.read(), os.path.basename(output_audio_path), key="download_audio_tab3")
                    else:
                        st.error("Tạo âm thanh thất bại.")

# --- Streamlit UI ---
st.set_page_config(page_title="PPTX Generator", layout="wide")
st.title("Tự động hóa Tạo PPTX từ Markdown")

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# --- Login/Register UI ---
if not st.session_state['logged_in']:
    st.header("Chào mừng đến với Trình tạo PPTX")
    st.write("Vui lòng đăng nhập để tiếp tục, hoặc đăng ký nếu bạn chưa có tài khoản.")

    col1, col2 = st.columns(2)

    with col1:
        with st.form("login_form"):
            st.subheader("Đăng nhập")
            login_username = st.text_input("Tên đăng nhập", key="login_user")
            login_password = st.text_input("Mật khẩu", type="password", key="login_pass")
            login_submitted = st.form_submit_button("Đăng nhập")
            if login_submitted:
                if auth.verify_user(login_username, login_password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = login_username
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không đúng.")

    with col2:
        with st.form("register_form"):
            st.subheader("Đăng ký")
            reg_username = st.text_input("Tên đăng nhập mới", key="reg_user")
            reg_password = st.text_input("Mật khẩu mới", type="password", key="reg_pass")
            reg_submitted = st.form_submit_button("Đăng ký")
            if reg_submitted:
                if reg_username and reg_password:
                    if auth.add_user(reg_username, reg_password):
                        st.success("Đăng ký thành công! Vui lòng đăng nhập.")
                    else:
                        st.error("Tên đăng nhập đã tồn tại.")
                else:
                    st.warning("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
else:
    main_app()
