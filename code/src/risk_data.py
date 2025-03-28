"""
Risk data dictionaries containing FATF ratings, corruption scores, and Basel AML scores.
"""

# FATF Black and Grey Lists
fatf_black = [
    "North Korea",
    "Iran",
    "Myanmar"
]

fatf_grey = [
    "Algeria",
    "Angola",
    "Bulgaria",
    "Burkina Faso",
    "Cameroon",
    "Côte d'Ivoire",
    "Croatia",
    "Democratic Republic of Congo",
    "Haiti",
    "Kenya",
    "Lao People's Democratic Republic",
    "Lebanon",
    "Mali",
    "Monaco",
    "Mozambique",
    "Namibia",
    "Nepal",
    "Nigeria",
    "South Africa",
    "South Sudan",
    "Syria",
    "Tanzania",
    "Venezuela",
    "Vietnam",
    "Yemen"
]

fatf_grey_2024 = [
    "Algeria",
    "Angola",
    "Bulgaria",
    "Burkina Faso",
    "Cameroon",
    "Côte d'Ivoire",
    "Croatia",
    "Democratic Republic of the Congo",
    "Haiti",
    "Kenya",
    "Laos",
    "Lebanon",
    "Mali",
    "Monaco",
    "Mozambique",
    "Namibia",
    "Nepal",
    "Nigeria",
    "South Africa",
    "South Sudan",
    "Syria",
    "Tanzania",
    "Venezuela",
    "Vietnam",
    "Yemen"
]

fatf_black_2024 = [
    "North Korea",
    "Iran",
    "Myanmar"
]

