import flet as ft
import random
import time
from datetime import datetime

def main(page: ft.Page):
    page.title = "MATH WORKOUT"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.bgcolor = "#f0f0f0"
    
    # All math problems
    all_problems = [
        {"question": "2 + 4", "answer": 6}, {"question": "2 + 5", "answer": 7},
        {"question": "2 + 6", "answer": 8}, {"question": "2 + 7", "answer": 9},
        {"question": "3 + 3", "answer": 6}, {"question": "3 + 4", "answer": 7},
        {"question": "3 + 5", "answer": 8}, {"question": "3 + 6", "answer": 9},
        {"question": "4 + 4", "answer": 8}, {"question": "4 + 5", "answer": 9},
        {"question": "5 - 2", "answer": 3}, {"question": "8 - 3", "answer": 5},
        {"question": "9 - 3", "answer": 6}, {"question": "1 * 3", "answer": 3},
        {"question": "1 * 5", "answer": 5}, {"question": "1 * 6", "answer": 6},
        {"question": "4 * 1", "answer": 4}, {"question": "5 * 1", "answer": 5},
        {"question": "7 * 1", "answer": 7}, {"question": "8 * 1", "answer": 8},
        {"question": "9 * 1", "answer": 9}, {"question": "10 - 5", "answer": 5},
        {"question": "2 * 3", "answer": 6}, {"question": "3 * 3", "answer": 9},
        {"question": "4 / 2", "answer": 2}, {"question": "6 / 2", "answer": 3},
        {"question": "8 / 2", "answer": 4}, {"question": "10 / 2", "answer": 5},
        {"question": "8 / 4", "answer": 2}, {"question": "9 / 3", "answer": 3},
        {"question": "8 / 1", "answer": 8}, {"question": "9 / 1", "answer": 9},
        {"question": "3 + 5", "answer": 8}, {"question": "7 - 3", "answer": 4},
        {"question": "2 * 4", "answer": 8}, {"question": "18 - 9", "answer": 9},
        {"question": "5 + 3", "answer": 8}, {"question": "12 / 4", "answer": 3},
        {"question": "17 - 9", "answer": 8}
    ]
    
    # Game state
    game_state = {
        "problems": [],
        "current_index": 0,
        "correct_answer": None,
        "timer_start": None,
        "mistakes_count": 0,
        "game_running": False
    }
    
    # UI Components
    timer_text = ft.Text("", size=16, color="#666")
    
    problem_text = ft.Text(
        "Press START to begin",
        size=32,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.NORMAL
    )
    
    problem_screen = ft.Container(
        content=ft.Stack([
            ft.Container(
                content=problem_text,
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=timer_text,
                alignment=ft.alignment.top_right,
                padding=10
            )
        ]),
        width=400,
        height=80,
        bgcolor="white",
        border=ft.border.all(3, "#444"),
        border_radius=10,
        alignment=ft.alignment.center,
    )
    
    result_text = ft.Text("", size=16, text_align=ft.TextAlign.CENTER)
    
    def update_timer():
        if game_state["game_running"] and game_state["timer_start"]:
            elapsed = time.time() - game_state["timer_start"]
            timer_text.value = f"{elapsed:.1f}s"
            page.update()
    
    def show_problem():
        if game_state["current_index"] >= len(game_state["problems"]):
            end_game()
            return
        
        prob = game_state["problems"][game_state["current_index"]]
        problem_text.value = prob["question"]
        game_state["correct_answer"] = prob["answer"]
        problem_screen.bgcolor = "white"
        page.update()
    
    def countdown(callback):
        for count in [3, 2, 1]:
            problem_text.value = str(count)
            problem_screen.bgcolor = "white"
            page.update()
            time.sleep(1)
        
        problem_text.value = ""
        callback()
    
    def end_game():
        game_state["game_running"] = False
        
        time_elapsed = time.time() - game_state["timer_start"]
        penalty = game_state["mistakes_count"] * 5
        total_time = time_elapsed + penalty
        
        problem_text.value = "Game Over"
        result_text.value = (
            f"Time Solving: {time_elapsed:.2f} seconds\n"
            f"Number of Mistakes: {game_state['mistakes_count']}\n"
            f"Total Time: {total_time:.2f} seconds (Time + Mistakes × 5s)"
        )
        
        start_btn.text = "START"
        start_btn.bgcolor = "#2ecc71"
        start_btn.disabled = False
        page.update()
    
    def start_game(e):
        if game_state["game_running"]:
            restart_game(e)
            return
        
        game_state["current_index"] = 0
        game_state["mistakes_count"] = 0
        game_state["correct_answer"] = None
        
        # Shuffle and select 20 problems
        shuffled = all_problems.copy()
        random.shuffle(shuffled)
        game_state["problems"] = shuffled[:20]
        
        result_text.value = ""
        problem_screen.bgcolor = "white"
        problem_text.value = "Get Ready..."
        start_btn.disabled = True
        page.update()
        
        def after_countdown():
            game_state["timer_start"] = time.time()
            game_state["game_running"] = True
            start_btn.text = "RESTART"
            start_btn.bgcolor = "#e74c3c"
            start_btn.disabled = False
            show_problem()
            
            # Start timer updates
            def timer_loop():
                while game_state["game_running"]:
                    update_timer()
                    time.sleep(0.1)
            
            import threading
            threading.Thread(target=timer_loop, daemon=True).start()
        
        countdown(after_countdown)
    
    def restart_game(e):
        game_state["game_running"] = False
        game_state["current_index"] = 0
        game_state["mistakes_count"] = 0
        game_state["correct_answer"] = None
        
        result_text.value = ""
        problem_screen.bgcolor = "white"
        problem_text.value = "Press START to begin"
        timer_text.value = ""
        start_btn.text = "START"
        start_btn.bgcolor = "#2ecc71"
        start_btn.disabled = False
        page.update()
    
    def handle_answer(num):
        if not game_state["game_running"]:
            return
        
        if num == game_state["correct_answer"]:
            game_state["current_index"] += 1
            show_problem()
        else:
            game_state["mistakes_count"] += 1
            problem_screen.bgcolor = "#e74c3c"
            page.update()
            time.sleep(0.3)
            if game_state["game_running"]:
                problem_screen.bgcolor = "white"
                page.update()
    
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == " ":  # Space key
            if game_state["game_running"]:
                restart_game(None)
            else:
                start_game(None)
        elif e.key in "123456789":
            handle_answer(int(e.key))
    
    page.on_keyboard_event = on_keyboard
    
    # Create answer buttons
    button_grid = ft.GridView(
        runs_count=3,
        max_extent=100,
        child_aspect_ratio=1,
        spacing=10,
        run_spacing=10,
    )
    
    for i in range(1, 10):
        btn = ft.ElevatedButton(
            text=str(i),
            width=100,
            height=100,
            style=ft.ButtonStyle(
                color="white",
                bgcolor="#3498db",
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=lambda e, num=i: handle_answer(num)
        )
        button_grid.controls.append(btn)
    
    start_btn = ft.ElevatedButton(
        text="START",
        style=ft.ButtonStyle(
            color="white",
            bgcolor="#2ecc71",
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        width=200,
        height=50,
        on_click=start_game
    )
    
    # Add all components to page
    page.add(
        ft.Text("MATH WORKOUT", size=40, weight=ft.FontWeight.BOLD, color="#222"),
        ft.Container(height=20),
        problem_screen,
        ft.Container(height=20),
        ft.Container(
            content=button_grid,
            width=340,
        ),
        ft.Container(height=20),
        start_btn,
        ft.Container(height=20),
        result_text
    )

ft.app(target=main)