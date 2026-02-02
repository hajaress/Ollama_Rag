from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

OUTPUT_DIR = Path("product_pdfs")
OUTPUT_DIR.mkdir(exist_ok=True)

products = {
    "LG_FrostFree_260L": """
Product Model: LG FrostFree 260L

Safety Instructions:
- Always unplug refrigerator before servicing.
- Do not touch compressor with wet hands.

Issue: Refrigerator not cooling properly
Possible Causes:
- Dirty condenser coils
- Low refrigerant gas
- Faulty thermostat

Troubleshooting Steps:
1. Check if power supply is stable.
2. Clean condenser coils using dry brush.
3. Ensure thermostat is set between 3 and 5.
4. If cooling does not improve, gas refilling may be required.

Issue: Excessive ice formation
Possible Causes:
- Door not closing properly
- Defrost heater malfunction

Troubleshooting Steps:
1. Inspect door gasket for damage.
2. Remove ice manually and restart refrigerator.
3. If problem persists, check defrost heater.

Escalation:
- Call authorized service center if compressor noise is abnormal.
""",

    "Samsung_Digital_Inverter_275L": """
Product Model: Samsung Digital Inverter 275L

Safety Instructions:
- Disconnect power before inspection.
- Avoid using sharp objects to remove ice.

Issue: Water leakage inside refrigerator
Possible Causes:
- Blocked drain pipe
- Ice buildup near evaporator

Troubleshooting Steps:
1. Check drain hole for blockage.
2. Flush drain pipe with warm water.
3. Ensure refrigerator is levelled properly.

Issue: Unusual noise during operation
Possible Causes:
- Loose internal components
- Fan motor obstruction

Troubleshooting Steps:
1. Inspect fan area for debris.
2. Tighten loose screws if accessible.
3. If noise persists, schedule service.

Escalation:
- Service visit required if fan motor is faulty.
"""
}

def create_pdf(filename, text):
    file_path = OUTPUT_DIR / f"{filename}.pdf"
    c = canvas.Canvas(str(file_path), pagesize=A4)
    width, height = A4

    y = height - 40
    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 14
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
    print(f"✅ Created {file_path}")

for product, content in products.items():
    create_pdf(product, content)
print("All product PDFs created successfully.")