# Corruption Perceptions Index (CPI) scores (0-100)
corruption_data = {
    "Denmark": 90,
    "Finland": 88,
    "Singapore": 84,
    "New Zealand": 83,
    "Luxembourg": 81,
    "Norway": 81,
    "Switzerland": 81,
    "Sweden": 80,
    "Netherlands": 78,
    "Australia": 77,
    "Iceland": 77,
    "Ireland": 77,
    "Estonia": 76,
    "Uruguay": 76,
    "Canada": 75,
    "Germany": 75,
    "Hong Kong": 74,
    "Bhutan": 72,
    "Seychelles": 72,
    "Japan": 71,
    "United Kingdom": 71,
    "Belgium": 69,
    "Barbados": 68,
    "United Arab Emirates": 68,
    "Austria": 67,
    "France": 67,
    "Taiwan": 67,
    "Bahamas": 65,
    "United States": 65,
    "Israel": 64,
    "Korea, South": 64,
    "Chile": 63,
    "Lithuania": 63,
    "Saint Vincent and the Grenadines": 63,
    "Cabo Verde": 62,
    "Dominica": 60,
    "Slovenia": 60,
    "Latvia": 59,
    "Qatar": 59,
    "Saint Lucia": 59,
    "Saudi Arabia": 59,
    "Costa Rica": 58,
    "Botswana": 57,
    "Portugal": 57,
    "Rwanda": 57,
    "Cyprus": 56,
    "Czechia": 56,
    "Grenada": 56,
    "Spain": 56,
    "Fiji": 55,
    "Oman": 55,
    "Italy": 54,
    "Bahrain": 53,
    "Georgia": 53,
    "Poland": 53,
    "Mauritius": 51,
    "Malaysia": 50,
    "Vanuatu": 50,
    "Greece": 49,
    "Jordan": 49,
    "Namibia": 49,
    "Slovakia": 49,
    "Armenia": 47,
    "Croatia": 47,
    "Kuwait": 46,
    "Malta": 46,
    "Montenegro": 46,
    "Romania": 46,
    "Benin": 45,
    "Côte d'Ivoire": 45,
    "São Tomé and Príncipe": 45,
    "Senegal": 45,
    "Jamaica": 44,
    "Kosovo": 44,
    "Timor-Leste": 44,
    "Bulgaria": 43,
    "China": 43,
    "Moldova": 43,
    "Solomon Islands": 43,
    "Albania": 42,
    "Ghana": 42,
    "Burkina Faso": 41,
    "Cuba": 41,
    "Hungary": 41,
    "South Africa": 41,
    "Tanzania": 41,
    "Trinidad and Tobago": 41,
    "Kazakhstan": 40,
    "North Macedonia": 40,
    "Suriname": 40,
    "Vietnam": 40,
    "Colombia": 39,
    "Guyana": 39,
    "Tunisia": 39,
    "Zambia": 39,
    "Gambia": 38,
    "India": 38,
    "Maldives": 38,
    "Argentina": 37,
    "Ethiopia": 37,
    "Indonesia": 37,
    "Lesotho": 37,
    "Morocco": 37,
    "Dominican Republic": 36,
    "Serbia": 35,
    "Ukraine": 35,
    "Algeria": 34,
    "Brazil": 34,
    "Malawi": 34,
    "Nepal": 34,
    "Niger": 34,
    "Thailand": 34,
    "Turkey": 34,
    "Belarus": 33,
    "Bosnia and Herzegovina": 33,
    "Laos": 33,
    "Mongolia": 33,
    "Panama": 33,
    "Philippines": 33,
    "Sierra Leone": 33,
    "Angola": 32,
    "Ecuador": 32,
    "Kenya": 32,
    "Sri Lanka": 32,
    "Togo": 32,
    "Uzbekistan": 32,
    "Djibouti": 31,
    "Papua New Guinea": 31,
    "Peru": 31,
    "Egypt": 30,
    "El Salvador": 30,
    "Mauritania": 30,
    "Bolivia": 28,
    "Guinea": 28,
    "Eswatini": 27,
    "Gabon": 27,
    "Liberia": 27,
    "Mali": 27,
    "Pakistan": 27,
    "Cameroon": 26,
    "Iraq": 26,
    "Madagascar": 26,
    "Mexico": 26,
    "Nigeria": 26,
    "Uganda": 26,
    "Guatemala": 25,
    "Kyrgyzstan": 25,
    "Mozambique": 25,
    "Central African Republic": 24,
    "Paraguay": 24,
    "Bangladesh": 23,
    "Congo": 23,
    "Iran": 23,
    "Azerbaijan": 22,
    "Honduras": 22,
    "Lebanon": 22,
    "Russia": 22,
    "Cambodia": 21,
    "Chad": 21,
    "Comoros": 21,
    "Guinea-Bissau": 21,
    "Zimbabwe": 21,
    "Democratic Republic of the Congo": 20,
    "Tajikistan": 19,
    "Afghanistan": 17,
    "Burundi": 17,
    "Turkmenistan": 17,
    "Haiti": 16,
    "Myanmar": 16,
    "Korea, North": 15,
    "Sudan": 15,
    "Nicaragua": 14,
    "Equatorial Guinea": 13,
    "Eritrea": 13,
    "Libya": 13,
    "Yemen": 13,
    "Syria": 12,
    "Venezuela": 10,
    "Somalia": 9,
    "South Sudan": 8
}

