import streamlit as st
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Grab Case Study - Mini Game",
    page_icon="🎮",
    layout="centered"
)

# --- 2. GIAO DIỆN CSS TÙY CHỈNH (MÀU XANH GRAB) ---
st.markdown("""
    <style>
    /* Nền toàn trang màu xanh Grab */
    .stApp {
        background-color: #00B14F;
    }
    
    /* Ghi đè màu chữ mặc định thành trắng */
    h1, h2, h3, p, span, div, label {
        color: white !important;
    }
    
    /* Tiêu đề chính */
    .main-title {
        text-align: center;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Hộp chứa từ khóa đã mở */
    .word-box {
        background-color: white;
        color: #00B14F !important;
        padding: 15px 5px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 900;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        margin: 5px;
        border: 2px solid white;
    }
    
    /* Hộp chứa từ khóa bị khóa */
    .locked-box {
        background-color: rgba(255, 255, 255, 0.15);
        color: rgba(255, 255, 255, 0.5) !important;
        padding: 15px 5px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        border: 2px dashed rgba(255, 255, 255, 0.4);
        margin: 5px;
    }
    
    /* Thẻ chứa câu hỏi cực to ở giữa */
    .question-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 40px 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        margin-top: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        text-align: center;
    }
    
    /* Form câu hỏi siêu to */
    .question-text {
        font-size: 2.2rem !important;
        font-weight: 800;
        line-height: 1.5;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Tùy chỉnh Nút Submit */
    .stButton>button {
        background-color: white;
        color: #00B14F !important;
        font-weight: 900;
        font-size: 1.3rem;
        border-radius: 12px;
        border: none;
        padding: 15px 20px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        text-transform: uppercase;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        background-color: #f0f0f0;
    }
    
    /* Làm đẹp các lựa chọn Radio */
    div[role="radiogroup"] {
        gap: 15px;
    }
    div[role="radiogroup"] > label {
        background-color: rgba(255, 255, 255, 0.15);
        padding: 15px 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-size: 1.2rem;
        cursor: pointer;
        transition: background 0.3s;
    }
    div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.25);
    }
    
    /* Lời chúc cuối cùng */
    .final-message {
        background-color: white;
        color: #00B14F !important;
        padding: 40px;
        border-radius: 20px;
        font-size: 3.5rem !important;
        font-weight: 900;
        margin: 30px 0;
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
        line-height: 1.4;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DỮ LIỆU GAME (7 CÂU HỎI + 7 TỪ KHÓA BÍ MẬT) ---
questions = [
    {
        "q": "Câu 1: Grab hiện đang hoạt động dựa trên mô hình quản trị cốt lõi nào?",
        "options": ["Quản trị cảm tính", "Quản trị dựa trên dữ liệu (Data-Driven)", "Quản trị hành chính truyền thống", "Quản trị thủ công"],
        "answer": "Quản trị dựa trên dữ liệu (Data-Driven)"
    },
    {
        "q": "Câu 2: Công nghệ nào giúp Grab ghép nối tài xế và hành khách siêu tốc?",
        "options": ["DispatchGym", "Temporal Workflow", "Blockchain", "ChatGPT"],
        "answer": "DispatchGym"
    },
    {
        "q": "Câu 3: Để cá nhân hóa trải nghiệm khách hàng, Grab dùng nền tảng gì?",
        "options": ["Hệ thống ERP", "Customer Data Platform (CDP)", "Telematics", "Bug Bounty"],
        "answer": "Customer Data Platform (CDP)"
    },
    {
        "q": "Câu 4: Công cụ giúp Grab tự động hóa điều tra rủi ro (RiskOps) là gì?",
        "options": ["Nhân viên trực tổng đài", "Camera giám sát", "SOP-driven LLM Agent", "Kiểm tra mã PIN"],
        "answer": "SOP-driven LLM Agent"
    },
    {
        "q": "Câu 5: Grab đã chuyển đổi kho dữ liệu của mình sang mô hình phân tán nào?",
        "options": ["Data Lake", "Data Mesh", "Data Warehouse", "Local Server"],
        "answer": "Data Mesh"
    },
    {
        "q": "Câu 6: Trợ lý AI nội bộ giúp kỹ sư Grab tiết kiệm hàng trăm giờ làm việc tên là gì?",
        "options": ["Siri", "Google Assistant", "GrabGPT", "Cortana"],
        "answer": "GrabGPT"
    },
    {
        "q": "Câu 7: Tóm lại, yếu tố nào quyết định thành công cuối cùng của chuyển đổi số?",
        "options": ["Nhiều tiền mua phần mềm", "Chiến lược quản trị & Con người", "Cắt giảm toàn bộ nhân viên", "Sở hữu lượng xe khổng lồ"],
        "answer": "Chiến lược quản trị & Con người"
    }
]

secret_words = ["CHÚC", "MỌI", "NGƯỜI", "MỘT", "NGÀY", "TỐT", "LÀNH!"]

# --- 4. TRẠNG THÁI TRÒ CHƠI (SESSION STATE) ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- 5. LOGIC HIỂN THỊ ---
st.markdown('<div class="main-title">🚀 TRÒ CHƠI TỔNG KẾT KIẾN THỨC</div>', unsafe_allow_html=True)

# Hiển thị thanh tiến trình
progress = st.session_state.current_q / 7
st.progress(progress)

# Hiển thị 7 Ô CHỮ BÍ MẬT (Mở dần khi trả lời đúng)
cols = st.columns(7)
for i in range(7):
    with cols[i]:
        if i < st.session_state.current_q:
            st.markdown(f'<div class="word-box">{secret_words[i]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="locked-box">❓</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# NẾU CHƯA KẾT THÚC GAME -> HIỂN THỊ CÂU HỎI
if not st.session_state.game_over:
    q_data = questions[st.session_state.current_q]
    
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    
    # Text câu hỏi siêu to
    st.markdown(f'<div class="question-text">{q_data["q"]}</div>', unsafe_allow_html=True)
    
    # Khung nhập câu trả lời
    with st.form(key=f"form_{st.session_state.current_q}"):
        choice = st.radio("Chọn đáp án chính xác:", q_data["options"], index=None, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("CHỌN & MỞ KHÓA Ô CHỮ")
        
        if submit_btn:
            if choice == q_data["answer"]:
                st.success("🎉 Chính xác! Bạn đã mở khóa được một ô chữ.")
                # Nếu là câu cuối cùng thì kết thúc game
                if st.session_state.current_q == 6:
                    st.session_state.game_over = True
                
                # Cập nhật số câu hỏi và load lại trang
                st.session_state.current_q += 1
                time.sleep(1) # Chờ 1 giây để load mượt hơn
                st.rerun()
            elif choice is None:
                st.warning("⚠️ Vui lòng chọn một đáp án trước khi bấm nút!")
            else:
                st.error("❌ Sai rồi! Nhớ lại bài thuyết trình của nhóm và chọn lại nhé.")
                
    st.markdown('</div>', unsafe_allow_html=True)

# NẾU ĐÃ TRẢ LỜI XONG 7 CÂU -> BẮN PHÁO HOA & HIỂN THỊ LỜI CHÚC
else:
    st.markdown('<div class="question-card" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown('<h2 style="font-size: 2.5rem; text-transform: uppercase;">🎉 THỬ THÁCH HOÀN THÀNH 🎉</h2>', unsafe_allow_html=True)
    
    # Hiển thị thông điệp siêu to
    final_message = " ".join(secret_words)
    st.markdown(f'<div class="final-message">{final_message}</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="font-weight: 400;">Cảm ơn thầy cô và các bạn đã lắng nghe báo cáo của nhóm!</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hiệu ứng pháo hoa của Streamlit
    st.balloons()
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Nút chơi lại
    if st.button("🔄 CHƠI LẠI TỪ ĐẦU"):
        st.session_state.current_q = 0
        st.session_state.game_over = False
        st.rerun()
