from dataclasses import dataclass

import cv2 as cv
import numpy as np
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
    """,
    unsafe_allow_html=True,
)


IMG_WIDTH_PX = 512
IMG_HEIGHT_PX = 256

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

EAN13_SAVE_PATH = "./ean_barcodes_img/ean13.png"


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)



B = {
    0 : (0, 1, 0, 0, 1, 1, 1),
    1 : (0, 1, 1, 0, 0, 1, 1),
    2 : (0, 0, 1, 1, 0, 1, 1),
    3 : (0, 1, 0, 0, 0, 0, 1),
    4 : (0, 0, 1, 1, 1, 0, 1),
    5 : (0, 1, 1, 1, 0, 0, 1),
    6 : (0, 0, 0, 0, 1, 0, 1),
    7 : (0, 0, 1, 0, 0, 0, 1),
    8 : (0, 0, 0, 1, 0, 0, 1),
    9 : (0, 0, 1, 0, 1, 1, 1)
}

def calc_crc() -> int:
    pass


def split_into_digits() -> list[int]:
    pass


def draw_ean_barcode(digits: list[int]):
    if len(digits) != 12:
        raise ValueError
    pass


# Create a white image
img = np.zeros((IMG_HEIGHT_PX, IMG_WIDTH_PX, 3), np.uint8)
img.fill(255)

# Draw a black line with thickness of 5 px
cv.line(img, Point(x=50, y=10).to_tuple(), Point(x=50, y=246).to_tuple(), BLACK, 5)
cv.imwrite(EAN13_SAVE_PATH, img)

with st.container():
    st.subheader("Urządzenia Peryferyjne")
    st.title("Generator kodów EAN-13")
    st.number_input("", min_value=0, max_value=999_999_999_999, step=1)

col1, col2, col3 = st.columns(3)
with col2:
    # display image
    st.image("./ean_barcodes_img/example.png")

    # display download button
    with open("./ean_barcodes_img/example.png", "rb") as file:
        st.download_button(
            label="Pobierz",
            data=file,
            file_name="./ean_barcodes_img/example.png",
            mime="image/png",
        )
