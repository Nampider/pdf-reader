from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, BooleanObject
import os

# File paths
source_path = r"./pdf-storage/source_filled.pdf"
target_path = r"./pdf-storage/target_template.pdf"
temp_output_path = r"./pdf-storage/_temp_filled.pdf"  # Temporary file

# Step 1: Load source and target PDFs
source_pdf = PdfReader(source_path)
target_pdf = PdfReader(target_path)
writer = PdfWriter()

# Step 2: Get filled form data from source
source_fields = source_pdf.get_fields()

# Step 3: Copy pages from target into writer
for page in target_pdf.pages:
    writer.add_page(page)

# Step 4: Transfer field values to the first page (or loop through all if needed)
for field_name, field_data in source_fields.items():
    value = field_data.get("/V")
    if value:
        writer.update_page_form_field_values(writer.pages[0], {field_name: value})

# Step 5: Ensure form fields appear correctly
if "/AcroForm" in target_pdf.trailer["/Root"]:
    writer._root_object.update({
        NameObject("/AcroForm"): target_pdf.trailer["/Root"]["/AcroForm"]
    })
    writer._root_object["/AcroForm"].update({
        NameObject("/NeedAppearances"): BooleanObject(True)
    })

# Step 6: Save to a temporary file
with open(temp_output_path, "wb") as f:
    writer.write(f)

# Step 7: Replace original target file with updated version
os.replace(temp_output_path, target_path)

print(f"Form fields from '{source_path}' successfully transferred to '{target_path}'.")
