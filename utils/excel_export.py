from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill,
    Font,
    Border,
    Side,
    Alignment
)


def create_styled_excel(df, sheet_name):

    wb = Workbook()

    ws = wb.active
    ws.title = sheet_name

    # ========================
    # Colors
    # ========================

    header_fill = PatternFill(
        fill_type="solid",
        start_color="2F5F8A",
        end_color="2F5F8A"
    )

    first_column_fill = PatternFill(
        fill_type="solid",
        start_color="2F5F8A",
        end_color="2F5F8A"
    )

    white_fill = PatternFill(
        fill_type="solid",
        start_color="4682B4",
        end_color="4682B4"
    )

    gray_fill = PatternFill(
        fill_type="solid",
        start_color="8FB3D6",
        end_color="8FB3D6"
    )

    # ========================
    # Fonts
    # ========================

    header_font = Font(
        color="000000",
        bold=True
    )

    first_column_font = Font(
        color="000000",
        bold=False
    )

    normal_font = Font(
        color="000000"
    )

    # ========================
    # Border
    # ========================

    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    # ========================
    # Header Row
    # ========================

    for col_num, column_name in enumerate(
        df.columns,
        start=1
    ):

        cell = ws.cell(
            row=1,
            column=col_num,
            value=column_name
        )

        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin_border

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # ========================
    # Data Rows
    # ========================

    for row_num, row in enumerate(
        df.values,
        start=2
    ):

        # Alternate colors
        row_fill = (
            white_fill
            if row_num % 2 == 0
            else gray_fill
        )

        for col_num, value in enumerate(
            row,
            start=1
        ):

            cell = ws.cell(
                row=row_num,
                column=col_num,
                value=str(value)
            )

            cell.border = thin_border

            # First column gets header color
            if col_num == 1:

                cell.fill = first_column_fill
                cell.font = first_column_font

            else:

                cell.fill = row_fill
                cell.font = normal_font

    # ========================
    # Auto Width
    # ========================

    for column_cells in ws.columns:

        max_length = 0

        column_letter = (
            column_cells[0].column_letter
        )

        for cell in column_cells:

            try:
                max_length = max(
                    max_length,
                    len(str(cell.value))
                )
            except:
                pass

        ws.column_dimensions[
            column_letter
        ].width = max_length + 5

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return output.getvalue()