"""
Comparison of CSV values as sets.
"""


class ValueComparator(object):
    """Allows comparing values loaded from CSV as sets.

    Attributes:
        path1 (str): Path to the first CSV.
        path2 (str): Path to the second CSV.

    TODO:
        Output path not hard-coded.
    """

    def __init__(self, path_in_1, path_in_2):

        with open(path_in_1, 'r') as f1:
            self.vals1 = {line.rstrip() for line in f1}

        with open(path_in_2, 'r') as f2:
            self.vals2 = {line.rstrip() for line in f2}

    def _write_output(self, path_out, result):
        """Writes output to CSV.

        Args:
            path_out (str): Path to output file.
            result (set): Result of comparison.
        """

        with open(path_out, 'w') as f_out:
            for i in result:
                f_out.writelines(f"{i}\n")

    def difference(self):
        """Calculates a difference from two sets.

        Writes the difference (elements in set 1 that are not in  set 2) to a file with `_write_output`.
        """

        result = self.vals1 - self.vals2
        self._write_output('set-comparison/difference.csv', result)


if __name__ == "__main__":

    Comparator = ValueComparator('set-comparison/input1.csv', 'set-comparison/input2.csv')
    Comparator.difference()
    print('Done')
