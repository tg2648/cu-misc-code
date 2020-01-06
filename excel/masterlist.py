# Standard library
from pathlib import Path

# Third party modules
import openpyxl
from openpyxl.utils import column_index_from_string

# Local imports
from excel import ExcelHandler


class FacultyMasterlistHandler(ExcelHandler):
    """Faculty masterlist excel file handler

    Attributes:
        attr1 (type): Description.
    """
    COLUMNS_TO_DELETE = ('F', 'L', 'P')
    SALARY_COLUMN = 'E'

    def __init__(self, path):
        super().__init__(path)
        self.keep_salary = True

    def _clean_cols(self, sheet):
        for col in self.COLUMNS_TO_DELETE:
            sheet.delete_cols(column_index_from_string(col))

        if self.keep_salary:
            sheet.delete_cols(column_index_from_string(self.SALARY_COLUMN))

    def _copy_sheet(self, sheet, target_sheet):
        for i in range(1, sheet.max_row):
            for j in range(1, sheet.max_column):
                target_sheet.cell(row=i, column=j).value = sheet.cell(row=i, column=j).value

    def clean(self):
        new_wb = openpyxl.Workbook()
        new_wb.active.title = 'Faculty List'
        self._clean_cols(sheet=self.wb['ANTH'])
        self._copy_sheet(sheet=self.wb['ANTH'], target_sheet=new_wb.active)
        new_wb.save(self.path.parent / 'list.xlsx')


if __name__ == "__main__":

    wb_path = Path(r'D:\My Drive\Code\CU Python\cu-misc-code\excel\test_masterlist.xls')
    masterlist = FacultyMasterlistHandler(wb_path)
    masterlist.clean()
    # print(masterlist)
    # print(type(masterlist.wb))


"""
- Clean up sheet name
- Copy data
- Clean up data
- Clean up tenure status
- Clean up rank
- Shifts columns around to align data
- Insert division name
"""
