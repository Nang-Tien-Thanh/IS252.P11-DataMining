import streamlit as st

st.title('Ứng dụng xử lý dữ liệu')
st.button('Start')

# Tùy chỉnh màu nền
st.markdown(
    """
    <style>
    /* Tạo lớp nền làm mờ */
    .blur-background {
        width: 1300.5px;
        height: 843.5px;
        position: fixed; /* Cố định ở toàn màn hình */
        top: 0;
        left: 0;
        background: conic-gradient(
            from 180deg at 46.27% 61.2%,
            #FD9E02 -36.08deg,
            #126782 24.57deg,
            #219EBC 91.73deg,
            #000000 166.89deg,
            #000000 207.82deg,
            #FD9E02 323.92deg,
            #126782 384.57deg
        );
        filter: blur(100px); /* Làm mờ */
        border-radius: 150px; /* Bo góc */
        z-index: -1000; /* Đưa lớp nền xuống dưới nội dung */
        margin-top: 16px; 
        margin-right: 70px;
        margin-left: 70px;
        margin-bottom: 16px; 
    }

    /* Đảm bảo nội dung hiển thị bình thường */
    .stApp {
        position: relative;
        z-index: 0;
    }
    
    .container {
        max-width:1440px;
        max-height:1024 px;
        display: flex;
        justify-content: center;
        align-items: center;    /* Căn dọc */
        position: relative;
        border: 1px white solid;
    }
    </style>
    
    <div class = "container" >
        <div class="blur-background"></div>
    </div>
    
    """,
    unsafe_allow_html=True
)
