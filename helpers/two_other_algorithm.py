import random
import math
import numpy as np


def logic_based(self, grid):
    # Kiểm tra tính hợp lệ khi điền số vào ô
    def is_valid(grid, row, col, num):
        # Kiểm tra số trong cùng hàng
        if num in grid[row]:
            return False
        # Kiểm tra số trong cùng cột
        for i in range(9):
            if grid[i][col] == num:
                return False
        # Kiểm tra số trong cùng khu vực 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False
        return True
    
    # Phương pháp Naked Single: Điền số duy nhất có thể vào ô
    def naked_single(grid):
        changes = False
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    possible_values = set(range(1, 10))
                    # Loại trừ các số đã có trong cùng hàng, cột và khu vực 3x3
                    for i in range(9):
                        possible_values.discard(grid[row][i])  # Loại trừ trong cùng hàng
                        possible_values.discard(grid[i][col])  # Loại trừ trong cùng cột
                    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                    for i in range(start_row, start_row + 3):
                        for j in range(start_col, start_col + 3):
                            possible_values.discard(grid[i][j])  # Loại trừ trong cùng khu vực 3x3
                    if len(possible_values) == 1:
                        grid[row][col] = possible_values.pop()
                        
                        self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].create_text(5, 5, text=str(grid[row][col]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                        self.root.update()  # Cập nhật giao diện
                        self.root.after(self.step_delay) 

                        changes = True
        return changes
    
    # Phương pháp Hidden Single: Tìm số duy nhất có thể trong một ô ẩn
    def hidden_single(grid):
        changes = False
        for num in range(1, 10):
            # Kiểm tra hàng
            for row in range(9):
                possible_cols = [col for col in range(9) if grid[row][col] == 0 and is_valid(grid, row, col, num)]
                if len(possible_cols) == 1:
                    grid[row][possible_cols[0]] = num
                    self.robot1_entries[int_to_alpha(row)+int_to_alpha(possible_cols[0])].create_text(5, 5, text=str(grid[row][possible_cols[0]]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                    self.root.update()  # Cập nhật giao diện
                    self.root.after(self.step_delay) 

                    changes = True
            # Kiểm tra cột
            for col in range(9):
                possible_rows = [row for row in range(9) if grid[row][col] == 0 and is_valid(grid, row, col, num)]
                if len(possible_rows) == 1:
                    grid[possible_rows[0]][col] = num
                    self.robot1_entries[int_to_alpha(possible_rows[0])+int_to_alpha(col)].create_text(5, 5, text=str(grid[possible_rows[0]][col]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                    self.root.update()  # Cập nhật giao diện
                    self.root.after(self.step_delay) 

                    changes = True
            # Kiểm tra khu vực 3x3
            for start_row in range(0, 9, 3):
                for start_col in range(0, 9, 3):
                    possible_cells = []
                    for row in range(start_row, start_row + 3):
                        for col in range(start_col, start_col + 3):
                            if grid[row][col] == 0 and is_valid(grid, row, col, num):
                                possible_cells.append((row, col))
                    if len(possible_cells) == 1:
                        grid[possible_cells[0][0]][possible_cells[0][1]] = num
                        
                        self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].create_text(5, 5, text=str(grid[row][col]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                        self.root.update()  # Cập nhật giao diện
                        self.root.after(self.step_delay) 

                        changes = True
        return changes
    
    # Phương pháp Naked Pairs: Loại trừ các số có thể điền vào ô nếu đã xác định được cặp số trong khu vực
    def naked_pairs(grid):
        changes = False
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                # Lọc các ô còn trống trong khu vực
                empty_cells = [(row, col) for row in range(start_row, start_row + 3)
                               for col in range(start_col, start_col + 3) if grid[row][col] == 0]
                # Tìm các cặp số có thể điền vào
                candidates = {}
                for row, col in empty_cells:
                    possible_values = set(range(1, 10))
                    for i in range(9):
                        possible_values.discard(grid[row][i])  # Loại trừ trong cùng hàng
                        possible_values.discard(grid[i][col])  # Loại trừ trong cùng cột
                    start_r, start_c = 3 * (row // 3), 3 * (col // 3)
                    for i in range(start_r, start_r + 3):
                        for j in range(start_c, start_c + 3):
                            possible_values.discard(grid[i][j])  # Loại trừ trong cùng khu vực 3x3
                    if len(possible_values) == 2:
                        candidates[(row, col)] = frozenset(possible_values)  # Sử dụng frozenset thay vì tuple
    
                # Kiểm tra các cặp và loại trừ
                pairs = {}
                for (row, col), vals in candidates.items():
                    for (r, c), v in candidates.items():
                        if (row, col) != (r, c) and vals == v:
                            if vals not in pairs:
                                pairs[vals] = [(row, col), (r, c)]
                
                for pair in pairs.values():
                    vals = pair[0]
                    for (row, col) in empty_cells:
                        if (row, col) not in pair:
                            # Tránh KeyError: Kiểm tra nếu khóa có tồn tại trong candidates
                            if (row, col) in candidates:
                                # Chắc chắn rằng candidates[(row, col)] là frozenset
                                if isinstance(candidates[(row, col)], frozenset) and vals.issubset(candidates[(row, col)]):
                                    candidates[(row, col)] -= vals
                                    changes = True
        return changes
    
        # Phương pháp Backtracking (kỹ thuật đệ quy)
    def backtracking(grid):
        
        if self.stop_flag:
            return False
        # Tìm ô trống
        empty_cell = find_empty_cell(grid)
        if not empty_cell:
            return True  # Đã hoàn thành bảng Sudoku
        row, col = empty_cell
    
        for num in range(1, 10):
            if is_valid(grid, row, col, num):
                grid[row][col] = num
                
                self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].create_text(5, 5, text=str(grid[row][col]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                self.root.update()  # Cập nhật giao diện                
               
                if (self.stop_flag == False):
                    self.root.after(self.step_delay)  

                if backtracking(grid):
                    return True
                
                self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].delete("all")
                grid[row][col] = 0  # Quay lại nếu không tìm được lời giải
    
        return False  # Không tìm thấy lời giải
    
    def find_empty_cell(grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return (row, col)
        return None
    
    # Hàm giải Sudoku với tất cả các kỹ thuật
    def solve_sudoku(grid):
        while True:
            changes = False
            # Áp dụng các kỹ thuật logic
            changes |= naked_single(grid)
            changes |= hidden_single(grid)
            #changes |= naked_pairs(grid)
            
            if not changes:  # Nếu không có thay đổi nào, dừng lại
                break
        # Sử dụng Backtracking nếu cần thiết
       # if find_empty_cell(grid):
       #     backtracking(grid)
        return grid
    
    # Hàm in bảng Sudoku
    def print_grid(grid):
        for row in grid:
            print(" ".join(str(cell) for cell in row))
    # Giải Sudoku và in kết quả
    
    print_grid(grid)
    sudoku_grid = grid
    solved_grid = solve_sudoku(sudoku_grid)
    print_grid(solved_grid)
    return solved_grid
        
def hybrid_sudoku_solver(self, grid):
    # Kiểm tra tính hợp lệ khi điền số vào ô
    def is_valid(grid, row, col, num):
        # Kiểm tra số trong cùng hàng
        if num in grid[row]:
            return False
        # Kiểm tra số trong cùng cột
        for i in range(9):
            if grid[i][col] == num:
                return False
        # Kiểm tra số trong cùng khu vực 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False
        return True
    
    # Phương pháp Naked Single: Điền số duy nhất có thể vào ô
    def naked_single(grid):
        changes = False
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    possible_values = set(range(1, 10))
                    # Loại trừ các số đã có trong cùng hàng, cột và khu vực 3x3
                    for i in range(9):
                        possible_values.discard(grid[row][i])  # Loại trừ trong cùng hàng
                        possible_values.discard(grid[i][col])  # Loại trừ trong cùng cột
                    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                    for i in range(start_row, start_row + 3):
                        for j in range(start_col, start_col + 3):
                            possible_values.discard(grid[i][j])  # Loại trừ trong cùng khu vực 3x3
                    if len(possible_values) == 1:
                        grid[row][col] = possible_values.pop()
                        
                        self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].create_text(5, 5, text=str(grid[row][col]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                        self.root.update()  # Cập nhật giao diện
                        self.root.after(self.step_delay) 

                        changes = True
        return changes
    
    # Phương pháp Hidden Single: Tìm số duy nhất có thể trong một ô ẩn
    def hidden_single(grid):
        changes = False
        for num in range(1, 10):
            # Kiểm tra hàng
            for row in range(9):
                possible_cols = [col for col in range(9) if grid[row][col] == 0 and is_valid(grid, row, col, num)]
                if len(possible_cols) == 1:
                    grid[row][possible_cols[0]] = num
                    self.robot1_entries[int_to_alpha(row)+int_to_alpha(possible_cols[0])].create_text(5, 5, text=str(grid[row][possible_cols[0]]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                    self.root.update()  # Cập nhật giao diện
                    self.root.after(self.step_delay) 

                    changes = True
            # Kiểm tra cột
            for col in range(9):
                possible_rows = [row for row in range(9) if grid[row][col] == 0 and is_valid(grid, row, col, num)]
                if len(possible_rows) == 1:
                    grid[possible_rows[0]][col] = num
                    self.robot1_entries[int_to_alpha(possible_rows[0])+int_to_alpha(col)].create_text(5, 5, text=str(grid[possible_rows[0]][col]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                    self.root.update()  # Cập nhật giao diện
                    self.root.after(self.step_delay) 

                    changes = True
            # Kiểm tra khu vực 3x3
            for start_row in range(0, 9, 3):
                for start_col in range(0, 9, 3):
                    possible_cells = []
                    for row in range(start_row, start_row + 3):
                        for col in range(start_col, start_col + 3):
                            if grid[row][col] == 0 and is_valid(grid, row, col, num):
                                possible_cells.append((row, col))
                    if len(possible_cells) == 1:
                        grid[possible_cells[0][0]][possible_cells[0][1]] = num
                        
                        self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].create_text(5, 5, text=str(grid[row][col]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                        self.root.update()  # Cập nhật giao diện
                        self.root.after(self.step_delay) 

                        changes = True
        return changes
    
    # Phương pháp Naked Pairs: Loại trừ các số có thể điền vào ô nếu đã xác định được cặp số trong khu vực
    def naked_pairs(grid):
        changes = False
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                # Lọc các ô còn trống trong khu vực
                empty_cells = [(row, col) for row in range(start_row, start_row + 3)
                               for col in range(start_col, start_col + 3) if grid[row][col] == 0]
                # Tìm các cặp số có thể điền vào
                candidates = {}
                for row, col in empty_cells:
                    possible_values = set(range(1, 10))
                    for i in range(9):
                        possible_values.discard(grid[row][i])  # Loại trừ trong cùng hàng
                        possible_values.discard(grid[i][col])  # Loại trừ trong cùng cột
                    start_r, start_c = 3 * (row // 3), 3 * (col // 3)
                    for i in range(start_r, start_r + 3):
                        for j in range(start_c, start_c + 3):
                            possible_values.discard(grid[i][j])  # Loại trừ trong cùng khu vực 3x3
                    if len(possible_values) == 2:
                        candidates[(row, col)] = frozenset(possible_values)  # Sử dụng frozenset thay vì tuple
    
                # Kiểm tra các cặp và loại trừ
                pairs = {}
                for (row, col), vals in candidates.items():
                    for (r, c), v in candidates.items():
                        if (row, col) != (r, c) and vals == v:
                            if vals not in pairs:
                                pairs[vals] = [(row, col), (r, c)]
                
                for pair in pairs.values():
                    vals = pair[0]
                    for (row, col) in empty_cells:
                        if (row, col) not in pair:
                            # Tránh KeyError: Kiểm tra nếu khóa có tồn tại trong candidates
                            if (row, col) in candidates:
                                # Chắc chắn rằng candidates[(row, col)] là frozenset
                                if isinstance(candidates[(row, col)], frozenset) and vals.issubset(candidates[(row, col)]):
                                    candidates[(row, col)] -= vals
                                    changes = True
        return changes
    
        # Phương pháp Backtracking (kỹ thuật đệ quy)
    def backtracking(grid):
        if self.stop_flag:
            return False
        # Tìm ô trống
        empty_cell = find_empty_cell(grid)
        if not empty_cell:
            return True  # Đã hoàn thành bảng Sudoku
        row, col = empty_cell
    
        for num in range(1, 10):
            if is_valid(grid, row, col, num):
                grid[row][col] = num
                
                self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].create_text(5, 5, text=str(grid[row][col]), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                self.root.update()  # Cập nhật giao diện                
               
                if (self.stop_flag == False):
                    self.root.after(self.step_delay)  

                if backtracking(grid):
                    return True
                
                self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].delete("all")
                grid[row][col] = 0  # Quay lại nếu không tìm được lời giải
    
        return False  # Không tìm thấy lời giải
    
    def find_empty_cell(grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return (row, col)
        return None
    
    # Hàm giải Sudoku với tất cả các kỹ thuật
    def solve_sudoku(grid):
        while True:
            changes = False
            # Áp dụng các kỹ thuật logic
            changes |= naked_single(grid)
            changes |= hidden_single(grid)
            #changes |= naked_pairs(grid)
            
            if not changes:  # Nếu không có thay đổi nào, dừng lại
                break
        # Sử dụng Backtracking nếu cần thiết
        if find_empty_cell(grid):
            backtracking(grid)
        return grid
    
    # Hàm in bảng Sudoku
    def print_grid(grid):
        for row in grid:
            print(" ".join(str(cell) for cell in row))
    # Giải Sudoku và in kết quả
    
    print_grid(grid)
    sudoku_grid = grid
    solved_grid = solve_sudoku(sudoku_grid)
    print_grid(solved_grid)
    return solved_grid


def int_to_alpha(x):
    return chr(x + ord('A'));


'''

sudoku_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

print("Stochastic Search Solution:")
solution = simulated_annealing(sudoku_puzzle)
print(np.array(solution))

print("\nHybrid Algorithm Solution:")
solution = hybrid_sudoku_solver(sudoku_puzzle)
print(np.array(solution))

'''