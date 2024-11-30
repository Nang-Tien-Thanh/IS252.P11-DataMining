import streamlit as st
sys.path.insert(0, './page')  # Đưa thư mục 'page' vào đường dẫn tìm kiếm module

# Import các trang từ thư mục 'page'
import Classification
import Cluster

# Tạo sidebar với các lựa chọn
st.sidebar.title("Chọn tính năng")

# Các lựa chọn trong sidebar
option = st.sidebar.radio("Điều hướng", ("Cây quyết định", "Gom cụm"))

# Điều hướng đến trang tương ứng khi người dùng chọn
if option == "Cây quyết định":
    Classification.app()  # Gọi hàm app trong Class.py
else if option == "Gom cụm":
    Cluster.app()  # Gọi hàm app trong Gomcum.py
