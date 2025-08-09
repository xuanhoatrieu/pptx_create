import streamlit as st
import os
import shutil
import toml
import time
from google import genai
from utils.pptx_creator import create_presentation
from utils.content_generator import generate_slide_content, generate_image_prompt
from utils.api_manager import get_gemini_client
from utils.gemini_image_generator import generate_image_with_gemini
from utils.ssml_generator import generate_ssml_from_notes
from utils.tts_generator import generate_audio_from_ssml
from utils.gemini_tts_generator import generate_audio_with_gemini

# --- Constants ---
DEFAULT_TITLE_BG = "1.png"
DEFAULT_CONTENT_BG = "2.png"
SECRETS_PATH = os.path.join(".streamlit", "secrets.toml")

# --- Data ---
CLOUD_TTS_VOICES = {
    "vi-VN": ["vi-VN-Neural2-A", "vi-VN-Neural2-D", "vi-VN-Wavenet-A", "vi-VN-Wavenet-B", "vi-VN-Wavenet-C", "vi-VN-Wavenet-D", "vi-VN-Standard-A", "vi-VN-Standard-B", "vi-VN-Standard-C", "vi-VN-Standard-D"],
    "en-US": ["en-US-Neural2-A", "en-US-Neural2-C", "en-US-Neural2-D", "en-US-Neural2-E", "en-US-Neural2-F", "en-US-Neural2-G", "en-US-Neural2-H", "en-US-Neural2-I", "en-US-Neural2-J"]
}
GEMINI_TTS_VOICES = {
    "Zephyr": "Nữ-Tươi sáng", "Puck": "Nam-Rộn ràng", "Charon": "Cung cấp nhiều thông tin", "Kore": "Chắc chắn", "Fenrir": "Dễ kích động", "Leda": "Trẻ trung", "Orus": "Chắc chắn", "Aoede": "Nhẹ nhàng", "Callirrhoe": "Dễ tính", "Autonoe": "Tươi sáng", "Enceladus": "Thì thầm", "Iapetus": "Rõ ràng", "Umbriel": "Dễ tính", "Algieba": "Mượt mà", "Despina": "Mượt mà", "Erinome": "Rõ ràng", "Algenib": "Trầm", "Rasalgethi": "Cung cấp nhiều thông tin", "Laomedeia": "Rộn ràng", "Achernar": "Mềm mại", "Alnilam": "Chắc chắn", "Schedar": "Đều đặn", "Gacrux": "Trưởng thành", "Pulcherrima": "Chuyển tiếp", "Achird": "Thân thiện", "Zubenelgenubi": "Bình thường", "Vindemiatrix": "Dịu dàng", "Sadachbia": "Sôi nổi", "Sadaltager": "Hiểu biết", "Sulafat": "Ấm áp"
}

# --- Helper Functions ---
def load_api_keys():
    try:
        secrets = toml.load(SECRETS_PATH)
        return secrets.get("api_keys", {})
    except FileNotFoundError:
        return {}
    except Exception as e:
        st.error(f"Error loading secrets.toml: {e}")
        return {}

def parse_markdown(md_content):
    slides = []
    for slide_block in md_content.strip().split("**Slide"):
        if not slide_block.strip(): continue
        lines = [line.strip() for line in slide_block.strip().split("\n") if line.strip()]
        if not lines: continue
        slide_data = {}
        full_title_line = lines.pop(0)
        for line in lines:
            if line.startswith('* **Title:**'): slide_data['title'] = line.replace('* **Title:**', '').strip()
            elif line.startswith('* **Subtitle:**'): slide_data['subtitle'] = line.replace('* **Subtitle:**', '').strip()
            elif line.startswith('* **Content:**'):
                idx = lines.index(line)
                slide_data['content'] = "\n".join([l.lstrip("* ").strip() for l in lines[idx+1:] if l.strip().startswith("*")])
            elif line.startswith('* **[Visual Idea]:**'): slide_data['visual_idea'] = line.replace('* **[Visual Idea]:**', '').strip()
            elif line.startswith('* **[Speaker Notes]:**'): slide_data['notes'] = line.replace('* **[Speaker Notes]:**', '').strip()
        if not slide_data.get('title'): slide_data['title'] = full_title_line.split(':', 1)[-1].replace('**','').strip()
        if slide_data: slides.append(slide_data)
    return slides

# --- Streamlit UI ---
st.set_page_config(page_title="PPTX Generator", layout="wide")
st.title("Tự động hóa Tạo PPTX từ Markdown")

# --- Sidebar Configuration ---
st.sidebar.header("Cấu hình chung")
api_keys = load_api_keys()
if not api_keys:
    st.sidebar.error(f"No API keys found in {SECRETS_PATH}. Please add your keys.")
    st.stop()

selected_profile = st.sidebar.selectbox("Chọn một Profile Gemini API:", list(api_keys.keys()))
api_key = api_keys[selected_profile]

genai_client, text_models, image_models = None, [], []
if api_key and "YOUR_API_KEY" not in api_key:
    try:
        genai_client = get_gemini_client(api_key)
        text_models = [m.name for m in genai_client.list_models() if "generateContent" in m.supported_generation_methods] or ["gemini-1.5-flash", "gemini-pro"]
        image_models = ["models/imagen-3.0-generate-002", "models/imagen-3.0-generate-003"]
    except Exception as e:
        st.sidebar.error(f"Failed to initialize clients or list models: {e}")
