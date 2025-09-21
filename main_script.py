import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors

input_csv = "input.csv"  # Update if needed
output_pdf = "coupons.pdf"
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

def draw_coupon(c, x, y, flat_no, day, meal_type, width=70*mm, height=30*mm, logo_path="logo.jpg"):
    # Background color: green for veg, red for non veg
    if "NON VEG" in meal_type.upper():
        bg_color = colors.red
    else:
        bg_color = colors.green
    
    # Draw background rectangle
    c.setFillColor(bg_color)
    c.rect(x, y - height, width, height, fill=1)
    
    # Draw border rectangle
    c.setLineWidth(1)
    c.setStrokeColor(colors.black)
    c.rect(x, y - height, width, height, fill=0)
    
    # Text start positions
    text_x = x + 5*mm
    text_y = y - 8*mm
    
    # Draw logo image at bottom right inside coupon
    logo_width = 20 * mm
    logo_height = 15 * mm
    logo_x = x + width - logo_width - 5 * mm
    logo_y = y - height + 5 * mm
    try:
        c.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
    except:
        # If logo file not found, just skip drawing image
        pass
    
    # Draw logo text at top
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(text_x, y - 6*mm, "Siddha Galaxia Phase 2 Durga Puja - 2025")
    
    # Draw coupon details text
    c.setFont("Helvetica-Bold", 10)
    c.drawString(text_x, text_y - 10, f"Flat No: {flat_no}")
    c.drawString(text_x, text_y - 22, f"Day: {day.capitalize()}")
    c.drawString(text_x, text_y - 34, f"Meal: {meal_type.title()}")

def main():
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
        
        # Title on top of page
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.black)
        c.drawCentredString(page_width / 2, page_height - 30, f"Coupons for Flat No: {flat_no}")
        
        coupon_count = 0
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
                            row_pos = coupon_count // coupons_per_row
                            col_pos = coupon_count % coupons_per_row
                            x = x_margin + col_pos * (coupon_width + x_spacing)
                            y = page_height - y_margin - row_pos * (coupon_height + y_spacing)
                            draw_coupon(c, x, y, flat_no, day, meal)
                            coupon_count += 1
        
        c.showPage()
    
    c.save()
    print(f"PDF saved as {output_pdf}")

if __name__ == "__main__":
    main()

