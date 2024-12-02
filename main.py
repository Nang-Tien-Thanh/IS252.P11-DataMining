import streamlit as st

from page import Classification
from page import Cluster
from page import Popular

# Định dạng nền
st.markdown(
    """
    <style>
    stAppViewContainer {
        display: flex;
        justify-content: center; /* Căn ngang */
    }


        body {
            display: flex;
            justify-content: center; /* Căn ngang */
            padding: auto;

        }
        .body {
            width: 1280.5px;
            height: 823.5px;

            background: conic-gradient(from 180deg at 46.27% 61.2%, #FD9E02 -36.08deg, #126782 24.57deg, #219EBC 91.73deg, #000000 166.89deg, #000000 207.82deg, #FD9E02 323.92deg, #126782 384.57deg);
            filter: blur(100px);
            border-radius: 150px;
            margin-left:0px;
            position: absolute;

        }

        button {
                justify-content: center;
                align-items: center;
                padding: 9px 42px;
                font-size: 20px;
                font-weight: bold;
                color: #023047;  /* Màu chữ */
                text-align: center;
                width: 200px;
                background: linear-gradient(180deg, #219EBC 0%, #FFB703 100%); /* Nền gradient */
                border-radius: 10px;
                border: none; /* Bỏ viền */
                cursor: pointer; /* Thêm con trỏ chuột kiểu pointer */
                transition: background 0.3s ease; /* Hiệu ứng chuyển màu nền khi hover */
                font-size: 16px;
            }

            button:hover {
                background: linear-gradient(180deg, #FFB703 0%, #219EBC 100%); /* Đổi màu nền khi hover */
            }





    </style>

    <body style="background-color: #000000; justify-content: center; /* Căn ngang */
        align-items: center;    /* Căn dọc */">
        <div class="body">
           

            
            </div>       

        </div>



    </body>

        """,
    unsafe_allow_html=True
)

st.markdown(
    """ 
        <style>
           .header {
                    margin-top: 250px; 
                    display: flex;
                    justify-content: center; /* Căn giữa nội dung theo chiều ngang */
                    align-items: center;    /* Căn giữa nội dung theo chiều dọc */
                    font-size: 40px;
                    font-weight: bold;
                    color: #fff;
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.52);
                    padding: 10px; /* Thêm khoảng cách */
                    border-radius: 60px; /* Bo góc */
                    margin-bottom: 20px;
                    
                }
                
        </style>
         </head>
        <div class="header">
            <iconify-icon class="icon" icon="fluent:library-24-filled"></iconify-icon></a>
            IS252.P11 - Datamining
        </div>
        
        """, unsafe_allow_html=True

)


# Tạo sidebar với các lựa chọn
st.sidebar.title("Chọn tính năng")

# Các lựa chọn trong sidebar
option = st.sidebar.radio("",
                          ("None", "Tập phổ biến và luật kết hợp", "Tập thô", "Phân lớp", "Gom cụm"))

# Điều hướng đến trang tương ứng khi người dùng chọn
if option == "Phân lớp":
    Classification.app()  # Gọi hàm app trong Class.py
elif option == "Gom cụm":
    Cluster.app()  # Gọi hàm app trong Gomcum.py
elif option == "Tập phổ biến và luật kết hợp":
    Popular.app()  # Gọi hàm app trong T.py
