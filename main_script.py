import pandas as pd
from math import ceil
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors

input_csv = "input.csv"  # update your CSV filename here

page_width, page_height = A4

days = ['SASTHI', 'SAPTAMI', 'ASTHAMI', 'NABAMI', 'DASHAMI']
meal_types = [
    'BREAKFAST',
    'LUNCH VEG',
    'LUNCH NON VEG',
    'DINNER VEG',
    'DINNER NON VEG',
    'LUNCH VEG KIDS',
    'LUNCH NON VEG KIDS',
    'DINNER VEG KIDS',
    'DINNER NON VEG KIDS'
]

# Fixed coupon size and spacing
coupon_width = 70 * mm
coupon_height = 30 * mm
spacing_x = 5 * mm
spacing_y = 5 * mm
margin = 15 * mm

usable_width = page_width - 2 * margin
usable_height = page_height - 2 * margin - 20 * mm  # Space for header

max_cols = int((usable_width + spacing_x) // (coupon_width + spacing_x))
max_rows = int((usable_height + spacing_y) // (coupon_height + spacing_y))
coupons_per_page = max_cols * max_rows

def draw_coupon(c, x, y, flat_no, day, meal_type, width=coupon_width, height=coupon_height, logo_path="logo.jpg"):
    if "NON VEG" in meal_type.upper():
        bg_color = colors.red
    else:
        bg_color = colors.green

    c.setFillColor(bg_color)
    c.rect(x, y - height, width, height, fill=1)

    c.setLineWidth(1)
    c.setStrokeColor(colors.black)
    c.rect(x, y - height, width, height, fill=0)

    text_x = x + 5*mm
    text_y = y - 8*mm

    logo_width = 20 * mm
    logo_height = 15 * mm
    logo_x = x + width - logo_width - 5 * mm
    logo_y = y - height + 5 * mm
    try:
        c.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
    except:
        pass

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(text_x, y - 6*mm, "Siddha Galaxia Phase 2 Durga Puja - 2025")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(text_x, text_y - 10, f"Flat No: {flat_no}")
    c.drawString(text_x, text_y - 22, f"Day: {day.capitalize()}")
    c.drawString(text_x, text_y - 34, f"Meal: {meal_type.title()}")

def create_pdf_for_flat(flat_no, coupons):
    pdf_filename = f"{flat_no}_durgapuja_food.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)

    total_coupons = len(coupons)
    total_pages = ceil(total_coupons / coupons_per_page) if total_coupons > 0 else 1

    for page_num in range(total_pages):
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.black)
        header_text = f"Coupons for Flat No: {flat_no} (Page {page_num + 1} of {total_pages})"
        c.drawCentredString(page_width / 2, page_height - margin / 2, header_text)

        start_index = page_num * coupons_per_page
        end_index = min(start_index + coupons_per_page, total_coupons)

        for i in range(start_index, end_index):
            rel_i = i - start_index
            row_num = rel_i // max_cols
            col_num = rel_i % max_cols

            x = margin + col_num * (coupon_width + spacing_x)
            y = page_height - margin - 20*mm - row_num * (coupon_height + spacing_y)

            day, meal = coupons[i]
            draw_coupon(c, x, y, flat_no, day, meal)

        c.showPage()

    c.save()
    print(f"PDF saved: {pdf_filename}")

def main():
    df = pd.read_csv(input_csv)

    for idx, row in df.iterrows():
        flat_no = row['FLAT NO']

        coupons = []
        for day in days:
            for meal in meal_types:
                col_name = f"{day} {meal}"
                if col_name in df.columns:
                    val = row[col_name]
                    if pd.notna(val):
                        try:
                            count = int(val)
                        except:
                            count = 0
                        for _ in range(count):
                            coupons.append((day, meal))

        create_pdf_for_flat(flat_no, coupons)

if __name__ == "__main__":
    main()

