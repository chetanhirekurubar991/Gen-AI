import pdfplumber


def extract_tables_from_pdf(pdf_path: str) -> list[dict]:
    extracted_tables = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            tables = page.extract_tables()

            for table_index, table in enumerate(tables):

                if not table:
                    continue

                cleaned = clean_table(table)
                header = cleaned[0]
                rows = cleaned[1:]

                markdown = convert_table_to_markdown(header, rows)

                extracted_tables.append({
                    "content": markdown,
                    "metadata": {
                        "source": pdf_path,
                        "page": page_number,
                        "table_index": table_index,
                        "type": "table"
                    }
                })

    return extracted_tables


def convert_table_to_markdown(header: list, rows: list) -> str:
    header = [str(cell) if cell is not None else "" for cell in header]

    markdown = "| " + " | ".join(header) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"

    for row in rows:
        row = [str(cell) if cell is not None else "" for cell in row]
        markdown += "| " + " | ".join(row) + " |\n"

    return markdown


def clean_table(table: list) -> list:
    cleaned_table = []

    for row in table:

        cleaned_row = []

        for cell in row:

            if cell is None:
                cleaned_row.append("")

            else:
                cleaned_cell = str(cell).replace("\n", " ").strip()
                cleaned_row.append(cleaned_cell)

        cleaned_table.append(cleaned_row)

    return cleaned_table

if __name__ == "__main__":

    tables = extract_tables_from_pdf("1table.pdf")

    for table in tables:
        print(f"Page: {table['metadata']['page']}")
        print(f"Type: {table['metadata']['type']}")
        print(table['content'])
        print("---")