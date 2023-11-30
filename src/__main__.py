from dataclasses import dataclass
from typing import Any

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

MODULE_WIDTH_PX = 4

EAN13_SAVE_PATH = "./ean_barcodes_img/ean13.png"


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)


A = {
    "0": (0, 0, 0, 1, 1, 0, 1),
    "1": (0, 0, 1, 1, 0, 0, 1),
    "2": (0, 0, 1, 0, 0, 1, 1),
    "3": (0, 1, 1, 1, 1, 0, 1),
    "4": (0, 1, 0, 0, 0, 1, 1),
    "5": (0, 1, 1, 0, 0, 0, 1),
    "6": (0, 1, 0, 1, 1, 1, 1),
    "7": (0, 1, 1, 1, 0, 1, 1),
    "8": (0, 1, 1, 0, 1, 1, 1),
    "9": (0, 0, 0, 1, 0, 1, 1),
}

B = {
    "0": (0, 1, 0, 0, 1, 1, 1),
    "1": (0, 1, 1, 0, 0, 1, 1),
    "2": (0, 0, 1, 1, 0, 1, 1),
    "3": (0, 1, 0, 0, 0, 0, 1),
    "4": (0, 0, 1, 1, 1, 0, 1),
    "5": (0, 1, 1, 1, 0, 0, 1),
    "6": (0, 0, 0, 0, 1, 0, 1),
    "7": (0, 0, 1, 0, 0, 0, 1),
    "8": (0, 0, 0, 1, 0, 0, 1),
    "9": (0, 0, 1, 0, 1, 1, 1),
}

C = {
    "0": (1, 1, 1, 0, 0, 1, 0),
    "1": (1, 1, 0, 0, 1, 1, 0),
    "2": (1, 1, 0, 1, 1, 0, 0),
    "3": (1, 0, 0, 0, 0, 1, 0),
    "4": (1, 0, 1, 1, 1, 0, 0),
    "5": (1, 0, 0, 1, 1, 1, 0),
    "6": (1, 0, 1, 0, 0, 0, 0),
    "7": (1, 0, 0, 0, 1, 0, 0),
    "8": (1, 0, 0, 1, 0, 0, 0),
    "9": (1, 1, 1, 0, 1, 0, 0),
}

CODING_SETS = {
    "0": (A, A, A, A, A, A),
    "1": (A, A, B, A, B, B),
    "2": (A, A, B, B, A, B),
    "3": (A, A, B, B, B, A),
    "4": (A, B, A, A, B, B),
    "5": (A, B, B, A, A, B),
    "6": (A, B, B, B, A, A),
    "7": (A, B, A, B, A, B),
    "8": (A, B, A, B, B, A),
    "9": (A, B, B, A, B, A),
}


def calc_crc(number: list[str]) -> str:
    S = 0

    for index, num in enumerate(number):
        if index % 2 == 1:
            S += int(num) * 3
        else:
            S += int(num)

    c = 10 - (S % 10)
    return str(c)


def split_into_digits(text_code: str) -> list[str]:
    if len(text_code) != 12:
        raise ValueError

    return [letter for letter in text_code]


def draw_ean_barcode(digits: list[str], img: Any) -> None:
    coding_set = CODING_SETS[digits[0]]
    offset = 50

    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        BLACK,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX
    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        WHITE,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX
    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        BLACK,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX

    for index, dgt in enumerate(digits[1:7]):
        for module in coding_set[index][dgt]:
            color = WHITE
            if module:
                color = BLACK

            cv.line(
                img,
                Point(offset, 10).to_tuple(),
                Point(offset, IMG_HEIGHT_PX - 20).to_tuple(),
                color,
                MODULE_WIDTH_PX,
            )
            offset += MODULE_WIDTH_PX

    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        WHITE,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX
    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        BLACK,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX
    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        WHITE,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX
    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        BLACK,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX
    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        WHITE,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX

    digits.append(calc_crc(digits))

    for dgt in digits[7:]:
        for module in C[dgt]:
            color = WHITE
            if module:
                color = BLACK

            cv.line(
                img,
                Point(offset, 10).to_tuple(),
                Point(offset, IMG_HEIGHT_PX - 20).to_tuple(),
                color,
                MODULE_WIDTH_PX,
            )
            offset += MODULE_WIDTH_PX

    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        BLACK,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX
    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        WHITE,
        MODULE_WIDTH_PX,
    )
    offset += MODULE_WIDTH_PX
    cv.line(
        img,
        Point(offset, 10).to_tuple(),
        Point(offset, IMG_HEIGHT_PX - 10).to_tuple(),
        BLACK,
        MODULE_WIDTH_PX,
    )


# Create a white image
img = np.zeros((IMG_HEIGHT_PX, IMG_WIDTH_PX, 3), np.uint8)
img.fill(255)

# Draw a black line with thickness of 5 px
# cv.line(img, Point(x=50, y=10).to_tuple(), Point(x=50, y=246).to_tuple(), BLACK, 5)

with st.container():
    st.subheader("Urządzenia Peryferyjne")
    st.title("Generator kodów EAN-13")

    text_code = st.text_input("Wprowadź kod", max_chars=12)

    try:
        digits = split_into_digits(text_code)

        draw_ean_barcode(digits, img)
        cv.imwrite(EAN13_SAVE_PATH, img)

        col1, col2, col3 = st.columns(3)
        with col2:
            # display image
            st.image("./ean_barcodes_img/ean13.png")

            # display download button
            with open("./ean_barcodes_img/ean13.png", "rb") as file:
                st.download_button(
                    label="Pobierz",
                    data=file,
                    file_name="./ean_barcodes_img/ean13.png",
                    mime="image/png",
                )
    except ValueError:
        pass
