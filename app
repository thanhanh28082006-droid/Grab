import streamlit as st
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Grab Case Study - Mini Game",
    page_icon="🎮",
    layout="centered"
)

# --- CSS TÙY CHỈNH (GIAO DIỆN CHUẨN GRAB & HỘP BÍ MẬT) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main-title {
        color: #00B14F;
        text-align: center;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    .word-box {
        background-color: #00B14F;
        color: white;
        padding: 20px 10px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 5px;
    }
    .locked-box {
        background-color: #e0e0e0;
        color: #9e9e9e;
        padding: 20px 10px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        border: 2px dashed #bdbdbd;
        margin: 5px;
    }
    .question-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
        border-top: 5px solid #00B14F;
    }
    .stButton>button {
        background-color: #00B14F;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #008a3d;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU CÂU HỎI BÁM SÁT BÀI THUYẾT TRÌNH ---
questions = [
    {
        "q": "Câu 1: Grab hoạt động chủ yếu dựa trên mô hình quản trị nào?",
        "options": ["Quản trị cảm tính", "Quản trị truyền thống", "Quản trị dựa trên dữ liệu (Data-Driven)", "Quản trị thủ công"],
        "answer": "Quản trị dựa trên dữ liệu (Data-Driven)"
    },
    {
        "q": "Câu 2: Công nghệ/Thuật toán nào giúp Grab tối ưu hóa việc ghép nối tài xế và khách hàng?",
        "options": ["DispatchGym", "GrabGPT", "Temporal Workflow", "Blockchain"],
        "answer": "DispatchGym"
    },
    {
        "q": "Câu 3: Nền tảng nào giúp Grab thu thập và cá nhân hóa trải nghiệm khách hàng?",
        "options": ["Hệ thống ERP", "Customer Data Platform (CDP)", "Phần mềm kế toán", "Telematics"],
        "answer": "Customer Data Platform (CDP)"
    },
    {
        "q": "Câu 4: Grab quản lý rủi ro gian lận (RiskOps) và điều tra chiếm đoạt tài khoản bằng công cụ gì?",
        "options": ["SOP-driven LLM Agent", "Kiểm tra thủ công bằng nhân viên", "Camera giám sát", "Chỉ dùng mã OTP"],
        "answer": "SOP-driven LLM Agent"
    },
    {
        "q": "Câu 5: Trong quản trị dữ liệu, Grab đã chuyển đổi từ kho dữ liệu tập trung sang mô hình phân tán nào?",
        "options": ["Data Lake", "Data Warehouse", "Data Mesh", "Cloud Storage"],
        "answer": "Data Mesh"
    },
    {
        "q": "Câu 6: Trợ lý AI nội bộ nào giúp các kỹ sư Grab tiết kiệm hàng trăm giờ làm việc?",
        "options": ["Siri", "Google Assistant", "Copilot", "GrabGPT"],
        "answer": "GrabGPT"
    },
    {
        "q": "Câu 7: Theo kết luận, yếu tố nào quyết định thành công cuối cùng của chuyển đổi số?",
        "options": ["Chỉ cần mua phần mềm đắt tiền", "Chiến lược quản trị và Con người", "Thay thế hoàn toàn con người bằng AI", "Sở hữu nhiều tài sản vật lý"],
        "answer": "Chiến lược quản trị và Con người"
    }
]

secret_words = ["CHÚC", "MỌI", "NGƯỜI", "MỘT", "NGÀY", "TỐT", "LÀNH"]

# --- QUẢN LÝ TRẠNG THÁI (SESSION STATE) ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered_correctly' not in st.session_state:
    st.session_state.answered_correctly = False
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- GIAO DIỆN CHÍNH ---
st.markdown('<div class="main-title">🎮 MINIGAME: GIẢI MÃ THÔNG ĐIỆP BÍ MẬT</div>', unsafe_allow_html=True)
st.write("Tham gia trả lời 7 câu hỏi tổng kết đề tài Grab. Mỗi câu trả lời đúng sẽ mở khóa một từ bí mật!")

# Thanh tiến trình
progress = st.session_state.score / 7
st.progress(progress)
st.write(f"**Điểm số:** {st.session_state.score}/7")

# --- HIỂN THỊ CÁC HỘP TỪ BÍ MẬT ---
cols = st.columns(7)
for i in range(7):
    with cols[i]:
        if i < st.session_state.score:
            st.markdown(f'<div class="word-box">{secret_words[i]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="locked-box">❓</div>', unsafe_allow_html=True)

st.markdown("---")

# --- LOGIC CÂU HỎI ---
if not st.session_state.game_over:
    q_data = questions[st.session_state.current_q]
    
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader(q_data["q"])
    
    # Form trả lời
    with st.form(key=f"form_{st.session_state.current_q}"):
        choice = st.radio("Chọn đáp án của bạn:", q_data["options"], index=None)
        submit_btn = st.form_submit_button("Trả lời 🚀")
        
        if submit_btn:
            if choice == q_data["answer"]:
                st.success("✅ Chính xác! Bạn đã mở khóa được 1 từ.")
                st.session_state.score += 1
                st.session_state.answered_correctly = True
                
                # Cập nhật trạng thái câu hỏi
                if st.session_state.current_q < 6:
                    st.session_state.current_q += 1
                    time.sleep(1) # Đợi 1 giây để người dùng đọc thông báo
                    st.rerun()
                else:
                    st.session_state.game_over = True
                    time.sleep(1)
                    st.rerun()
            elif choice is None:
                st.warning("⚠️ Vui lòng chọn một đáp án trước khi gửi.")
            else:
                st.error("❌ Sai rồi. Hãy suy nghĩ lại nhé!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- KẾT THÚC GAME ---
else:
    st.markdown('<div class="question-card" style="text-align: center;">', unsafe_allow_html=True)
    st.title("🎉 XUẤT SẮC!")
    st.subheader(f"Thông điệp bí mật là: {' '.join(secret_words)}")
    st.write("Cảm ơn thầy cô và các bạn đã lắng nghe bài thuyết trình của nhóm!")
    st.markdown('</div>', unsafe_allow_html=True)
    st.balloons() # Hiệu ứng bóng bay/pháo hoa
    
    if st.button("🔄 Chơi lại từ đầu"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered_correctly = False
        st.session_state.game_over = False
        st.rerun()

# Footer
st.markdown("<br><br><p style='text-align: center; color: #9e9e9e; font-size: 12px;'>Phát triển cho Bài báo cáo môn Quản trị Doanh nghiệp</p>", unsafe_allow_html=True)
