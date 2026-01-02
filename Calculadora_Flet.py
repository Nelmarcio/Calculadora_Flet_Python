import flet as ft
import math
import sys
import logging
from io import StringIO

# Redirecionar stdout/stderr para evitar erros de logging quando rodando como .exe
if sys.stdout is None:
    sys.stdout = StringIO()
if sys.stderr is None:
    sys.stderr = StringIO()

# Desabilitar logging verbose do Flet
logging.getLogger("flet").setLevel(logging.ERROR)

def main(page: ft.Page):
    page.window_resizable = False
    page.title = "Calculadora Flet"
    page.padding = 0
    page.bgcolor = "#000000"
    page.window_min_width = 350
    page.window_min_height = 480
    page.window_max_width = 350
    page.window_max_height = 480

    # Estado da calculadora
    display_value = ["0"]
    previous_value = ["0"]
    operation = [None]
    should_reset_display = [False]
    
    # Display principal
    display = ft.TextField(
        value="0",
        read_only=True,
        text_align=ft.TextAlign.END,
        text_size=48,
        height=150,
        expand=True,
        bgcolor="#00000F",
        color="#FFFFFF",
        border_color="#000000",
        border_width=1,
        border_radius=15,
    
    )
    
    def update_display(value):
        display_value[0] = value
        display.value = value
        page.update()
    
    def append_number(num):
        if should_reset_display[0]:
            display_value[0] = str(num)
            should_reset_display[0] = False
        else:
            if display_value[0] == "0" and str(num) != ".":
                display_value[0] = str(num)
            elif str(num) == "." and "." in display_value[0]:
                return
            else:
                display_value[0] += str(num)
        update_display(display_value[0])
    
    def set_operation(op):
        if operation[0] is not None and not should_reset_display[0]:
            calculate()
        else:
            previous_value[0] = display_value[0]
        operation[0] = op
        should_reset_display[0] = True
    
    def calculate():
        try:
            if operation[0] is None:
                return
            
            prev = float(previous_value[0])
            curr = float(display_value[0])
            
            if operation[0] == "+":
                result = prev + curr
            elif operation[0] == "-":
                result = prev - curr
            elif operation[0] == "*":
                result = prev * curr
            elif operation[0] == "/":
                if curr == 0:
                    update_display("Erro")
                    return
                result = prev / curr
            elif operation[0] == "%":
                result = prev % curr
            else:
                result = curr
            
            # Formatar resultado
            if result == int(result):
                update_display(str(int(result)))
            else:
                update_display(str(round(result, 10)))
            
            operation[0] = None
            should_reset_display[0] = True
            previous_value[0] = display_value[0]
        except:
            update_display("Erro")
    
    def clear():
        display_value[0] = "0"
        previous_value[0] = "0"
        operation[0] = None
        should_reset_display[0] = False
        update_display("0")
    
    def toggle_sign():
        try:
            num = float(display_value[0])
            update_display(str(-num))
        except:
            pass
    
    def percentage():
        try:
            num = float(display_value[0])
            update_display(str(num / 100))
            should_reset_display[0] = True
        except:
            pass
    
    def backspace():
        if len(display_value[0]) > 1:
            display_value[0] = display_value[0][:-1]
        else:
            display_value[0] = "0"
        update_display(display_value[0])
    
    def format_result(result, decimals=10):
        """Formata resultado removendo zeros desnecessários"""
        if result == int(result):
            return str(int(result))
        else:
            return str(round(result, decimals))
    
    def math_operation(operation_func, decimals=10, check_negative=False, check_zero=False):
        """Executa operação matemática genérica"""
        try:
            num = float(display_value[0])
            if check_negative and num < 0:
                update_display("Erro")
                return
            if check_zero and num == 0:
                update_display("Erro")
                return
            result = operation_func(num)
            update_display(format_result(result, decimals))
            should_reset_display[0] = True
        except:
            update_display("Erro")
    
    def square_root():
        math_operation(math.sqrt, check_negative=True)
    
    def power_two():
        math_operation(lambda x: x ** 2)
    
    def reciprocal():
        math_operation(lambda x: 1 / x, check_zero=True)
    
    def sine():
        math_operation(lambda x: math.sin(math.radians(x)))
    
    def cosine():
        math_operation(lambda x: math.cos(math.radians(x)))
    
    def tangent():
        math_operation(lambda x: math.tan(math.radians(x)))
    
    def log10():
        math_operation(math.log10, check_negative=True)
    
    def ln():
        math_operation(math.log, check_negative=True)
    
    def exponential():
        math_operation(math.exp)
    
    def power10():
        math_operation(lambda x: 10 ** x)
    
    def pi_func():
        update_display(str(round(math.pi, 10)))
        should_reset_display[0] = True
    
    def factorial_func():
        try:
            num = int(float(display_value[0]))
            if num < 0:
                update_display("Erro")
                return
            result = math.factorial(num)
            update_display(str(result))
            should_reset_display[0] = True
        except:
            update_display("Erro")
    
    def rad_to_deg():
        math_operation(math.degrees)
    
    def deg_to_rad():
        math_operation(math.radians)
    
    def celsius_to_fahrenheit():
        math_operation(lambda x: (x * 9/5) + 32, decimals=2)
    
    def btn(text, on_click_func=None, bgcolor="#333333", text_color="#FFFFFF", size=20, expand=1):
        """Cria um botão com estilo iPhone"""
        button = ft.Container(
            content=ft.Text(
                text,
                size=size,
                color=text_color,
                weight="bold",
                text_align=ft.TextAlign.CENTER,
            ),
            on_click=lambda e: on_click_func() if on_click_func else None,
            bgcolor=bgcolor,
            border_radius=10,
            padding=10,
            height=50,
            width=80,
            expand=expand
        )
        return button
    
    # Cores do iPhone
    COLOR_NUMBER = "#333333"
    COLOR_OPERATION = "#FF9500"
    COLOR_EQUALS = "#34C759"
    COLOR_CLEAR = "#A5A5A5"
    
    page.add(
        display,
        ft.Container(
            content=ft.Column(
                spacing=8,
                controls=[
                    # Row 1: AC, +/-, %, ÷
                    ft.Row(
                        spacing=8,
                        controls=[
                            btn("AC", clear, COLOR_CLEAR, "#000000", expand=1),
                            btn("+/-", toggle_sign, COLOR_CLEAR, "#000000", expand=1),
                            btn("%", percentage, COLOR_CLEAR, "#000000", expand=1),
                            btn("÷", lambda: set_operation("/"), COLOR_OPERATION, expand=1),
                        ]
                    ),
                    # Row 2: 7, 8, 9, ×
                    ft.Row(
                        spacing=8,
                        controls=[
                            btn("7", lambda: append_number(7), COLOR_NUMBER, expand=1),
                            btn("8", lambda: append_number(8), COLOR_NUMBER, expand=1),
                            btn("9", lambda: append_number(9), COLOR_NUMBER, expand=1),
                            btn("×", lambda: set_operation("*"), COLOR_OPERATION, expand=1),
                        ]
                    ),
                    # Row 3: 4, 5, 6, -
                    ft.Row(
                        spacing=8,
                        controls=[
                            btn("4", lambda: append_number(4), COLOR_NUMBER, expand=1),
                            btn("5", lambda: append_number(5), COLOR_NUMBER, expand=1),
                            btn("6", lambda: append_number(6), COLOR_NUMBER, expand=1),
                            btn("-", lambda: set_operation("-"), COLOR_OPERATION, expand=1),
                        ]
                    ),
                    # Row 4: 1, 2, 3, +
                    ft.Row(
                        spacing=8,
                        controls=[
                            btn("1", lambda: append_number(1), COLOR_NUMBER, expand=1),
                            btn("2", lambda: append_number(2), COLOR_NUMBER, expand=1),
                            btn("3", lambda: append_number(3), COLOR_NUMBER, expand=1),
                            btn("+", lambda: set_operation("+"), COLOR_OPERATION, expand=1),
                        ]
                    ),
                    # Row 5: 0, ., =
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "0",
                                    size=20,
                                    color="#FFFFFF",
                                    weight="bold",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                on_click=lambda e: append_number(0),
                                bgcolor=COLOR_NUMBER,
                                border_radius=10,
                                padding=10,
                                height=50,
                                width=170,
                                expand=2
                            ),
                            btn(".", lambda: append_number("."), COLOR_NUMBER, expand=1),
                            btn("=", calculate, COLOR_EQUALS, "#000000", 24, expand=1),
                        ]
                    ),
                    # Row 6: Funções adicionais
                    ft.Row(
                        spacing=8,
                        controls=[
                            btn("√", square_root, COLOR_CLEAR, "#000000", 18, expand=1),
                            btn("x²", power_two, COLOR_CLEAR, "#000000", 18, expand=1),
                            btn("1/x", reciprocal, COLOR_CLEAR, "#000000", 16, expand=1),
                            btn("⌫", backspace, COLOR_CLEAR, "#000000", 18, expand=1),
                        ]
                    ),
                    # Row 7: Funções trigonométricas
                    ft.Row(
                        spacing=8,
                        controls=[
                            btn("sin", sine, COLOR_CLEAR, "#000000", 16, expand=1),
                            btn("cos", cosine, COLOR_CLEAR, "#000000", 16, expand=1),
                            btn("tan", tangent, COLOR_CLEAR, "#000000", 16, expand=1),
                            btn("π", pi_func, COLOR_CLEAR, "#000000", 18, expand=1),
                        ]
                    ),
                    # Row 8: Funções logarítmicas
                    ft.Row(
                        spacing=8,
                        controls=[
                            btn("log", log10, COLOR_CLEAR, "#000000", 16, expand=1),
                            btn("ln", ln, COLOR_CLEAR, "#000000", 16, expand=1),
                            btn("e^x", exponential, COLOR_CLEAR, "#000000", 16, expand=1),
                            btn("10^x", power10, COLOR_CLEAR, "#000000", 14, expand=1),
                        ]
                    ),
                    # Row 9: Fatorial e Conversões
                    ft.Row(
                        spacing=8,
                        controls=[
                            btn("n!", factorial_func, COLOR_CLEAR, "#000000", 18, expand=1),
                            btn("°→rad", deg_to_rad, COLOR_CLEAR, "#000000", 12, expand=1),
                            btn("rad→°", rad_to_deg, COLOR_CLEAR, "#000000", 12, expand=1),
                            btn("°C→°F", celsius_to_fahrenheit, COLOR_CLEAR, "#000000", 12, expand=1),
                        ]
                    ),

                ],
            ),
            padding=0,
        ),
    )

if __name__ == "__main__":
    ft.app(target=main)
