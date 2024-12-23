# cd D:\NAM3\HK1\DataMining\DOAN\IS252.P11-DataMining\page
# streamlit run Cluster.py
# Import thư viện

import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from minisom import MiniSom
import numpy as np
import matplotlib.pyplot as plt


def app():
    # CSS tuỳ chỉnh giao diện
    st.markdown("""
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Cluster</title>
            <!-- Tải thư viện Iconify -->
            <script src="https://code.iconify.design/iconify-icon/2.1.0/iconify-icon.min.js"></script>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }

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
            }

            button:hover {
                background: linear-gradient(180deg, #FFB703 0%, #219EBC 100%); /* Đổi màu nền khi hover */
            }
                    
        </style>
        </head>
        <div class="header">
            <iconify-icon class="icon" icon="fluent:library-24-filled"></iconify-icon></a>
            Gom cụm
        </div>

    """, unsafe_allow_html=True)

    # Upload file CSV
    uploaded_file = st.file_uploader("Tải file dữ liệu (CSV):", type=["csv"])
    if uploaded_file:
        # Nếu file đã được tải lên
        data = pd.read_csv(uploaded_file, sep=';')
        st.success("Dữ liệu đã tải thành công!")

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

        # Chuyển DataFrame thành HTML với class để hiển thị bảng
        data_html = data.to_html(
            index=False,
            classes='data-table',  # Thêm class để áp dụng CSS
            border=0
        )

        # Hiển thị CSS và bảng HTML
        st.markdown(custom_data_table_css, unsafe_allow_html=True)
        st.markdown(
            f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)

        # Chọn thuật toán
        algorithm = st.selectbox("Chọn thuật toán:", ["K-means", "Kohonen"])

    # Hiển thị kết quả K-means
        if algorithm == "K-means":
            num_clusters = st.number_input(
                "Số cụm (k):", min_value=1, max_value=20, step=1, value=3)
            if st.button("Thực hiện K-means", key="kmeans"):
                # Thực hiện K-means
                kmeans = KMeans(n_clusters=num_clusters, random_state=0)
                kmeans.fit(data)
                data["Gom cụm"] = kmeans.labels_

                # Hiển thị kết quả
                data['Gom cụm'] = kmeans.labels_  # Thêm nhãn cụm vào dữ liệu

                # Hiển thị tiêu đề
                st.markdown(
                    '<h2 style="margin-bottom: -40px;">Kết quả K-means:</h2>', unsafe_allow_html=True)

                # CSS tùy chỉnh cho bảng K-means
                custom_table_css = """
                    <style>
                        .kmeans-table-container {
                            display: flex;
                            justify-content: center; /* Căn giữa bảng */
                            align-items: center;
                            margin: 0 auto; /* Tự động căn giữa */
                            max-width: 100%; /* Giới hạn chiều rộng */
                            overflow-x: auto; /* Thêm cuộn ngang nếu bảng quá lớn */
                        }
                        .kmeans-table {
                            border-collapse: collapse;
                            font-size: 16px; /* Kích thước chữ */
                            font-family: Arial, sans-serif;
                            width: 100%; /* Chiều rộng bảng */
                            text-align: center;
                            border: 1px solid #ddd; /* Viền bảng */
                            color: #023047;
                            margin: 20px auto; /* Khoảng cách giữa bảng và các phần tử khác */
                        }

                        .kmeans-table th {
                            background-color: #126782; /* Màu nền tiêu đề */
                            color: #FFFFFF; /* Màu chữ tiêu đề */
                            padding: 10px;
                            text-align: center;
                        }

                        .kmeans-table td {
                            padding: 8px 10px;
                            text-align: center;
                        }

                        .kmeans-table tr:nth-child(even) {
                            background-color: #f3f3f3; /* Màu nền dòng chẵn */
                        }

                        .kmeans-table tr:nth-child(odd) {
                            background-color: #ffffff; /* Màu nền dòng lẻ */
                        }

                        .kmeans-table tr:hover {
                            background-color: #FFB703; /* Màu nền khi hover */
                            color: #000000; /* Màu chữ khi hover */
                        }
                    </style>
                """

                # Chuyển đổi dataframe thành HTML với class
                data_html = data.to_html(
                    index=False,
                    classes='kmeans-table',
                    border=0
                )

                # Hiển thị bảng kết quả với CSS
                st.markdown(custom_table_css, unsafe_allow_html=True)
                st.markdown(
                    f'<div class="kmeans-table-container">{data_html}</div>', unsafe_allow_html=True)

                # Hiển thị Vector trọng tâm dưới dạng bảng
                st.markdown('<h2>Vector trọng tâm:</h2>',
                            unsafe_allow_html=True)

                # Chuyển đổi các vector trọng tâm thành DataFrame
                centroids = kmeans.cluster_centers_  # Vector trọng tâm

                # Đổi tên cột cho phù hợp với yêu cầu
                # Giả sử dữ liệu có 2 chiều (x, y)
                centroids_df = pd.DataFrame(centroids, columns=["x", "y"])
                centroids_df.insert(0, 'Trọng tâm các cụm', [
                                    f'Cụm {i+1}' for i in range(len(centroids_df))])

                # CSS tùy chỉnh cho bảng Vector trọng tâm
                custom_centroid_table_css = """
                    <style>
                        .centroid-table-container {
                            display: flex;
                            justify-content: center; /* Căn giữa bảng */
                            align-items: center;
                            margin: 20px auto; /* Căn giữa bảng */
                            max-width: 100%; /* Giới hạn chiều rộng */
                            overflow-x: auto; /* Thêm cuộn ngang nếu bảng quá rộng */
                        }
                        .centroid-table {
                            border-collapse: collapse;
                            font-size: 16px; /* Kích thước chữ */
                            font-family: Arial, sans-serif;
                            width: 100%; /* Chiếm toàn bộ chiều rộng khung */
                            text-align: center;
                            border: 1px solid #ddd; /* Viền bảng */
                            color: #023047;
                        }

                        .centroid-table th {
                            background-color: #126782; /* Màu nền tiêu đề */
                            color: #FFFFFF; /* Màu chữ tiêu đề */
                            padding: 10px;
                            text-align: center;
                        }

                        .centroid-table td {
                            padding: 8px 10px;
                            text-align: center;
                        }

                        .centroid-table tr:nth-child(even) {
                            background-color: #f3f3f3; /* Màu nền dòng chẵn */
                        }

                        .centroid-table tr:nth-child(odd) {
                            background-color: #ffffff; /* Màu nền dòng lẻ */
                        }

                        .centroid-table tr:hover {
                            background-color: #FFB703; /* Màu nền khi hover */
                            color: #000000; /* Màu chữ khi hover */
                        }
                    </style>
                """

                # Chuyển DataFrame thành HTML với class để hiển thị bảng
                centroid_table_html = centroids_df.to_html(
                    index=False,
                    classes='centroid-table',  # Thêm class để áp dụng CSS
                    border=0
                )

                # Hiển thị CSS và bảng HTML
                st.markdown(custom_centroid_table_css, unsafe_allow_html=True)
                st.markdown(f'<div class="centroid-table-container">{
                            centroid_table_html}</div>', unsafe_allow_html=True)

                # Hiển thị biểu đồ K-means
                st.markdown('<h2>Biểu đồ K-means:</h2>',
                            unsafe_allow_html=True)
                plt.figure(figsize=(8, 6))
                plt.scatter(data.iloc[:, 0], data.iloc[:, 1],
                            c=kmeans.labels_, cmap='viridis')
                plt.title("K-means Clustering")
                plt.xlabel(data.columns[0])
                plt.ylabel(data.columns[1])
                plt.colorbar(label='Cluster')
                st.pyplot(plt)

        elif algorithm == "Kohonen":
            map_width = st.number_input(
                "Chiều rộng bản đồ (Width):", min_value=1, step=1, value=5)
            map_height = st.number_input(
                "Chiều cao bản đồ (Height):", min_value=1, step=1, value=5)
            num_epochs = st.number_input(
                "Số lần lặp (Epochs):", min_value=1, step=1, value=100)
            alpha = st.number_input("Tốc độ học (Alpha):",
                                    min_value=0.01, max_value=1.0, step=0.01, value=0.5)
            neighborhood_radius = st.number_input(
                "Bán kính vùng lân cận:", min_value=1, step=1, value=2)

            if st.button("Thực hiện Kohonen", key="kohonen"):
                # Chuẩn bị dữ liệu
                data_values = data.values
                data_values = (data_values - np.mean(data_values, axis=0)
                               ) / np.std(data_values, axis=0)

                # Huấn luyện Kohonen SOM
                som = MiniSom(map_width, map_height,
                              data_values.shape[1], sigma=neighborhood_radius, learning_rate=alpha)
                som.random_weights_init(data_values)
                som.train_random(data_values, num_epochs)

                # Gắn cụm
                # each label is a tuple (x, y) coordinate
                labels = [som.winner(x) for x in data_values]
                # Creating a string key for clusters
                data["Gom cụm"] = [f"{x[0]}-{x[1]}" for x in labels]

                # Hiển thị kết quả Kohonen dưới dạng bảng
                st.markdown(
                    '<h2 style="margin-bottom: -40px;">Kết quả Kohonen:</h2>', unsafe_allow_html=True)

                # Chuyển đổi dữ liệu thành HTML bảng với CSS tùy chỉnh
                custom_table_css = """
                    <style>
                        .kohonen-table-container {
                            display: flex;
                            justify-content: center; /* Căn giữa bảng */
                            align-items: center;
                            margin: 0 auto; /* Tự động căn giữa */
                            max-width: 100%; /* Giới hạn chiều rộng */
                            overflow-x: auto; /* Thêm cuộn ngang nếu bảng quá lớn */
                        }
                        .kohonen-table {
                            border-collapse: collapse;
                            font-size: 16px; /* Kích thước chữ */
                            font-family: Arial, sans-serif;
                            width: 100%; /* Chiều rộng bảng */
                            text-align: center;
                            border: 1px solid #ddd; /* Viền bảng */
                            color: #023047;
                            margin: 20px auto; /* Khoảng cách giữa bảng và các phần tử khác */
                        }

                        .kohonen-table th {
                            background-color: #126782; /* Màu nền tiêu đề */
                            color: #FFFFFF; /* Màu chữ tiêu đề */
                            padding: 10px;
                            text-align: center;
                        }

                        .kohonen-table td {
                            padding: 8px 10px;
                            text-align: center;
                        }

                        .kohonen-table tr:nth-child(even) {
                            background-color: #f3f3f3; /* Màu nền dòng chẵn */
                        }

                        .kohonen-table tr:nth-child(odd) {
                            background-color: #ffffff; /* Màu nền dòng lẻ */
                        }

                        .kohonen-table tr:hover {
                            background-color: #FFB703; /* Màu nền khi hover */
                            color: #000000; /* Màu chữ khi hover */
                        }
                    </style>
                """

                # Chuyển đổi dataframe thành HTML với class
                data_html = data.to_html(
                    index=False,
                    classes='kohonen-table',
                    border=0
                )

                # Hiển thị bảng kết quả với CSS
                st.markdown(custom_table_css, unsafe_allow_html=True)
                st.markdown(
                    f'<div class="kohonen-table-container">{data_html}</div>', unsafe_allow_html=True)

                # Hiển thị Trọng số các nút dưới dạng bảng
                st.markdown('<h2>Trọng số các nút:</h2>',
                            unsafe_allow_html=True)

                weights_matrix = som.get_weights()

                # Tạo bảng từ trọng số
                weights_table = []
                for i, weights in enumerate(weights_matrix):
                    row = {f"Nút {j}": weights[j] for j in range(len(weights))}
                    weights_table.append(row)

                # Chuyển đổi sang DataFrame để dễ xử lý
                weights_df = pd.DataFrame(weights_table)

                # Tạo HTML cho bảng
                table_html = weights_df.to_html(
                    index=True,
                    classes='styled-table',  # Thêm class để áp dụng CSS
                    border=0  # Bỏ viền mặc định của bảng
                )

                # CSS tùy chỉnh với kích thước bảng nhỏ hơn
                custom_css = """
                    <style>
                        .styled-table-container {
                            display: flex;
                            justify-content: center; /* Căn giữa bảng */
                            align-items: center;
                            margin: 0 auto; /* Tự động căn giữa */
                            max-width: 100%; /* Giới hạn chiều rộng tối đa */
                        }
                        .styled-table {
                            border-collapse: collapse;
                            font-size: 16px; /* Giảm kích thước chữ */
                            font-family: Arial, sans-serif;
                            width: 100%; /* Bảng chiếm toàn bộ khung div */
                            text-align: center;
                            border: 1px solid #ddd; /* Viền bảng */
                            color: #126782;
                            margin: 0 auto; /* Tự động căn giữa */
                        }

                        .styled-table th, .styled-table td {
                            padding: 10px 15px;
                            text-align: center;
                        }

                        .styled-table th {
                            background-color: #126782; /* Màu nền tiêu đề */
                            color: #FFFFFF; /* Màu chữ tiêu đề */
                            position: sticky;
                            top: 0; /* Cố định tiêu đề khi cuộn */
                            z-index: 2; /* Đặt trên các dòng khác */
                        }

                        .styled-table td:first-child {
                            position: sticky;
                            left: 0; /* Cố định cột đầu tiên khi cuộn ngang */
                            background-color: #f3f3f3; /* Đặt màu nền riêng cho cột cố định */
                            z-index: 1; /* Đảm bảo nằm dưới tiêu đề */
                        }

                        .styled-table tr:nth-child(even) {
                            background-color: #f3f3f3; /* Màu nền dòng chẵn */
                        }

                        .styled-table tr:nth-child(odd) {
                            background-color: #ffffff; /* Màu nền dòng lẻ */
                        }

                        .styled-table tr:hover {
                            background-color: #FFB703; /* Màu nền khi hover */
                            color: #000000; /* Màu chữ khi hover */
                        }
                    </style>

                """

                # Hiển thị CSS và bảng HTML trong div có kích thước cụ thể
                st.markdown(custom_css, unsafe_allow_html=True)
                st.markdown(
                    f'<div class="styled-table-container">{table_html}</div>', unsafe_allow_html=True)

                # Hiển thị nhận xét
                st.markdown("<h3>Chú thích:</h3>", unsafe_allow_html=True)
                st.write("""
                - Mỗi hàng trong bảng tương ứng với một hàng (row) trên bản đồ Kohonen.
                - Các cột trong bảng tương ứng với các nút trên bản đồ, với mỗi nút có một vector trọng số (weights).
                - Sự khác biệt giữa các giá trị trọng số cho thấy cách SOM đã học và tổ chức dữ liệu. 
                - Các nút gần nhau trên bản đồ Kohonen thường có giá trị trọng số tương tự, phản ánh dữ liệu trong các cụm liên quan.
                """)

                # Hiển thị biểu đồ Kohonen SOM
                st.markdown('<h2>Biểu đồ Kohonen SOM:</h2>',
                            unsafe_allow_html=True)
                plt.figure(figsize=(8, 6))

                # Flatten the coordinates of the labels
                # x-coordinate from (x, y) tuples
                x_vals = [label[0] for label in labels]
                # y-coordinate from (x, y) tuples
                y_vals = [label[1] for label in labels]

                # Color map based on clusters
                cluster_labels = [som.winner(x)[0] * som.get_weights().shape[1] + som.winner(x)[
                    1] for x in data_values]  # flatten cluster index
                plt.scatter(x_vals, y_vals, c=cluster_labels,
                            cmap='viridis', marker='o')

                plt.title("Kohonen SOM Clustering")
                plt.xlabel("X")
                plt.ylabel("Y")
                plt.colorbar(label='Cluster')
                st.pyplot(plt)
    else:
        # Nếu chưa tải lên file
        st.warning("Vui lòng tải file CSV để tiếp tục.")
