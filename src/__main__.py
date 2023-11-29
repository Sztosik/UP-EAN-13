import streamlit as st


# center barcode image when full screan
st.markdown(
    """
    <style>
        button[title^=Exit]+div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)


st.title('Generator kodów EAN-13')
st.number_input('', min_value=0, max_value=9_999_999_999_999, step=1, key=id)

col1, col2, col3 = st.columns(3)
with col2:
    st.image('./ean_barcodes_img/example.png')