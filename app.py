import streamlit as st
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Khám phá Bí mật Grab", page_icon="🛵", layout="wide")

# --- DỮ LIỆU CÂU HỎI (Chủ đề Ứng dụng CNTT tại Grab) ---
QUESTIONS = [
    {
        "id": 1,
        "word": "CHÚC",
        "question": "Mô hình ứng dụng tích hợp nhiều dịch vụ (gọi xe, giao thức ăn, thanh toán...) mà Grab đang theo đuổi gọi là gì?",
        "options": ["A. Mini App", "B. Super App", "C. Web App", "D. Single App"],
        "answer": "B. Super App"
    },
    {
        "id": 2,
        "word": "MỌI",
        "question": "Xu hướng quản trị cốt lõi của Grab là Quản trị dựa trên yếu tố nào?",
        "options": ["A. Trực giác", "B. Kinh nghiệm", "C. Dữ liệu (Data-Driven)", "D. Cảm xúc"],
        "answer": "C. Dữ liệu (Data-Driven)"
    },
    {
        "id": 3,
        "word": "NGƯỜI",
        "question": "Công nghệ cốt lõi nào giúp Grab tự động phân tích và ghép nối tài xế với khách hàng một cách tối ưu?",
        "options": ["A. Blockchain", "B. Machine Learning", "C. Thực tế ảo (VR)", "D. In 3D"],
        "answer": "B. Machine Learning"
    },
    {
        "id": 4,
        "word": "MỘT",
        "question": "Hệ thống nào được Grab sử dụng chủ yếu để quản lý dữ liệu và chăm sóc khách hàng (CRM/CDP)?",
        "options": ["A. Nền tảng dữ liệu khách hàng", "B. Hệ thống kế toán", "C. Phần mềm diệt virus", "D. Mạng nội bộ LAN"],
        "answer": "A. Nền tảng dữ liệu khách hàng"
    },
    {
        "id": 5,
        "word": "NGÀY",
        "question": "Giải pháp CNTT nào giúp Grab quản trị rủi ro tài chính và xử lý hàng triệu giao dịch mỗi ngày?",
        "options": ["A. Ghi sổ tay", "B. Thanh toán tiền mặt", "C. Ví điện tử & Hệ thống AI", "D. Đếm tiền thủ công"],
        "answer": "C. Ví điện tử & Hệ thống AI"
    },
    {
        "id": 6,
        "word": "TỐT",
        "question": "Để dự báo và hoạch định chiến lược kinh doanh chính xác, Grab ứng dụng công nghệ phân tích dữ liệu nào?",
        "options": ["A. Small Data", "B. Big Data (Dữ liệu lớn)", "C. No Data", "D. Fake Data"],
        "answer": "B. Big Data (Dữ liệu lớn)"
    },
    {
        "id": 7,
        "word": "LÀNH",
        "question": "Một trong những hạn chế/rủi ro lớn nhất của việc quản trị hoàn toàn bằng thuật toán (Algorithmic Management) là gì?",
        "options": ["A. Chạy quá nhanh", "B. Tốn giấy mực", "C. Hiện tượng 'Hộp đen thuật toán'", "D. Giao diện xấu"],
        "answer": "C. Hiện tượng 'Hộp đen thuật toán'"
    }
]

TARGET_PHRASE = "CHÚC MỌI NGƯỜI MỘT NGÀY TỐT LÀNH"

# --- KHỞI TẠO SESSION STATE (Lưu trạng thái trò chơi) ---
if 'revealed_words' not in st.session_state:
    st.session_state.revealed_words = [False] * 7
if 'active_question' not in st.session_state:
    st.session_state.active_question = None
if 'game_won' not in st.session_state:
    st.session_state.game_won = False

# --- HÀM XỬ LÝ SỰ KIỆN ---
def open_question(idx):
    st.session_state.active_question = idx

def close_question():
    st.session_state.active_question = None

def check_answer(q_idx, selected_option, correct_option):
    if selected_option == correct_option:
        st.session_state.revealed_words[q_idx] = True
        st.session_state.active_question = None
        st.toast('🎉 Trả lời chính xác! Tuyệt vời!', icon='💚')
        # Kiểm tra xem đã mở hết chưa
        if all(st.session_state.revealed_words):
            st.session_state.game_won = True
    else:
        st.toast('😢 Sai rồi! Hãy thử lại hoặc chọn câu khác nhé.', icon='❌')

# Hàm mới: Mở toàn bộ không cần nhập
def reveal_all():
    st.session_state.revealed_words = [True] * 7
    st.session_state.game_won = True
    st.toast('🏆 Xuất sắc! Mọi bí ẩn đã được giải mã!', icon='🌟')

