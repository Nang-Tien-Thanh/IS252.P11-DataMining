
# import thư viện
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
import graphviz
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB


def app():
    # Tùy chỉnh màu nền
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
            Phân lớp
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

    # Chọn thuật toán
    st.write("\n")
    st.write("_________________________________________________________________")
    st.markdown("#### **Vẽ cây quyết định**")
    algorithm = st.selectbox("Chọn thuật toán để vẽ cây quyết định:", ["None",
                                                                       "Thuật toán ID3"])

    # Chọn độ đo
    # Kiểm tra nếu thuật toán chọn là ID3 thì hiển thị nút "Chọn độ đo"
    if algorithm == "Thuật toán ID3":
        measure = st.selectbox(
            "Chọn độ đo:", ["Độ lợi thông tin", "Chỉ số Gini"])

    # 2 nút tạo cây quyêts định và nút Nút gốc của cây
    # Chia bố cục thành 3 cột
    col1, col2, col3 = st.columns([1, 2, 1])  # [1, 2, 1] để căn giữa

    with col1:
        create_tree_button = st.button("Tạo cây quyết định")
        st.write("")  # Để giữ khoảng trống

    with col2:
        # Hiển thị hai nút theo hàng ngang
        btn1, btn2 = st.columns(2)
        with btn1:
            st.write("")  # Để giữ khoảng trống

    with col3:
        st.write("")  # Để giữ khoảng trống

    # Tìm luật phân lớp cho mẫu
    st.write("\n\n")
    st.write("_________________________________________________________________")
    st.markdown("#### **Tìm luật phân lớp cho mẫu**")
    # Chọn thuật toán để phân lớp
    ThuatToanPhanLop = st.selectbox("Chọn thuật toán để phân lớp", ['None',
                                    "Cây quyết định", "Natives Bayes"])

    # Chia thành 4 cột cho 4 dropdownlist
    coll1, coll2, coll3, coll4 = st.columns(4)

    with coll1:
        attribute1 = st.selectbox(
            "Outlook", ['None', 'Sunny', 'Overcast', 'Rain'])
    with coll2:
        attribute2 = st.selectbox("Temp", ['None', 'Hot', 'Mild', 'Cool'])
    with coll3:
        attribute3 = st.selectbox("Humidity", ['None', 'High', 'Normal'])
    with coll4:
        attribute4 = st.selectbox("Wind", ['None', 'Strong', 'Weak'])

    # Hiển thị nút tìm luật

    # Hiển thị kết quả tìm luật
    coll1, coll2 = st.columns(2)
    with coll1:
        btnFind = st.button("Tìm")

    # ----------------------------------------------------------------
    st.write("_________________________________________________________________")
    # Hiển thị bảng kết quả tìm luật
    st.markdown("#### **Hiển thị kết quả**")

    # các hàm tạo cây quyết định
    def ID3_DoLoiThongTin(data, measure):
        if measure == "Độ lợi thông tin":
            # Xử lý dữ liệu đầu vào
            X = data[['Outlook', 'Temp', 'Humidity', 'Wind']]  # Các đặc trưng
            y = data['Play']  # Biến mục tiêu

            # Chuyển các giá trị phân loại thành số (vì DecisionTreeClassifier yêu cầu dữ liệu số)
            le = preprocessing.LabelEncoder()
            X = X.apply(le.fit_transform)
            y = y.map({'Yes': 1, 'No': 0})

            # Tạo mô hình cây quyết định với độ đo Độ lợi thông tin
            clf = DecisionTreeClassifier(criterion="entropy")
            clf.fit(X, y)

            # Xuất cây quyết định dưới dạng đồ họa
            dot_data = export_graphviz(clf, out_file=None,
                                       feature_names=X.columns,
                                       class_names=['No', 'Yes'],
                                       filled=True, rounded=True,
                                       special_characters=True)
            graph = graphviz.Source(dot_data)
            st.graphviz_chart(graph)

    def ID3_ChiSoGini(data, measure):
        if measure == "Chỉ số Gini":
            # Xử lý dữ liệu đầu vào
            X = data[['Outlook', 'Temp', 'Humidity', 'Wind']]  # Các đặc trưng
            y = data['Play']  # Biến mục tiêu

            # Chuyển các giá trị phân loại thành số (vì DecisionTreeClassifier yêu cầu dữ liệu số)
            le = preprocessing.LabelEncoder()
            X = X.apply(le.fit_transform)
            y = y.map({'Yes': 1, 'No': 0})

            # Tạo mô hình cây quyết định với chỉ số Gini
            clf = DecisionTreeClassifier(criterion="gini")
            clf.fit(X, y)

            # Xuất cây quyết định dưới dạng đồ họa
            dot_data = export_graphviz(clf, out_file=None,
                                       feature_names=X.columns,
                                       class_names=['No', 'Yes'],
                                       filled=True, rounded=True,
                                       special_characters=True)
            graph = graphviz.Source(dot_data)
            st.graphviz_chart(graph)

    # Tạo cây quyết định
    if create_tree_button:
        if measure == "Độ lợi thông tin":
            ID3_DoLoiThongTin(data, measure)

        elif measure == "Chỉ số Gini":
            ID3_ChiSoGini(data, measure)

    # phân lớp
    if btnFind:

        if ThuatToanPhanLop == "Cây quyết định":
            selected_attributes = {
                'Outlook': attribute1,
                'Temp': attribute2,
                'Humidity': attribute3,
                'Wind': attribute4
            }

            active_features = {key: value for key,
                               value in selected_attributes.items() if value != 'None'}

            if not active_features:
                st.error("Vui lòng chọn ít nhất một thuộc tính!")
            else:
                selected_columns = list(active_features.keys())
                X = data[selected_columns]
                y = data['Play']

                # Mã hóa dữ liệu
                le_dict = {}  # Từ điển lưu trữ LabelEncoder cho từng cột
                for col in selected_columns:
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col])
                    le_dict[col] = le

                y_encoded = y.map({'Yes': 1, 'No': 0})  # Mã hóa biến mục tiêu

                # Huấn luyện mô hình
                clf = DecisionTreeClassifier(criterion="entropy")
                clf.fit(X, y_encoded)

                # Chuẩn bị dữ liệu đầu vào từ người dùng
                try:
                    user_input = [le_dict[col].transform(
                        [value])[0] for col, value in active_features.items()]
                    prediction = clf.predict([user_input])
                    class_label = 'Yes' if prediction[0] == 1 else 'No'
                    st.success(f"Dự đoán: Lớp '{class_label}' (dựa trên các thuộc tính: {
                        ', '.join(selected_columns)})")
                except ValueError as e:
                    st.error(f"Lỗi mã hóa dữ liệu: {
                        e}. Vui lòng kiểm tra dữ liệu đầu vào.")

        elif ThuatToanPhanLop == "Natives Bayes":
            selected_attributes = {
                'Outlook': attribute1,
                'Temp': attribute2,
                'Humidity': attribute3,
                'Wind': attribute4
            }

            active_features = {key: value for key,
                               value in selected_attributes.items() if value != 'None'}

            if not active_features:
                st.error("Vui lòng chọn ít nhất một thuộc tính!")
            else:
                selected_columns = list(active_features.keys())
                X = data[selected_columns]
                y = data['Play']

                # Mã hóa dữ liệu
                le_dict = {}  # Từ điển lưu trữ LabelEncoder cho từng cột
                for col in selected_columns:
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col])
                    le_dict[col] = le

                y_encoded = y.map({'Yes': 1, 'No': 0})  # Mã hóa biến mục tiêu

                # Huấn luyện mô hình Naive Bayes
                nb = GaussianNB()  # Sử dụng Gaussian Naive Bayes
                nb.fit(X, y_encoded)

                # Chuẩn bị dữ liệu đầu vào từ người dùng
                try:
                    user_input = [le_dict[col].transform(
                        [value])[0] for col, value in active_features.items()]
                    prediction = nb.predict([user_input])
                    class_label = 'Yes' if prediction[0] == 1 else 'No'
                    st.success(f"Dự đoán: Lớp '{class_label}' (dựa trên các thuộc tính: {
                        ', '.join(selected_columns)})")
                except ValueError as e:
                    st.error(f"Lỗi mã hóa dữ liệu: {
                        e}. Vui lòng kiểm tra dữ liệu đầu vào.")
