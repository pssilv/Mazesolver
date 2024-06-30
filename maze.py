from cell import Cell
import random
import time
import sys

sys.setrecursionlimit(10000)


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.solve()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for cells in self._cells:
            for cell in cells:
                cell.visited = False

    def solve(self):
        return self._solve_i(0, 0)

    def _solve_i(self, i, j):
        self._undo_stack = []
        self._animate()

        while i != self._num_cols - 1 or j != self._num_rows - 1:
            self._animate()

            if self._cells[i][j].has_right_wall:
                self._cells[i][j].has_right_wall_visited = True

            if self._cells[i][j].has_bottom_wall:
                self._cells[i][j].has_bottom_wall_visited = True

            if self._cells[i][j].has_left_wall:
                self._cells[i][j].has_left_wall_visited = True

            if self._cells[i][j].has_top_wall:
                self._cells[i][j].has_top_wall_visited = True

            if (not self._cells[i][j].has_right_wall_visited or
                not self._cells[i][j].has_bottom_wall_visited or
                not self._cells[i][j].has_left_wall_visited or
                not self._cells[i][j].has_top_wall_visited):

                if not self._cells[i][j].has_right_wall_visited:
                    self._cells[i][j].has_right_wall_visited = True
                    self._cells[i][j].draw_move(self._cells[i + 1][j])
                    i += 1
                    self._cells[i][j].has_left_wall_visited = True
                    print("Right")
                    self._undo_stack.append({"i": 1})

                elif not self._cells[i][j].has_bottom_wall_visited:
                    self._cells[i][j].has_bottom_wall_visited = True
                    self._cells[i][j].draw_move(self._cells[i][j + 1])
                    j += 1
                    self._cells[i][j].has_top_wall_visited = True
                    print("Bottom")
                    self._undo_stack.append({"j": 1})

                elif not self._cells[i][j].has_left_wall_visited:
                    self._cells[i][j].has_left_wall_visited = True
                    self._cells[i][j].draw_move(self._cells[i - 1][j])
                    i -= 1
                    self._cells[i][j].has_right_wall_visited = True
                    print("Left")
                    self._undo_stack.append({"i": -1})

                elif not self._cells[i][j].has_top_wall_visited:
                    self._cells[i][j].has_top_wall_visited = True
                    self._cells[i][j].draw_move(self._cells[i][j - 1])
                    j -= 1
                    self._cells[i][j].has_bottom_wall_visited = True
                    print("Top")
                    self._undo_stack.append({"j": -1})

            else:
                print("Backtrack")
                if (self._cells[i][j].has_right_wall_visited and
                    self._cells[i][j].has_bottom_wall_visited and
                    self._cells[i][j].has_left_wall_visited and
                    self._cells[i][j].has_top_wall_visited):

                    sensor = 0

                    for pop in range(len(self._undo_stack)):
                        dic = self._undo_stack.pop()

                        if len(self._undo_stack) == 0:
                            print("You lost!")
                            return False

                        for key in dic:
                            if key == "i":
                                self._cells[i][j].draw_move(self._cells[i - dic[key] ][j], True)
                                i -= dic[key]
                                sensor = 1
                                break

                            if key == "j":
                                self._cells[i][j].draw_move(self._cells[i][j - dic[key] ], True)
                                j -= dic[key]
                                sensor = 1
                                break

                        if sensor != 0:
                            sensor = 0
                            break

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            print("You win!")
