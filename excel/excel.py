# Standard library
from pathlib import Path

# Third party modules
import openpyxl
import win32com.client as win32


class ExcelHandler(object):
    """Excel handler

    If file in .xls format, creates a .xlsx version first.

    Attributes:
        attr1 (type): Description.
    """

    def __init__(self, path):
        self.path = Path(path)

        if self.path.suffix == '.xls':
            # First check if .xlsx version already exsists
            # If not, convert the .xls file
            path_xlsx = self.path.with_suffix('.xlsx')

            if not path_xlsx.exists():
                try:
                    excel = win32.gencache.EnsureDispatch('Excel.Application')
                    wb = excel.Workbooks.Open(self.path.as_posix())
                    # FileFormat = 51 for the .xlsx extension
                    # Convert `Path` object to `str`, SaveAs does not like `Path` objects
                    wb.SaveAs(str(path_xlsx), FileFormat=51)
                    wb.Close()
                    excel.Application.Quit()
                except:
                    print('Conversion to .xlsx failed.')

            self.path = path_xlsx

        if not self.path.exists():
            raise FileNotFoundError(f'File "{self.path}" does not exist.')

        self.wb = openpyxl.load_workbook(self.path)