# Basel AML Index scores
basel_score = {
    "Myanmar": 8.17,
    "Haiti": 7.92,
    "Democratic Republic of the Congo": 7.73,
    "Congo": 7.73,
    "Chad": 7.60,
    "Venezuela": 7.59,
    "Lao PDR": 7.53,
    "Central African Republic": 7.49,
    "Gabon": 7.48,
    "Republic of the Congo": 7.28,
    "Guinea-Bissau": 7.28,
    "China": 7.27,
    "Mozambique": 7.15,
    "Liberia": 7.11,
    "Algeria": 6.92,
    "Vietnam": 6.90,
    "Kenya": 6.87,
    "Nigeria": 6.85,
    "Niger": 6.83,
    "Mali": 6.81,
    "Madagascar": 6.76,
    "Cambodia": 6.75,
    "Angola": 6.71,
    "Turkmenistan": 6.71,
    "Eswatini": 6.69,
    "Comoros": 6.68,
    "Cameroon": 6.67,
    "Sierra Leone": 6.49,
    "Burkina Faso": 6.48,
    "Togo": 6.48,
    "Tajikistan": 6.45,
    "Benin": 6.44,
    "Guinea": 6.44,
    "Cote D'ivoire": 6.42,
    "Nicaragua": 6.40,
    "Solomon Islands": 6.32,
    "Mauritania": 6.28,
    "Kuwait": 6.27,
    "United Arab Emirates": 6.18,
    "Thailand": 6.16,
    "Suriname": 6.09,
    "Tanzania": 6.08,
    "Nepal": 6.01,
    "Lesotho": 5.98,
    "Zimbabwe": 5.98,
    "Kyrgyzstan": 5.95,
    "Rwanda": 5.94,
    "Panama": 5.90,
    "Saudi Arabia": 5.88,
    "Philippines": 5.84,
    "Lebanon": 5.81,
    "Uganda": 5.71,
    "South Africa": 5.70,
    "Belarus": 5.67,
    "Ethiopia": 5.66,
    "Honduras": 5.66,
    "Tonga": 5.65,
    "Saint Kitts and Nevis": 5.64,
    "Türkiye": 5.63,
    "Bangladesh": 5.62,
    "Gambia": 5.56,
    "Pakistan": 5.56,
    "Qatar": 5.55,
    "Senegal": 5.53,
    "Bhutan": 5.51,
    "El Salvador": 5.51,
    "Cuba": 5.50,
    "Malaysia": 5.50,
    "India": 5.49,
    "Cape Verde": 5.45,
    "Guatemala": 5.45,
    "Malawi": 5.45,
    "Bolivia": 5.44,
    "Mexico": 5.44,
    "Azerbaijan": 5.40,
    "Brazil": 5.36,
    "Hong Kong, SAR, China": 5.34,
    "Zambia": 5.34,
    "Indonesia": 5.33,
    "Ghana": 5.28,
    "Sri Lanka": 5.28,
    "Uzbekistan": 5.27,
    "Ukraine": 5.26,
    "Bahamas": 5.21,
    "Malta": 5.18,
    "Bahrain": 5.17,
    "Egypt": 5.08,
    "Ecuador": 5.06,
    "Hungary": 5.06,
    "Vanuatu": 5.05,
    "Paraguay": 5.00,
    "Bulgaria": 4.99,
    "Romania": 4.99,
    "Mongolia": 4.98,
    "Dominican Republic": 4.96,
    "Morocco": 4.94,
    "Colombia": 4.92,
    "Namibia": 4.89,
    "Serbia": 4.82,
    "Cyprus": 4.81,
    "Jordan": 4.81,
    "United States": 4.81,
    "Italy": 4.80,
    "Jamaica": 4.79,
    "Japan": 4.77,
    "Peru": 4.77,
    "Tunisia": 4.77,
    "Seychelles": 4.76,
    "Grenada": 4.72,
    "Fiji": 4.71,
    "Singapore": 4.70,
    "Kazakhstan": 4.65,
    "Moldova": 4.65,
    "Georgia": 4.64,
    "Germany": 4.63,
    "Costa Rica": 4.61,
    "Mauritius": 4.61,
    "Barbados": 4.58,
    "Samoa": 4.56,
    "Croatia": 4.53,
    "Netherlands": 4.52,
    "Belgium": 4.48,
    "Canada": 4.47,
    "Saint Lucia": 4.46,
    "Switzerland": 4.46,
    "Korea, South": 4.42,
    "Slovakia": 4.39,
    "Botswana": 4.36,
    "Albania": 4.35,
    "Armenia": 4.35,
    "Austria": 4.35,
    "Poland": 4.34,
    "Brunei Darussalam": 4.30,
    "Spain": 4.29,
    "North Macedonia": 4.24,
    "Ireland": 4.23,
    "Montenegro": 4.23,
    "Dominica": 4.21,
    "Trinidad and Tobago": 4.19,
    "Liechtenstein": 4.16,
    "United Kingdom": 4.14,
    "Uruguay": 4.11,
    "Antigua and Barbuda": 4.10,
    "Portugal": 4.09,
    "Chile": 4.08,
    "Latvia": 4.08,
    "Saint Vincent and The Grenadines": 4.07,
    "Taiwan (Chinese Taipei)": 4.05,
    "Australia": 4.04,
    "Luxembourg": 3.99,
    "Israel": 3.97,
    "France": 3.86,
    "Czech Republic": 3.85,
    "Norway": 3.76,
    "New Zealand": 3.68,
    "Greece": 3.66,
    "Lithuania": 3.54,
    "Slovenia": 3.54,
    "Denmark": 3.50,
    "Sweden": 3.45,
    "Andorra": 3.29,
    "Estonia": 3.16,
    "Finland": 3.07,
    "Iceland": 3.00,
    "San Marino": 2.96,
}