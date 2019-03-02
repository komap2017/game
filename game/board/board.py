import random


def _make_field(rows, columns):
    result = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(None)
        result.append(row)
    return result


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.field = _make_field(rows, columns)

    def fill_empty(self, cell):
        if len(self.field) < self.rows * self.columns:
            for i in range(self.rows):
                for j in range(self.columns):
                    current = self.field[i][j]
                    if current is None:
                        self.field[i][j] = cell
                        return

    def rotate(self, first, second):
        first_cell = self.field[first[0]][first[1]]
        second_cell = self.field[second[0]][second[1]]
        self.field[first[0]][first[1]] = second_cell
        self.field[second[0]][second[1]] = first_cell

    def __getitem__(self,index):
        return self.field[index]

    def __setitem__(self,index,value):
        self.field[index] = value

    @staticmethod
    def _equal_elements(first, second):
        return first.color == second.color

    def check_exploded(self):
        marked_exploded = []
        for i in range(self.rows):
            current_column = 0
            while current_column < self.columns:
                first_element = self.field[i][current_column]
                next_elements = current_column + 1

                def wrap(elem, column):
                    return {'element' : elem, 'column': column, 'row': i}
                
                same_elements = [wrap(first_element, current_column)]
                while next_elements < self.columns:
                    next_element = self.field[i][next_elements]
                    if self._equal_elements(first_element, next_element):
                        next_element = wrap(next_element, next_elements)
                        same_elements.append(next_element)
                    else:
                        if len(same_elements) > 2:
                            marked_exploded.extend(same_elements)
                            current_column = same_elements[-1]['column'] + 1
                        first_element = next_element
                        same_elements = [wrap(first_element, next_elements)]
                    next_elements += 1
                if len(same_elements) > 2:
                    marked_exploded.extend(same_elements)
                    current_column = same_elements[-1]['column'] + 1
                current_column += 1
        for i in range(self.columns):
            current_row = 0
            while current_row < self.rows:
                first_element = self.field[current_row][i]
                next_elements = current_row + 1

                def wrap(elem, r):
                    return {'element' : elem, 'column': i, 'row': r}
                
                same_elements = [wrap(first_element, current_row)]
                while next_elements < self.rows:
                    next_element = self.field[next_elements][i]
                    if self._equal_elements(first_element, next_element):
                        next_element = wrap(next_element, next_elements)
                        same_elements.append(next_element)
                    else:
                        if len(same_elements) > 2:
                            marked_exploded.extend(same_elements)
                            current_row = same_elements[-1]['row'] + 1
                        first_element = next_element
                        same_elements = [wrap(first_element, next_elements)]
                    next_elements += 1
                if len(same_elements) > 2:
                    marked_exploded.extend(same_elements)
                    current_row = same_elements[-1]['row'] + 1
                current_row += 1  
        return self._explode(marked_exploded)

    def _explode(self, same_elements):
        elements = []
        results = []
        for element in same_elements:
            row = element['row']
            column = element['column']
            element = element['element']
            if (row, column) not in elements:
                results.append(element.explode(self, row, column))
            elements.append((row, column))
        return results

    def fall(self):
        empty = []
        for i in range(self.rows):
            for j in range(self.columns):
                cell = self.field[i][j]
                if cell is None:
                    info = (i, j)
                    empty.append(info)
        for row, column in empty:
            if row > 0:
                for current_row in range(row, 0, -1):
                    self.field[current_row][column] = self.field[current_row - 1][column]
                    self.field[current_row - 1][column] = None

    def generate_new(self, elements):
        for i in range(self.rows):
            for j in range(self.columns):
                cell = self.field[i][j]
                if cell is None:
                    item = random.choice(elements)
                    item = item()
                    self.field[i][j] = item