# --- CSS TÙY CHỈNH (Giao diện đẹp, bo tròn, màu Grab) ---
st.markdown("""
<style>
    /* Nền trang web xanh nhạt */
    .stApp {
        background-color: #E8F5E9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Container nền trắng bo tròn */
    .white-container {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 16px rgba(0,177,79,0.1);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    /* Trang trí xe Grab bay lượn */
    .grab-car {
        position: absolute;
        font-size: 40px;
        opacity: 0.3;
        animation: drive 15s linear infinite;
        bottom: 10px;
    }
    @keyframes drive {
        0% { transform: translateX(-100px); }
        100% { transform: translateX(1000px); }
    }

    /* Các ô chữ ẩn/hiện */
    .word-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80px;
        background: linear-gradient(135deg, #00B14F, #009140);
        color: white;
        border-radius: 15px;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .word-hidden {
        background: #E0E0E0;
        color: #9E9E9E;
        font-size: 30px;
    }
    
    /* Style cho nút chọn câu hỏi */
    div.stButton > button {
        border-radius: 25px;
        font-weight: bold;
        border: 2px solid #00B14F;
        color: #00B14F;
        background-color: white;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #00B14F;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Tiêu đề */
    .main-title {
        text-align: center;
        color: #00B14F;
        font-size: 40px;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)


# --- HIỆU ỨNG PHÁO HOA & HOA RƠI KHI THẮNG ---
if st.session_state.game_won:
    st.balloons() # Hiệu ứng bóng bay/pháo hoa mặc định của Streamlit
    st.markdown("""
    <style>
    /* Hiệu ứng hoa rơi */
    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 1;}
        100% { transform: translateY(100vh) rotate(360deg); opacity: 0;}
    }
    .flower {
        position: fixed;
        font-size: 30px;
        z-index: 9999;
        top: -10vh;
        animation: fall linear forwards;
    }
    </style>
    <script>
    // Sinh ra những bông hoa và pháo hoa bằng JS
    const flowers = ['🌸', '🌺', '🌼', '✨', '🛵', '💚'];
    for(let i=0; i<50; i++) {
        let f = document.createElement('div');
        f.className = 'flower';
        f.innerText = flowers[Math.floor(Math.random() * flowers.length)];
        f.style.left = Math.random() * 100 + 'vw';
        f.style.animationDuration = (Math.random() * 3 + 2) + 's';
        f.style.animationDelay = Math.random() * 2 + 's';
        document.body.appendChild(f);
    }
    </script>
    <div style="text-align:center; padding: 30px; background-color: #00B14F; color: white; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,177,79,0.5); animation: pulse 2s infinite;">
        <h1 style="font-size: 50px;">🎉 XUẤT SẮC! 🎉</h1>
        <h2>CHÚC MỌI NGƯỜI MỘT NGÀY TỐT LÀNH</h2>
        <p>Bạn đã giải mã thành công bí mật quản trị số của Grab!</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# --- GIAO DIỆN CHÍNH ---

st.markdown('<div class="main-title">🛵 TRÒ CHƠI GIẢI MÃ BÍ MẬT GRAB 💚</div>', unsafe_allow_html=True)

# Khung chứa các ô chữ
st.markdown('<div class="white-container"><div class="grab-car">🛵</div>', unsafe_allow_html=True)
st.subheader("Bức thông điệp bí ẩn (7 Từ)")

cols = st.columns(7)
for i, col in enumerate(cols):
    with col:
        if st.session_state.revealed_words[i]:
            st.markdown(f'<div class="word-box">{QUESTIONS[i]["word"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="word-box word-hidden">?</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# Khung chọn câu hỏi & đoán toàn bộ
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="white-container">', unsafe_allow_html=True)
    st.subheader("🎯 Chọn câu hỏi để giải mã")
    btn_cols = st.columns(7)
    for i, b_col in enumerate(btn_cols):
        with b_col:
            # Nếu chữ đã mở thì hiển thị dấu check, chưa mở thì hiện số
            btn_label = f"Câu {i+1}" if not st.session_state.revealed_words[i] else "✅ Đã mở"
            if st.button(btn_label, key=f"btn_q_{i}", disabled=st.session_state.revealed_words[i]):
                open_question(i)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="white-container">', unsafe_allow_html=True)
    st.subheader("🚀 Mở toàn bộ")
    st.write("Nhấn nút dưới đây nếu bạn muốn lật mở tất cả ô chữ!")
    # Nút mới: Không cần nhập text nữa
    if st.button("Đoán đúng toàn bộ", use_container_width=True):
        reveal_all()
        st.rerun() # Tải lại trang ngay lập tức để hiện pháo hoa
    st.markdown('</div>', unsafe_allow_html=True)

# Khung hiển thị câu hỏi (Chỉ hiện khi click vào số)
if st.session_state.active_question is not None:
    idx = st.session_state.active_question
    q_data = QUESTIONS[idx]
    
    st.markdown('<div class="white-container" style="border: 3px solid #00B14F;">', unsafe_allow_html=True)
    col_q, col_close = st.columns([9, 1])
    with col_q:
        st.markdown(f"<h3 style='color: #009140;'>❓ Câu hỏi {idx + 1}: {q_data['question']}</h3>", unsafe_allow_html=True)
    with col_close:
        if st.button("✖ Đóng", key="close_btn"):
            close_question()
            st.rerun()

    st.write("Chọn đáp án đúng nhất:")
    
    # Bố cục 4 đáp án dạng lưới 2x2
    ans_cols = st.columns(2)
    for i, option in enumerate(q_data['options']):
        col_idx = i % 2
        with ans_cols[col_idx]:
            if st.button(option, key=f"opt_{idx}_{i}", use_container_width=True):
                check_answer(idx, option, q_data['answer'])
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)