else:
    st.sidebar.warning("Please provide a Gemini API Key.")

st.sidebar.subheader("Cài đặt Sinh nội dung & Hình ảnh")
# Set default text model to gemini-2.5-flash if available
default_text_model_name = "gemini-2.5-flash"
try:
    default_text_index = text_models.index(default_text_model_name)
except ValueError:
    default_text_index = 0 # Fallback to the first model
text_model_name = st.sidebar.selectbox(
    "Chọn mô hình sinh văn bản:", 
    text_models, 
    index=default_text_index, 
    disabled=not genai_client
)
image_model_name = st.sidebar.selectbox("Chọn mô hình sinh ảnh:", image_models, disabled=not genai_client)

st.sidebar.subheader("Cài đặt Âm thanh (Text-to-Speech)")
tts_enabled = st.sidebar.checkbox("Bật tính năng chuyển văn bản thành giọng nói", value=True)
# Set default TTS service to Gemini
tts_service = st.sidebar.selectbox(
    "Chọn dịch vụ TTS:",
    ["Google AI Studio (Gemini)", "Google Cloud TTS"],
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

# --- Tab 1: Full Presentation Generation ---
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
                    st.error("Không thể tạo. Vui lòng chọn một profile API hợp lệ.")
                    st.stop()

                # --- Clean up and setup directories only when generation starts ---
                if os.path.exists(output_dir): shutil.rmtree(output_dir)
                os.makedirs(os.path.join(output_dir, "images"))
                if tts_enabled: os.makedirs(os.path.join(output_dir, "audio"))

                progress_bar = st.progress(0)
                processed_slides = []
                st.subheader("Tiến trình tạo Slide")
                for i, slide in enumerate(slides_data):
                    progress_bar.progress((i + 1) / len(slides_data))
                    
                    with st.expander(f"Slide {i+1}: {slide.get('title', 'Không có tiêu đề')}", expanded=True):
                        st.write("--- Bắt đầu xử lý ---")
                        
                        # Content optimization is always needed for titles and structure
                        with st.spinner("Đang tối ưu hóa nội dung..."):
                            optimized_content = generate_slide_content(genai_client, text_model_name, slide.get("title", ""), slide.get("content", ""))
                            st.success("Tối ưu hóa nội dung thành công.")

                        image_path = None
                        if generation_mode != "Chỉ tạo âm thanh" and "visual_idea" in slide:
                            with st.spinner("Đang tạo ảnh..."):
                                image_prompt = generate_image_prompt(genai_client, text_model_name, slide["visual_idea"])
                                image_path = os.path.join(output_dir, "images", f"slide_{i+1}.png")
                                if not generate_image_with_gemini(api_key, image_model_name, image_prompt, image_path):
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

                with st.spinner("Đang tạo file PowerPoint..."):
                    create_presentation(output_pptx_path, processed_slides, DEFAULT_TITLE_BG, DEFAULT_CONTENT_BG)
                
                st.success("Tạo bài giảng thành công!")
                
                # --- Create ZIP archive ---
                archive_path_base = os.path.join(os.getcwd(), f"{base_name}_lecture_package")
                archive_path_zip = shutil.make_archive(archive_path_base, 'zip', output_dir)
                
                # --- Display Download Buttons ---
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
                # The temporary zip file will be cleaned up on the next run


        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn trong Tab 1: {e}")
            import traceback
            st.error(traceback.format_exc())

# --- Tab 2: Standalone Image Generation ---
with tab2:
    st.header("Công cụ tạo ảnh riêng lẻ")
    image_prompt_text = st.text_area("Nhập ý tưởng hình ảnh (Visual Idea):", key="image_prompt_tab2")
    
    if st.button("Tạo ảnh", key="create_image_tab2"):
        if not genai_client or not image_prompt_text:
            st.warning("Vui lòng chọn một profile API hợp lệ và nhập ý tưởng hình ảnh.")
        else:
            with st.spinner("Đang tạo ảnh..."):
                single_images_dir = os.path.join(os.getcwd(), "single_images")
                os.makedirs(single_images_dir, exist_ok=True)
                timestamp = int(time.time())
                output_image_path = os.path.join(single_images_dir, f"image_{timestamp}.png")
                final_prompt = generate_image_prompt(genai_client, text_model_name, image_prompt_text)
                success = generate_image_with_gemini(api_key, image_model_name, final_prompt, output_image_path)

                if success:
                    st.success("Tạo ảnh thành công!")
                    st.image(output_image_path)
                    with open(output_image_path, "rb") as f:
                        st.download_button("Tải ảnh về", f.read(), os.path.basename(output_image_path), key="download_image_tab2")
                else:
                    st.error("Tạo ảnh thất bại.")

# --- Tab 3: Standalone Audio Generation ---
with tab3:
    st.header("Công cụ tạo âm thanh riêng lẻ")
    text_to_speak_tab3 = st.text_area("Nhập văn bản cần chuyển thành giọng nói:", key="text_to_speak_tab3")

    if st.button("Tạo âm thanh", key="create_audio_tab3"):
        if not genai_client or not text_to_speak_tab3:
            st.warning("Vui lòng chọn một profile API hợp lệ và nhập văn bản.")
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
