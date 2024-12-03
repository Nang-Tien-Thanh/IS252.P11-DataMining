import streamlit as st
import pandas as pd

# Cấu hình trang Streamlit
# st.set_page_config(page_title="Tập thô",
#                    layout="wide", initial_sidebar_state="expanded")
# Tiêu đề ứng dụng
st.markdown('<div class="head-title">Tập thô</div>', unsafe_allow_html=True)


def app():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-sizing: border-box;
            width: 100%;
            height: 1868px;
            font-family: 'Inter', sans-serif;
            position: relative;
            margin: 0px auto;
                
            background-image: url('D:/IS252.P11-DataMining-main/page/image/background1.png');
            background-size: cover;  /* Phóng to ảnh để bao phủ màn hình */
            background-repeat: no-repeat;
            background-position: center center;
            # background-attachment: fixed; /* Cố định nền khi cuộn */
            }
                
                /* Chỉnh hình nền cho toàn màn hình */
            .stApp {
                background: radial-gradient(circle at 30% 30%, rgba(0, 120, 160, 0.6), transparent 70%),
                radial-gradient(circle at 70% 70%, rgba(214, 90, 0, 0.6), transparent 70%),
                linear-gradient(to right, #000000, #1a1a1a);
                background-size: cover;
                background-attachment: fixed;
                margin: 0;
                font-family: 'Inter', sans-serif;
                color: white;
                height: cover;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                flex-wrap: wrap;
            }

            .head-title {
                display: flex;
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
                justify-content: center;
                align-items: center;
                padding: 16px 46px;

                font-family: 'Inter';
                font-style: normal;
                font-weight: 800;
                font-size: 40px;
                line-height: 67px;
                color: #FFFFFF;

                width: 100%;
                height: 100px;

                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.52);
                border-radius: 60px;
            }
                
            /* Tùy chỉnh nút tải lên file */
            div.stButton > button {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 4px 18px;
                gap: 10px;

                background: linear-gradient(90deg, #FFB703 0%, #CD9302 44%, #996E02 90.5%);
                border: none;
                border-radius: 10px;

                font-family: 'Inter', sans-serif;
                font-style: normal;
                font-weight: 600;
                font-size: 24px;
                line-height: 29px;
                letter-spacing: -0.03em;

                color: #023047;
                cursor: pointer;
            }

            /* Khi hover nút */
            div.stButton > button:hover {
                background: linear-gradient(90deg, #CD9302 0%, #996E02 50%, #FFB703 100%);
                color: #023047;
            }
                
            div.stButton > button:active {
                color: #023047;
            }

            .container {
                margin-top: 20px;
            }
            label {
                font-size: 16px;
                color: #555;
            }
        </style>
        
        
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
            Tập thô
        </div>
        
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Tải lên file Excel", type=["xlsx"])

    if uploaded_file is not None:
        # Đọc dữ liệu từ file Excel
        df = pd.read_excel(uploaded_file)

        # Mapping dữ liệu định tính sang số
        mapping = {
            "Bằng cấp": {"Trung cấp": 1, "Đại học": 2, "Cao học": 3},
            "Kinh Nghiệm": {"Ít": 1, "Trung bình": 2, "Nhiều": 3},
            "Tiếng anh": {"Không": 0, "Biết": 1},
            "Phỏng vấn": {"Bình thường": 1, "Tốt": 2, "Xuất sắc": 3},
            "Tuyển dụng": {"Từ chối": 0, "Chấp nhận": 1}
        }
        reverse_mapping = {col: {v: k for k, v in mapping.items()}
                           for col, mapping in mapping.items()}

        for col, col_mapping in mapping.items():
            if col in df.columns:
                df[col] = df[col].map(col_mapping)

        # Lấy danh sách các cột thuộc tính
        columns = df.columns.tolist()
        decision_column = columns[-1]  # Cột thuộc tính quyết định (cuối cùng)
        attributes = columns[1:-1]  # Các thuộc tính (trừ cột quyết định)

        # Bước 2: Chọn phương pháp tính
        st.markdown('<div class="container">', unsafe_allow_html=True)
        selected_method = st.selectbox(
            "Chọn phương pháp tính",
            ["Tính xấp xỉ", "Khảo sát sự phụ thuộc", "Tính các rút gọn"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Giao diện theo từng phương pháp
        if selected_method == "Tính xấp xỉ":
            # Chọn tập thuộc tính
            st.markdown(
                '<label for="tap-thuoc-tinh">Chọn tập thuộc tính:</label>', unsafe_allow_html=True)
            selected_attributes = st.multiselect(
                "Chọn tập thuộc tính", attributes)

            # Tạo từ điển ánh xạ ngược từ số sang chữ (reverse mapping)
            reverse_mapping_decision = {v: k for k,
                                        v in mapping[decision_column].items()}

            # Lấy danh sách các giá trị thuộc tính quyết định dưới dạng chữ
            unique_decision_values = [reverse_mapping_decision[val]
                                      for val in df[decision_column].dropna().unique()]

            # Hiển thị dropdown với giá trị chữ
            decision_value_label = st.selectbox(
                "Chọn giá trị của thuộc tính quyết định",
                unique_decision_values
            )

            # Chuyển giá trị được chọn từ chữ về số để tính toán
            decision_value = {v: k for k, v in reverse_mapping_decision.items()}[
                decision_value_label]

        elif selected_method == "Khảo sát sự phụ thuộc":
            # Chọn tập thuộc tính
            st.markdown(
                '<label for="tap-thuoc-tinh">Chọn tập thuộc tính:</label>', unsafe_allow_html=True)
            selected_attributes = st.multiselect(
                "Chọn tập thuộc tính", attributes)

        # Nút tính toán
        if st.button("Thực hiện"):
            if selected_method == "Tính xấp xỉ":
                if not selected_attributes:
                    st.write("Vui lòng chọn tập thuộc tính.")
                else:
                    # Hàm tính xấp xỉ dưới
                    def approximation_lower(df, attributes, decision_value):
                        lower_indices = []
                        for idx, row in df.iterrows():
                            attribute_values = tuple(row[attributes])
                            subset = df[(df[attributes] == attribute_values).all(
                                axis=1)][decision_column]
                            if (subset == decision_value).all():
                                lower_indices.append(idx + 1)  # Lưu số thứ tự
                        return len(lower_indices), lower_indices

                    # Hàm tính xấp xỉ trên
                    def approximation_upper(df, attributes, decision_value):
                        upper_indices = []
                        for idx, row in df.iterrows():
                            attribute_values = tuple(row[attributes])
                            subset = df[(df[attributes] == attribute_values).all(
                                axis=1)][decision_column]
                            if decision_value in subset.values:
                                upper_indices.append(idx + 1)  # Lưu số thứ tự
                        return len(upper_indices), upper_indices

                    # Tính toán xấp xỉ
                    lower_count, lower_set = approximation_lower(
                        df, selected_attributes, decision_value)
                    upper_count, upper_set = approximation_upper(
                        df, selected_attributes, decision_value)
                    st.write(f"Xấp xỉ dưới: {lower_count}, tập giá trị: {
                             set(lower_set)}")
                    st.write(f"Xấp xỉ trên: {upper_count}, tập giá trị: {
                             set(upper_set)}")

            elif selected_method == "Khảo sát sự phụ thuộc":
                if not selected_attributes:
                    st.write("Vui lòng chọn tập thuộc tính.")
                else:
                    # Lấy cột quyết định (cột cuối cùng)
                    decision_column = columns[-1]
                    df = df.dropna(subset=selected_attributes +
                                   [decision_column])  # Loại bỏ giá trị NaN

                    # Hàm tính xấp xỉ dưới
                    def approximation_lower(df, attributes, decision_column):
                        lower_set = []
                        for _, row in df.iterrows():
                            attribute_values = tuple(row[attributes])
                            decision_value = row[decision_column]
                            subset = df[(df[attributes] == attribute_values).all(
                                axis=1)][decision_column]
                            if (subset == decision_value).all():
                                lower_set.append(1)
                            else:
                                lower_set.append(0)
                        return sum(lower_set)

                    # Hàm tính xấp xỉ trên
                    def approximation_upper(df, attributes, decision_column):
                        upper_set = []
                        for _, row in df.iterrows():
                            attribute_values = tuple(row[attributes])
                            subset = df[(df[attributes] == attribute_values).all(
                                axis=1)][decision_column]
                            upper_set.append(len(subset))
                        return sum(upper_set)

                    # Tính toán theo phương pháp đã chọn
                    lower_approximation = approximation_lower(
                        df, selected_attributes, decision_column)
                    upper_approximation = approximation_upper(
                        df, selected_attributes, decision_column)

                    # Tính hệ số phụ thuộc
                    k = lower_approximation / \
                        len(df) if len(df) > 0 else 0  # Hệ số phụ thuộc
                    st.write(f"Hệ số phụ thuộc (k): {k:.2f}")

                    # Tính độ chính xác
                    accuracy = lower_approximation / \
                        upper_approximation if upper_approximation != 0 else 0
                    st.write(f"Độ chính xác: {accuracy:.2f}")

            elif selected_method == "Tính các rút gọn":
                # Loại bỏ cột đầu tiên để không xét nó khi tìm rút gọn
                columns = df.columns
                decision_column = columns[-1]  # Cột quyết định
                # Chỉ lấy các thuộc tính (bỏ cột đầu tiên và cột quyết định)
                attributes = columns[1:-1]

                # Hàm tìm rút gọn (reduct)

                def find_reducts(df, decision_column, attributes):
                    reducts = []  # Danh sách các tập rút gọn

                    # Lấy tất cả các tổ hợp thuộc tính (rút gọn)
                    from itertools import combinations
                    for r in range(1, len(attributes) + 1):
                        for subset in combinations(attributes, r):
                            # Kiểm tra nếu tập thuộc tính này có khả năng phân biệt tất cả các đối tượng
                            grouped = df.groupby(list(subset))[
                                decision_column].nunique()
                            if grouped.eq(1).all():
                                reducts.append(set(subset))  # Lưu tập rút gọn

                    # Loại bỏ các tập dư thừa (không cần thiết)
                    minimal_reducts = []
                    for reduct in reducts:
                        if not any(reduct > other for other in reducts if reduct != other):
                            minimal_reducts.append(reduct)
                    return minimal_reducts

                # Hàm tạo luật phân lớp với dữ liệu được chuyển về dạng chữ
                def generate_classification_rules_with_reverse_mapping(df, reduct, decision_column, reverse_mapping):
                    rules = []
                    # Lọc dữ liệu theo tập rút gọn
                    for _, subset in df.groupby(list(reduct)):
                        # Tìm giá trị duy nhất của cột quyết định
                        decision_values = subset[decision_column].unique()
                        if len(decision_values) == 1:  # Đảm bảo chỉ có 1 giá trị duy nhất
                            decision_value = decision_values[0]
                            # Chuyển giá trị số sang chữ dựa trên reverse_mapping
                            decision_label = reverse_mapping[decision_column].get(
                                decision_value, decision_value)

                            # Tạo điều kiện với dữ liệu đã chuyển về dạng chữ
                            conditions = " AND ".join(
                                [
                                    f"{col} = '{reverse_mapping[col].get(
                                        subset[col].iloc[0], subset[col].iloc[0])}'"
                                    for col in reduct
                                ]
                            )
                            rules.append(f"IF {conditions} THEN {
                                         decision_column} = '{decision_label}'")
                    return rules

                # Tìm các rút gọn
                reducts = find_reducts(df, decision_column, attributes)

                # Hiển thị kết quả
                st.write("Kết quả:")
                if reducts:
                    st.write("Các rút gọn tìm được:")
                    for reduct in reducts:
                        st.write(", ".join(reduct))

                    # Chọn tập rút gọn đầu tiên để tạo luật phân lớp
                    reduct = list(reducts[0])  # Lấy rút gọn đầu tiên
                    classification_rules = generate_classification_rules_with_reverse_mapping(
                        df, reduct, decision_column, reverse_mapping
                    )

                    # Hiển thị 3 luật phân lớp đầu tiên
                    st.write("Đề xuất 3 luật phân lớp chính xác 100%:")
                    for rule in classification_rules[:3]:
                        st.write(rule)
                else:
                    st.write("Không tìm thấy rút gọn.")
