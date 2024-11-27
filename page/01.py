import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Cấu hình trang Streamlit
st.set_page_config(page_title="My App", layout="wide", initial_sidebar_state="collapsed")

# Hiển thị thông báo hoặc mô tả
st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(circle at 30% 30%, rgba(0, 120, 160, 0.6), transparent 70%),
                radial-gradient(circle at 70% 70%, rgba(214, 90, 0, 0.6), transparent 70%),
                linear-gradient(to right, #000000, #1a1a1a);
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: white;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        header {
            width: 1280px;
            height: 101px;
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.52);
            border-radius: 60px;
            margin: 50px auto;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }

        #icon {
            all: unset;
            width: 68px;
            height: 68px;
            color: white;
            margin-left: 10px;
            display: flex;
            justify-content: left;
            align-items: center;
        }

        header h1 {
            font-size: 36px;
            font-weight: 800px;
            text-align: center;
            margin: 0;
            color: white;
        }

        .input {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            margin: 0 70px 50px;
        }

        .go {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 50px;
        }

        label {
            font-size: 28px;
            font-weight: 500;
            margin-right: 15px;
        }

        .file-input {
            display: none;
        }

        .add-file-button {
            background: linear-gradient(to right, #FFB703, #CD9302, #996E02);
            color: #023047;
            width: 125px;
            height: 100%;
            border: none;
            border-radius: 10px;
            padding: 10px 15px;
            font-family: 'Inter', sans-serif;
            font-weight: 500px;
            font-size: 24px;
            cursor: pointer;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        }

        select {
            background: #d9d9d9;
            color: #023047;
            height: 50px;
            border: none;
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 16px;
            cursor: pointer;
            text-align: left;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        }

        button {
            background: linear-gradient(to right, #FFB703, #CD9302, #996E02);
            color: #023047;
            width: 313px;
            height: 58px;
            border: none;
            padding: 10px 15px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            font-size: 24px;
            cursor: pointer;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        }

        button:hover {
            background: linear-gradient(to right, #CD9302, #996E02);
        }

        footer {
            width: 1280px;
            height: 600px;
            margin-bottom: 20px;
            padding: 10px;
            background: #d9d9d9 0.2;
            border-radius: 40px;
            border: 1px solid #fbfbfb;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        footer p {
            margin-top: 2px;
            margin-left: 5px;
            font-size: 32px;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
        }
            
        .stDataFrame tbody td {
            background-color: #f5f5f5;
            text-align: center;  /* Căn giữa */
            font-weight: bold;   /* Đậm tiêu đề */
            color: black;        /* Màu chữ */
        }

        .stDataFrame thead th {
            background-color: #2D9CDB;  /* Màu nền tiêu đề bảng */
            color: white;               /* Màu chữ tiêu đề */
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

# Giao diện nhập liệu
st.markdown("<header><h1>Tập phổ biến và luật kết hợp</h1></header>", unsafe_allow_html=True)

# Input file và thuật toán chọn
st.markdown('<div class="input">', unsafe_allow_html=True)
st.markdown("<label>Nhập file:</label>", unsafe_allow_html=True)
file = st.file_uploader("Chọn tệp tin", type=['csv', 'xlsx'])
st.markdown("<label>Chọn thuật toán:</label>", unsafe_allow_html=True)

# Dropdown cho thuật toán
dropdown_html = """
<select id="dropdown-menu">
    <option value="" disabled selected></option>
    <option value="frequent_itemsets">Tìm tập phổ biến và luật kết hợp</option>
    <option value="maximal_itemsets">Tìm tập phổ biến tối đại</option>
    <option value="association_rules">Độ tin cậy của luật kết hợp</option>
</select>
"""
st.markdown(dropdown_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Giao diện nhập liệu: Hiển thị label cho minsupp
st.markdown("<label>Nhập minsupp (Sự hỗ trợ tối thiểu)</label>", unsafe_allow_html=True)

# Nhập giá trị minsupp (sự hỗ trợ tối thiểu), không sử dụng label trong st.number_input
minsupp = st.number_input(
    label="Nhập minsupp (Sự hỗ trợ tối thiểu)",
    min_value=0.0,  # Giá trị nhỏ nhất
    max_value=1.0,  # Giá trị lớn nhất
    value=0.1,      # Giá trị mặc định
    step=0.01       # Bước nhảy giữa các giá trị
)

mincoff = st.number_input(
    label="Nhập mincoff (Độ tin cậy tối thiểu)",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01
)

def find_maximal_frequent_itemsets(frequent_itemsets):
    """
    Hàm tìm các tập phổ biến tối đại từ các tập phổ biến.
    """
    maximal_itemsets = []
    for index, itemset in frequent_itemsets.iterrows():
        is_maximal = True
        for sub_index, sub_itemset in frequent_itemsets.iterrows():
            if itemset['itemsets'].issubset(sub_itemset['itemsets']) and itemset['support'] == sub_itemset['support']:
                is_maximal = False
                break
        if is_maximal:
            maximal_itemsets.append(itemset)
    return pd.DataFrame(maximal_itemsets)

if file is not None:
    try:
        # Bước 2: Đọc tệp và chuyển thành DataFrame
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            st.error("Chỉ hỗ trợ tệp CSV và XLSX.")

        # Bước 3: Chuyển DataFrame thành bảng HTML
        df_html = df.to_html(classes="table table-striped table-bordered", index=False)

        # Bước 4: Hiển thị bảng HTML trong Streamlit
        st.markdown("""
            <style>
                .table {
                    width: 100%;
                    height: 400px;
                    overflow-y: scroll;
                    border-collapse: collapse;
                }
                .table thead th {
                    background-color: #4285f4;
                    color: white;
                    padding: 10px;
                    text-align: center;
                }
                .table tbody td {
                    padding: 10px;
                    text-align: center;
                    border-bottom: 1px solid #ddd;
                }
            </style>
            """, unsafe_allow_html=True)
        st.markdown(df_html, unsafe_allow_html=True)
        # Chuyển đổi dữ liệu
    itemsets = df.groupby('Ma_hoa_don')['Ma_hang'].apply(set).reset_index(name='itemsets')

    # Hiển thị kết quả thuật toán
    if dropdown_html == "apriori":
        te = TransactionEncoder()
        te_ary = te.fit(itemsets['itemsets']).transform(itemsets['itemsets'])
        df_ary = pd.DataFrame(te_ary, columns=te.columns_)

        # Áp dụng Apriori
        frequent_itemsets = apriori(df_ary, min_support=min_support, use_colnames=True)
        st.write(frequent_itemsets)
        
    elif dropdown_html == "maximal":
        st.write("Maximal Itemsets chưa được cài đặt")
        
    elif dropdown_html == "rules":
        frequent_itemsets = apriori(df_ary, min_support=min_support, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_threshold)
        st.write(rules)
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")
