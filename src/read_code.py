from .__main__ import calc_crc, split_into_digits
from .country_codes import country_codes

while True:
    code = input("Skanuj kod: ")

    digits = split_into_digits(code[:12])
    read_crc = str(code[12])
    correct_crc = calc_crc(digits)

    if read_crc == correct_crc:
        print("Poprawne crc")
    else:
        print("Niepoprawne crc")

    country_code = str(code[:3])
    print(f"Kod kraju: {country_code}")

    try:
        print(f"Kraj: {country_codes[country_code]}\n")

    except:
        print(f"Kraj: niezidentyfikowany\n")
