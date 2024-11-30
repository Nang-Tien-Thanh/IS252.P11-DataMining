
# import thư viện
from sklearn import preprocessing
import graphviz
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from minisom import MiniSom
import numpy as np
import matplotlib.pyplot as plt

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


    # Upload file CSV
    uploaded_file = st.file_uploader("Tải file dữ liệu (CSV):", type=["csv"])
    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file, sep=';')
        # Loại bỏ khoảng trắng trong tên cột (bao gồm cả khoảng trắng ở đầu và cuối)
            data.columns = data.columns.str.replace(' ', '', regex=True)

        # Loại bỏ khoảng trắng trong các giá trị dữ liệu (bao gồm cả khoảng trắng ở đầu và cuối)
            for column in data.columns:
                if data[column].dtype == 'object':  # Chỉ áp dụng cho các cột kiểu chuỗi
                    data[column] = data[column].str.replace(' ', '', regex=True)
            # In ra tên các cột trong tệp CSV
            st.write("Tên các cột trong tệp CSV:", data.columns)
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


    # CSS tùy chỉnh cho bảng Dữ liệu đã tải lên
    # custom_data_table_css = """
    #     <style>
    #         .data-table-container {
    #             display: flex;
    #             justify-content: center; /* Căn giữa bảng */
    #             align-items: center;
    #             margin: 20px auto; /* Căn giữa bảng */
    #             max-width: 100%; /* Giới hạn chiều rộng */
    #             overflow-x: auto; /* Thêm cuộn ngang nếu bảng quá rộng */
    #         }
    #         .data-table {
    #             border-collapse: collapse;
    #             font-size: 16px; /* Kích thước chữ */
    #             font-family: Arial, sans-serif;
    #             width: 100%; /* Chiếm toàn bộ chiều rộng khung */
    #             text-align: center;
    #             border: 1px solid #ddd; /* Viền bảng */
    #             color: #023047;
    #         }

    #         .data-table th {
    #             background-color: #FFB703; /* Màu nền tiêu đề */
    #             color: #FFFFFF; /* Màu chữ tiêu đề */
    #             padding: 10px;
    #             text-align: center;
    #         }

    #         .data-table td {
    #             padding: 8px 10px;
    #             text-align: center;
    #         }

    #         .data-table tr:nth-child(even) {
    #             background-color: #f3f3f3; /* Màu nền dòng chẵn */
    #         }

    #         .data-table tr:nth-child(odd) {
    #             background-color: #ffffff; /* Màu nền dòng lẻ */
    #         }

    #         .data-table tr:hover {
    #             background-color: #8ECAE6; /* Màu nền khi hover */
    #             color: #000000; /* Màu chữ khi hover */
    #         }
    #     </style>
    # """


    # Chuyển DataFrame thành HTML với class để hiển thị bảng
    # if data:
    #     data_html = data.to_html(
    #         index=False,
    #         classes='data-table',  # Thêm class để áp dụng CSS
    #         border=0
    #     )

    # Hiển thị CSS và bảng HTML
    # st.markdown(custom_data_table_css, unsafe_allow_html=True)
    # st.markdown(
    #     f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)


    # Chọn thuật toán
    st.write("\n")
    st.write("_________________________________________________________________")
    algorithm = st.selectbox("Chọn thuật toán để vẽ cây quyết định:", ["None",
                            "Thuật toán ID3"])

    # Chọn độ đo
    # Kiểm tra nếu thuật toán chọn là ID3 thì hiển thị nút "Chọn độ đo"
    if algorithm == "Thuật toán ID3":
        measure = st.selectbox("Chọn độ đo:", ["Độ lợi thông tin", "Chỉ số Gini"])


    # 2 nút tạo cây quyêts định và nút Nút gốc của cây
    # Chia bố cục thành 3 cột
    col1, col2, col3 = st.columns([1, 2, 1])  # [1, 2, 1] để căn giữa

    with col1:
        st.write("")  # Để giữ khoảng trống

    with col2:
        # Hiển thị hai nút theo hàng ngang
        btn1, btn2 = st.columns(2)
        with btn1:
            create_tree_button = st.button("Tạo cây quyết định")

        with btn2:
            goc_tree_button = st.button("Nút gốc của cây")

    with col3:
        st.write("")  # Để giữ khoảng trống


    # Tìm luật phân lớp cho mẫu
    st.write("\n\n")
    st.write("_________________________________________________________________")
    st.write("Tìm luật phân lớp cho mẫu")

    # Chọn thuật toán để phân lớp
    ThuatToanPhanLop = st.selectbox("Chọn thuật toán để phân lớp", ["Cây quyết định","Natives Bayes"])

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
        st.button("Tìm")
    with coll2:
        c_coll1, c_coll2 = st.columns(2)
        with c_coll1:
            st.write("Mẫu thuộc lớp:")
        with c_coll2:
            st.text("None")

    # ----------------------------------------------------------------
    st.write("_________________________________________________________________")
    # Hiển thị bảng kết quả tìm luật
    st.write("Hiển thị kết quả")

    #các hàm tạo cây quyết định
    def ID3_DoLoiThongTin (data,measure):
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
        if measure =="Chỉ số Gini":
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
            ID3_DoLoiThongTin(data,measure)

        else if measure == "Chỉ số Gini":
            ID3_ChiSoGini(data, measure)


    #phân lớp
    if ThuatToanPhanLop == "Cây quyết định":
        # Thu thập các thuộc tính được chọn
        selected_attributes = {
            'Outlook': attribute1,
            'Temp': attribute2,
            'Humidity': attribute3,
            'Wind': attribute4
        }
        
        # Lọc các thuộc tính không phải 'None'
        active_features = {key: value for key, value in selected_attributes.items() if value != 'None'}

        if not active_features:
            st.error("Vui lòng chọn ít nhất một thuộc tính!")
        else:
            # Lấy dữ liệu tương ứng với các thuộc tính đã chọn
            selected_columns = list(active_features.keys())
            X_partial = X[selected_columns]  # Dữ liệu chỉ chứa các cột được chọn
            X_partial_encoded = X_partial.apply(le.fit_transform)  # Mã hóa dữ liệu

            # Tái huấn luyện mô hình trên các thuộc tính đã chọn
            clf = DecisionTreeClassifier(criterion="entropy")
            clf.fit(X_partial_encoded, y_encoded)

            # Chuẩn bị dữ liệu đầu vào từ người dùng
            user_input = [le.fit_transform(data[col])[data[col] == value].iloc[0] for col, value in active_features.items()]
            
            # Dự đoán
            prediction = clf.predict([user_input])
            class_label = 'Yes' if prediction[0] == 1 else 'No'

            # Hiển thị kết quả
            st.success(f"Dự đoán: Lớp '{class_label}' (dựa trên các thuộc tính: {', '.join(selected_columns)})")


    else if ThuatToanPhanLop == "Natives Bayes":
        # Thu thập các thuộc tính được chọn
        selected_attributes = {
            'Outlook': attribute1,
            'Temp': attribute2,
            'Humidity': attribute3,
            'Wind': attribute4
        }
        
        # Lọc các thuộc tính không phải 'None'
        active_features = {key: value for key, value in selected_attributes.items() if value != 'None'}

        if not active_features:
            st.error("Vui lòng chọn ít nhất một thuộc tính!")
        else:
            # Lấy dữ liệu tương ứng với các thuộc tính đã chọn
            selected_columns = list(active_features.keys())
            X_partial = X[selected_columns]  # Dữ liệu chỉ chứa các cột được chọn
            X_partial_encoded = X_partial.apply(le.fit_transform)  # Mã hóa dữ liệu

            # Huấn luyện mô hình Naive Bayes trên các thuộc tính đã chọn
            nb = GaussianNB()  # Hoặc MultinomialNB() tùy thuộc vào loại dữ liệu
            nb.fit(X_partial_encoded, y_encoded)

            # Chuẩn bị dữ liệu đầu vào từ người dùng
            user_input = [le.fit_transform(data[col])[data[col] == value].iloc[0] for col, value in active_features.items()]
            
            # Dự đoán
            prediction = nb.predict([user_input])
            class_label = 'Yes' if prediction[0] == 1 else 'No'

            # Hiển thị kết quả
            st.success(f"Dự đoán: Lớp '{class_label}' (dựa trên các thuộc tính: {', '.join(selected_columns)})")
