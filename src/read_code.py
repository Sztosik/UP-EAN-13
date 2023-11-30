from .country_codes import country_codes

while True:
    code = input("Skanuj kod: ")

    country_code = str(code[:3])
    print(f"Kod kraju: {country_code}")

    try:
        print(f"Kraj: {country_codes[country_code]}\n")

    except:
        print(f"Kraj: niezidentyfikowany\n")
