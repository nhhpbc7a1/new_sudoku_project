import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import random
import numpy as np
import copy
from helpers.ui_helpers import *
from helpers.logic_helpers import *
from helpers.state_helpers import *
from helpers.file_helpers import *
from helpers.dancing_links import *
from helpers.dancing_links import solve_sudoku
from helpers.two_other_algorithm import *

class Sudoku:
    def __init__(self, root):
        self.game_size = 3
        self.step_delay = 10
        self.selected_entry = ""
        self.root = root
        self.root.title("Sudoku")
        self.root.geometry("1100x650")
        self.root.configure(bg="#FDE2BC")
        
        
        # Sidebar setup
        self.sidebar = tk.Frame(self.root, bg="#D2691E")
        self.sidebar.pack(side="left", fill="y")

        # Add logo
        image_path = "icons8-sudoku-100.png"
        image = load_sudoku_img(image_path)
        tk_image = ImageTk.PhotoImage(image)
        self.logo_label = tk.Label(
            self.sidebar, image=tk_image, bg="#D2691E", width=250, height=150
        )
        self.logo_label.image = tk_image
        self.logo_label.grid(row=0, column=0, pady=1)

        # Buttons
        self.level_buttons_visible = False
        self.setup_buttons()

        # Board setup
        self.board_frame = tk.Frame(self.root, bg="#FDE2BC")
        self.board_frame.pack(side="right", fill="both", expand=True, pady=(20,0))

        # Game variables
        self.values = {}
        self.entries = {}
        
        self.robot1_values = {}
        self.robot1_entries = {}
        self.robot1_algorithm = "backtracking"
        self.robot1_start_state = [];
        #self.board = [];

        self.start_state = []
        self.goal_state = []
        self.mode = "hard"
        self.cnt_mistake = 0
        self.is_playing = False
        self.is_using_pencil = False
        self.seconds = 0
        self.running = False

        self.welcome_screen(self.board_frame)
        self.stop_flag = False
        self.algorithm_name = "backtracking"
        

    def setup_buttons(self):
        self.buttonSingle = ctk.CTkButton(
            self.sidebar,
            text="Single Player",
            fg_color="#C72424",
            text_color="white",
            font=("Arial", 14, "bold"),
            corner_radius=6,
            width=180,
            height=50,
            command=self.show_level_buttons,
        )
        self.buttonSingle.grid(row=1, column=0, padx=30)

        self.buttonVs = ctk.CTkButton(
            self.sidebar,
            text="Machine vs Player",
            fg_color="#C72424",
            text_color="white",
            font=("Arial", 14, "bold"),
            corner_radius=6,
            width=180,
            height=50,
            command=lambda: self.check_and_confirm("human_vs_robot", ""),
        )
        self.buttonVs.grid(row=5, column=0, pady=(15, 0))

        self.buttonMachine = ctk.CTkButton(
            self.sidebar,
            text="Machine mode",
            fg_color="#C72424",
            text_color="white",
            font=("Arial", 14, "bold"),
            corner_radius=6,
            width=180,
            height=50,
            command=self.show_AI_options_buttons,
        )
        self.buttonMachine.grid(row=6, column=0, pady=(15,0))

        self.buttonExit = ctk.CTkButton(
            self.sidebar,
            text="Exit",
            fg_color="#C72424",
            text_color="white",
            font=("Arial", 14, "bold"),
            corner_radius=6,
            width=180,
            height=50,
            command=self.root.destroy
        )
        self.buttonExit.grid(row=12, column=0, pady=15)
    def welcome_screen(self,board_frame):
        welcome_screen(self,board_frame);

    def clear_memset(self):
        clear_memset(self)

    def create_board(self, frame):
        create_board(self, frame)

    def create_robot_board(self, frame):
        create_robot_board(self, frame)

    def generate_sudoku(self, level="medium"):
        generate_sudoku(self, level)

    def solve_sudoku_backtracking(self, board):
        solve_sudoku_backtracking(self, board)

    def solve_sudoku_constraint_propagation(self, board):
        solve_sudoku_constraint_propagation(self, board)

    def is_valid(self, board, row, col, num):
        return is_valid(self, board, row, col, num)

    def find_empty_cell(self, board):
        return find_empty_cell(self, board)

    def update_timer(self):
        update_timer(self)

    def start_timer(self):
        start_timer(self)

    def reset_timer(self):
        reset_timer(self)

    def increase_mistake(self):
        return increase_mistake(self)
        
    def new_game_action(self, mode):
        new_game_action(self, mode)

    def done_game_action(self, winner, is_solved):
        done_game_action(self, winner, is_solved)
        
    def show_level_buttons(self):
        done_game_action(self)
        
    def show_AI_options_buttons(self):
        show_AI_options_buttons(self)

    def human_single(self, board_frame, mode):
        human_single(self, board_frame, mode)
    
    def human_vs_robot(self, board_frame):
        human_vs_robot(self, board_frame)
        
    def robot_single(self, board_frame, mode):
        robot_single(self, board_frame, mode)


    def fill_game_board(self, mode):
        fill_game_board(self, mode)

    def set_value(self, value):
        set_value(self, value)

    def select_entry(self, key):
        select_entry(self, key)

    def clear_highlight(self):
        clear_highlight(self)

    def enter_start_number(self, number):
        enter_start_number(self, number)

    def enter_large_number(self, number):
        enter_large_number(self, number)

    def enter_small_number(self, number):
        enter_small_number(self, number)

    def erase(self):
        erase(self)

    def fill_resolve_AI(self, board):
        fill_resolve_AI(self, board)

    def show_level_buttons(self):
        show_level_buttons(self)

    def start_game_action(self, mode):
        start_game_action(self, mode)
        
    def check_and_confirm(self, string, mode):
        check_and_confirm(self, string, mode)
        
    def switch_page(self, string, mode):
        switch_page(self, string, mode)
        
    def pencil_action(self):
        pencil_action(self);
                
    def solve_sudoku_dancing_links(self, board):
        print(board);
        board = solve_sudoku(self, board)
        #print(board);
        self.fill_resolve_AI(board)
        
    def logic_based(self, board):
        board = logic_based(self, board)
        self.fill_resolve_AI(board)
        
    def hybrid_sudoku_solver(self, board):
        board = hybrid_sudoku_solver(self, board)
        self.fill_resolve_AI(board)

        
    def enter_robot_entries(self, row, col, num):
        if (self.robot1_start_state[row][col] == 0):
            self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].create_text(5, 5, text=str(num+1), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
            self.root.update()  # Cập nhật giao diện
            self.root.after(self.step_delay) 
            
    def hint_number(self):
        hint_number(self);
    

def int_to_alpha(x):
    return chr(x + ord('A'));

if __name__ == "__main__":
    root = tk.Tk()
    game = Sudoku(root)
    root.mainloop()
