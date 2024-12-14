# import thư viện
import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import pearsonr


def app():
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



        </body>

            """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
            <style>
            .header {
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
                Tiền xử lý dữ liệu
            </div>

            """, unsafe_allow_html=True

    )

    # CSS tùy chỉnh cho bảng Dữ liệu đã tải lên
    custom_data_table_css = """
            <style>
                .data-table-container {
                    display: flex;
                    justify-content: center; /* Căn giữa bảng */
                    align-items: center;
                    margin: 20px auto; /* Căn giữa bảng */
                    max-width: 100%; /* Giới hạn chiều rộng */
                    overflow-x: auto; /* Thêm cuộn ngang nếu bảng quá rộng */
                }
                .data-table {
                    border-collapse: collapse;
                    font-size: 16px; /* Kích thước chữ */
                    font-family: Arial, sans-serif;
                    width: 100%; /* Chiếm toàn bộ chiều rộng khung */
                    text-align: center;
                    border: 1px solid #ddd; /* Viền bảng */
                    color: #023047;
                }

                .data-table th {
                    background-color: #FFB703; /* Màu nền tiêu đề */
                    color: #FFFFFF; /* Màu chữ tiêu đề */
                    padding: 10px;
                    text-align: center;
                }

                .data-table td {
                    padding: 8px 10px;
                    text-align: center;
                }

                .data-table tr:nth-child(even) {
                    background-color: #f3f3f3; /* Màu nền dòng chẵn */
                }

                .data-table tr:nth-child(odd) {
                    background-color: #ffffff; /* Màu nền dòng lẻ */
                }

                .data-table tr:hover {
                    background-color: #8ECAE6; /* Màu nền khi hover */
                    color: #000000; /* Màu chữ khi hover */
                }
            </style>
        """
    st.markdown("#### **Tải File dữ liệu**")
    # Upload file CSV
    # data = ""
    uploaded_file = st.file_uploader("Tải file dữ liệu (CSV):", type=["csv"])
    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file, sep=';')
        # Loại bỏ khoảng trắng trong tên cột (bao gồm cả khoảng trắng ở đầu và cuối)
            data.columns = data.columns.str.replace(' ', '', regex=True)

        # Loại bỏ khoảng trắng trong các giá trị dữ liệu (bao gồm cả khoảng trắng ở đầu và cuối)
            for column in data.columns:
                if data[column].dtype == 'object':  # Chỉ áp dụng cho các cột kiểu chuỗi
                    data[column] = data[column].str.replace(
                        ' ', '', regex=True)

            data_html = data.to_html(
                index=False,
                classes='data-table',  # Thêm class để áp dụng CSS
                border=0
            )

            st.markdown(custom_data_table_css, unsafe_allow_html=True)
            st.markdown(
                f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Lỗi khi tải file: {e}")
    else:
        st.write("Vui lòng chờ tải file dữ liêu lên")

    # Tính hệ số tương quan

    st.write("\n_________________________________________________________________")
    st.markdown("#### **Tính hệ số tương quan**")

    # chức năng tính hệ số tương quan
    if st.button("Tính"):
        # Lấy cột DoanhThu và Chiphiquangcao
        doanh_thu = data['DoanhThu']
        chi_phi = data['Chiphíquảngcáo']

        # Tính hệ số tương quan Pearson
        correlation, _ = pearsonr(doanh_thu, chi_phi)

        # Hiển thị kết quả
        st.success(f"Hệ số tương quan: {correlation:.4f}")
