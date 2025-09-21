import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Config
input_csv = "input.csv"  # change to your CSV filename
output_pdf = "coupons.pdf"
page_width, page_height = A4

days = ['SASTHI', 'SAPTAMI', 'ASTHAMI', 'NABAMI']
meal_types = ['BREAKFAST', 'LUNCH VEG', 'LUNCH NON VEG', 'DINNER VEG', 'DINNER NON VEG']

def draw_coupon(c, x, y, flat_no, day, meal_type, width=70*mm, height=30*mm):
    c.rect(x, y - height, width, height)
    text_x = x + 5*mm
    text_y = y - 10*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(text_x, text_y, f"Flat No: {flat_no}")
    c.drawString(text_x, text_y - 12, f"Day: {day}")
    c.drawString(text_x, text_y - 24, f"Meal: {meal_type}")

def main():
    # Read CSV file
    df = pd.read_csv(input_csv)
    
    c = canvas.Canvas(output_pdf, pagesize=A4)
    
    coupons_per_row = 3
    coupon_width = 70 * mm
    coupon_height = 30 * mm
    x_margin = 15 * mm
    y_margin = 20 * mm
    x_spacing = 10 * mm
    y_spacing = 10 * mm
    
    for idx, row in df.iterrows():
        flat_no = row['FLAT NO']
        
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(page_width / 2, page_height - 30, f"Coupons for Flat No: {flat_no}")
        
        coupon_count = 0
        for day in days:
            for meal in meal_types:
                col_name = f"{day} {meal}"
                if col_name in df.columns:
                    val = row[col_name]
                    if pd.notna(val) and str(val).strip() != "" and str(val).strip() != "0":
                        row_pos = coupon_count // coupons_per_row
                        col_pos = coupon_count % coupons_per_row
                        x = x_margin + col_pos * (coupon_width + x_spacing)
                        y = page_height - y_margin - row_pos * (coupon_height + y_spacing)
                        draw_coupon(c, x, y, flat_no, day.capitalize(), meal)
                        coupon_count += 1
        
        c.showPage()
    
    c.save()
    print(f"PDF saved as {output_pdf}")

if __name__ == "__main__":
    main()

