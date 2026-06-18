import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Khám phá Bí mật Grab", page_icon="🛵", layout="wide")

# --- DỮ LIỆU CÂU HỎI ---
QUESTIONS = [
    {"id": 1, "word": "CHÚC", "question": "Mô hình ứng dụng tích hợp nhiều dịch vụ (gọi xe, giao thức ăn, thanh toán...) mà Grab đang theo đuổi gọi là gì?", "options": ["A. Mini App", "B. Super App", "C. Web App", "D. Single App"], "answer": "B. Super App"},
    {"id": 2, "word": "MỌI", "question": "Xu hướng quản trị cốt lõi của Grab là Quản trị dựa trên yếu tố nào?", "options": ["A. Trực giác", "B. Kinh nghiệm", "C. Dữ liệu (Data-Driven)", "D. Cảm xúc"], "answer": "C. Dữ liệu (Data-Driven)"},
    {"id": 3, "word": "NGƯỜI", "question": "Công nghệ cốt lõi nào giúp Grab tự động phân tích và ghép nối tài xế với khách hàng một cách tối ưu?", "options": ["A. Blockchain", "B. Machine Learning", "C. Thực tế ảo (VR)", "D. In 3D"], "answer": "B. Machine Learning"},
    {"id": 4, "word": "MỘT", "question": "Hệ thống nào được Grab sử dụng chủ yếu để quản lý dữ liệu và chăm sóc khách hàng (CRM/CDP)?", "options": ["A. Nền tảng dữ liệu khách hàng", "B. Hệ thống kế toán", "C. Phần mềm diệt virus", "D. Mạng nội bộ LAN"], "answer": "A. Nền tảng dữ liệu khách hàng"},
    {"id": 5, "word": "NGÀY", "question": "Giải pháp CNTT nào giúp Grab quản trị rủi ro tài chính và xử lý hàng triệu giao dịch mỗi ngày?", "options": ["A. Ghi sổ tay", "B. Thanh toán tiền mặt", "C. Ví điện tử & Hệ thống AI", "D. Đếm tiền thủ công"], "answer": "C. Ví điện tử & Hệ thống AI"},
    {"id": 6, "word": "TỐT", "question": "Để dự báo và hoạch định chiến lược kinh doanh chính xác, Grab ứng dụng công nghệ phân tích dữ liệu nào?", "options": ["A. Small Data", "B. Big Data (Dữ liệu lớn)", "C. No Data", "D. Fake Data"], "answer": "B. Big Data (Dữ liệu lớn)"},
    {"id": 7, "word": "LÀNH", "question": "Một trong những hạn chế/rủi ro lớn nhất của việc quản trị hoàn toàn bằng thuật toán (Algorithmic Management) là gì?", "options": ["A. Chạy quá nhanh", "B. Tốn giấy mực", "C. Hiện tượng 'Hộp đen thuật toán'", "D. Giao diện xấu"], "answer": "C. Hiện tượng 'Hộp đen thuật toán'"}
]

# --- KHỞI TẠO SESSION STATE ---
if 'revealed_words' not in st.session_state:
    st.session_state.revealed_words = [False] * 7
if 'game_won' not in st.session_state:
    st.session_state.game_won = False

# --- HÀM XỬ LÝ (DIALOG) ---
@st.dialog("🎯 THỬ THÁCH GIẢI MÃ", width="large")
def show_question_modal(idx):
    q_data = QUESTIONS[idx]
    
    # State tạm thời cho modal
    if f"q_status_{idx}" not in st.session_state:
        st.session_state[f"q_status_{idx}"] = "playing"
    
    st.markdown(f"<h3 style='text-align:center; color:#00B14F;'>{q_data['question']}</h3>", unsafe_allow_html=True)
    
    if st.session_state[f"q_status_{idx}"] == "correct":
        st.success("✅ Bạn đã trả lời đúng!")
        if st.button("Đóng & Tiếp tục", use_container_width=True):
            st.rerun()
    else:
        if st.session_state[f"q_status_{idx}"] == "wrong":
            st.error("❌ Sai rồi, thử lại nhé!")
        
        cols = st.columns(2)
        for i, option in enumerate(q_data['options']):
            with cols[i % 2]:
                if st.button(option, key=f"opt_{idx}_{i}", use_container_width=True):
                    if option == q_data['answer']:
                        st.session_state[f"q_status_{idx}"] = "correct"
                        st.session_state.revealed_words[idx] = True
                        st.rerun()
                    else:
                        st.session_state[f"q_status_{idx}"] = "wrong"
                        st.rerun()

# --- CSS TÙY CHỈNH ---
st.markdown("""
<style>
    .stApp { background-color: #E8F5E9; }
    .word-box { display: flex; justify-content: center; align-items: center; height: 80px; background: linear-gradient(135deg, #00B14F, #009140); color: white; border-radius: 15px; font-size: 24px; font-weight: bold; }
    .word-hidden { background: #E0E0E0; color: #9E9E9E; }
    .white-container { background-color: #FFFFFF; border-radius: 20px; padding: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .main-title { text-align: center; color: #00B14F; font-size: 35px; font-weight: 900; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- GIAO DIỆN ---
st.markdown('<div class="main-title">🛵 TRÒ CHƠI GIẢI MÃ BÍ MẬT GRAB 💚</div>', unsafe_allow_html=True)

st.markdown('<div class="white-container">', unsafe_allow_html=True)
cols = st.columns(7)
for i, col in enumerate(cols):
    with col:
        if st.session_state.revealed_words[i]:
            st.markdown(f'<div class="word-box">{QUESTIONS[i]["word"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="word-box word-hidden">?</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.subheader("🎯 Chọn câu hỏi để giải mã")
btn_cols = st.columns(7)
for i, b_col in enumerate(btn_cols):
    with b_col:
        label = f"Câu {i+1}" if not st.session_state.revealed_words[i] else "✅"
        if st.button(label, key=f"btn_{i}", disabled=st.session_state.revealed_words[i]):
            show_question_modal(i)

if all(st.session_state.revealed_words):
    st.balloons()
    st.success("🎉 Bạn đã giải mã thành công toàn bộ thông điệp!")
