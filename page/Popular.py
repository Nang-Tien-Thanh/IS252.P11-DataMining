import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Cấu hình trang Streamlit
st.set_page_config(page_title="Phân tích luật kết hợp",
                   layout="wide", initial_sidebar_state="expanded")


def app():
    # CSS Tùy chỉnh
    st.markdown("""
    <style>
        /* Toàn bộ ứng dụng */
        /* CSS Tùy chỉnh */
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

    /* Khu vực tải file */
    .file-uploader {
        color: white;
        font-size: 30px;
        width: 80%;
        max-width: 500px;
    }

    /* Tiêu đề */
    .container {
        width: 704px; 
        height: 101px;
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.52);
        border-radius: 60px;
        margin: 50px auto;
        margin-top: 200px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }
            
    .container h1 {
        font-size: 40px;  /* Chỉnh cỡ chữ tiêu đề lớn hơn */
        font-weight: 800px;
        text-align: center;
        margin: 0;
        color: white;
    }

    /* Bảng dữ liệu */
    .dataframe {
        width: 90%;
        margin: 30px auto;
        border-collapse: collapse;
        font-size: 18px;  /* Chỉnh kích thước chữ trong bảng lớn hơn */
        background-color: rgba(0, 0, 0, 0.7);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border-radius: 8px;
    }

    .dataframe thead {
        background-color: #FFB703;
        color: white;
        font-weight: bold;
        font-size: 20px; /* Cỡ chữ tiêu đề bảng lớn hơn */
    }

    .dataframe th, .dataframe td {
        border: 1px solid #023047;
        padding: 12px;
        text-align: center;
        font-size: 18px; /* Chỉnh kích thước chữ trong ô bảng */
    }

    .dataframe tr:nth-child(even) {
        background-color: rgba(255, 255, 255, 0.1);
    }

    .dataframe tr:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }

    /* Các phần tử select và input */
    input[type="number"], select {
        padding: 12px;
        font-size: 18px; /* Chỉnh cỡ chữ trong select và input */
        margin: 12px;
        border-radius: 6px;
        border: 1px solid #023047;
        background-color: #FFFFFF;
        color: #023047;
        cursor: pointer;
    }

    /* Nút và các input */
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
        background: linear-gradient(to right, #CD9302, #996E02);
    }
            
    /* Kết quả phần tử */
    .result-container {
        background-color: #996E02;
        color: white;
        padding: 15px;
        margin-top: 20px;
        border-radius: 8px;
        font-size: 20px; /* Cỡ chữ trong kết quả lớn hơn */
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header với CSS container
    st.markdown("""
    <div class="container">
        <h1>Tập phổ biến và luật kết hợp</h1>
    </div>
    """, unsafe_allow_html=True)

    # Khu vực tải file
    st.markdown("<div class='file-uploader'><strong>1. Chọn tệp tin:</strong></div>",
                unsafe_allow_html=True)
    file = st.file_uploader(
        "Chọn tệp dữ liệu (CSV hoặc XLSX)", type=['csv', 'xlsx'])

    # Nếu có file được tải lên
    if file is not None:
        try:
            # Đọc file
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)

            # Kiểm tra dữ liệu
            if "Ma_hoa_don" not in df.columns or "Ma_hang" not in df.columns:
                st.markdown(
                    "<p class='error'>Tệp tin cần có các cột: 'Ma_hoa_don' và 'Ma_hang'.</p>", unsafe_allow_html=True)
            else:
                st.write("**Dữ liệu đã tải lên:**")
                # Sử dụng markdown để hiển thị bảng với lớp CSS đã chỉnh sửa
                st.markdown(f"<table class='dataframe'>{df.to_html(
                    index=False)}</table>", unsafe_allow_html=True)

                # Chọn thuật toán
                st.markdown("### 2. Chọn thuật toán phân tích:")
                option = st.selectbox(
                    "Chọn thuật toán bạn muốn thực hiện:",
                    options=["", "Tìm tập phổ biến",
                             "Tìm tập phổ biến tối đại", "Phân tích luật kết hợp"]
                )

                # Các tham số đầu vào
                if option in ["Tìm tập phổ biến", "Tìm tập phổ biến tối đại"]:
                    minsupp = st.number_input(
                        "Nhập giá trị minsupp (0.01 - 1.0):",
                        min_value=0.01, max_value=1.0, value=0.1, step=0.01
                    )
                elif option == "Phân tích luật kết hợp":
                    minsupp = st.number_input(
                        "Nhập giá trị minsupp (0.01 - 1.0):",
                        min_value=0.01, max_value=1.0, value=0.1, step=0.01
                    )
                    mincoff = st.number_input(
                        "Nhập giá trị mincoff (0.01 - 1.0):",
                        min_value=0.01, max_value=1.0, value=0.5, step=0.01
                    )

                # Nút chạy thuật toán
                if st.button("Chạy thuật toán"):
                    # Tiền xử lý dữ liệu
                    transactions = df.groupby('Ma_hoa_don')[ 
                        'Ma_hang'].apply(list).tolist()
                    te = TransactionEncoder()
                    te_ary = te.fit(transactions).transform(transactions)
                    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

                    # Thực thi thuật toán
                    if option == "Tìm tập phổ biến":
                        frequent_itemsets = apriori(
                            df_encoded, min_support=minsupp, use_colnames=True)
                        st.markdown(
                            "<div class='result-container'><strong>Kết quả: Tập phổ biến</strong></div>", unsafe_allow_html=True)
                        st.markdown(f"<table class='dataframe'>{frequent_itemsets.to_html(
                            index=False)}</table>", unsafe_allow_html=True)

                    elif option == "Tìm tập phổ biến tối đại":
                        frequent_itemsets = apriori(
                            df_encoded, min_support=minsupp, use_colnames=True)

                        # Tìm các tập phổ biến tối đại
                        max_itemsets = []
                        for idx, itemset in frequent_itemsets.iterrows():
                            itemset_list = list(itemset['itemsets'])
                            is_maximal = True
                            for sub_idx, sub_itemset in frequent_itemsets.iterrows():
                                # Kiểm tra nếu tập con lớn hơn tập hiện tại và cũng là tập phổ biến
                                if len(itemset_list) < len(sub_itemset['itemsets']) and set(itemset_list).issubset(sub_itemset['itemsets']):
                                    is_maximal = False
                                    break
                            if is_maximal:
                                max_itemsets.append(itemset)

                        max_itemsets_df = pd.DataFrame(max_itemsets)
                        st.markdown(
                            "<div class='result-container'><strong>Kết quả: Tập phổ biến tối đại</strong></div>", unsafe_allow_html=True)
                        st.markdown(f"<table class='dataframe'>{max_itemsets_df.to_html(
                            index=False)}</table>", unsafe_allow_html=True)

                    elif option == "Phân tích luật kết hợp":
                        frequent_itemsets = apriori(df_encoded, min_support=minsupp, use_colnames=True)
                        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=mincoff)

                        # Thêm cột 'Rule' để tạo tên luật (R1, R2, ...)
                        rules['Rule'] = ['R' + str(i+1) for i in range(len(rules))]

                        # Lọc ra các cột cần hiển thị: Rule, Input (antecedents), và Confidence (CF)
                        rules_display = rules[['Rule', 'antecedents', 'consequents', 'confidence']]

                        # Chuyển 'frozenset' thành chuỗi không có từ "frozenset"
                        rules_display['antecedents'] = rules_display['antecedents'].apply(lambda x: ', '.join(list(x)))
                        rules_display['consequents'] = rules_display['consequents'].apply(lambda x: ', '.join(list(x)))


                        # Thực hiện in ra bảng nếu có
                        if len(rules_display) > 0:
                            st.markdown(
                                "<div class='result-container'><strong>Kết quả: Phân tích luật kết hợp</strong></div>", unsafe_allow_html=True)
                            # Áp dụng font đỏ vào các dòng có Confidence > mincoff
                            html_table = rules_display.style.applymap(
                                lambda x: 'font-weight: bold; color: red;', subset=['confidence'])

                            st.markdown(f"<table class='dataframe'>{html_table.to_html()}</table>", unsafe_allow_html=True)


                        else:
                            st.markdown(
                                "<div class='result-container'><strong>Không có luật kết hợp thỏa mãn!</strong></div>", unsafe_allow_html=True)

        except Exception as e:
            st.write(f"Đã xảy ra lỗi: {str(e)}")
