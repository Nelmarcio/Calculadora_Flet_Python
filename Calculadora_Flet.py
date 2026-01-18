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
    page.window.resizable = True
    page.window.width = 320
    page.window.height = 620
    page.window.visible = True
    page.update()
    page.title = "Calculadora Flet"
    page.padding = 1
    page.bgcolor = "#000000"

    # Estado da calculadora
    display_value = ["0"]
    previous_value = ["0"]
    operation = [None]
    should_reset_display = [False]
    second_mode = [False]  # Estado do modo 2nd
    history = []  # Histórico de operações
    
    # Listas para rastrear botões que mudam com 2nd
    button_refs = {"trig": [], "log": [], "extra": [], "second": None}
    
    # ListView de histórico com rolagem
    history_list = ft.ListView(
        controls=[],
        spacing=1,
        height=80,
        expand=False,
        auto_scroll=True,
    )
    
    history_container = ft.Container(
        content=history_list,
        height=50,
        bgcolor="#1a1a1a",
        border_radius=8,
        padding=8,
    )
    
    # Display principal
    display = ft.TextField(
        value="0",
        read_only=True,
        text_align=ft.TextAlign.END,
        text_size=30,
        height=80,
        expand=True,
        bgcolor="#00000F",
        color="#FFFFFF",
        border_color="#000000",
        border_width=3,
        border_radius=15,
        max_length=15,
    )
    
    def update_display(value):
        # Limitar texto do display a 15 caracteres
        if len(value) > 15:
            value = value[:15]
        display_value[0] = value
        
        # Formatar com separador de milhares
        formatted_value = format_display_with_thousands(value)
        display.value = formatted_value
        page.update()
    
    def add_to_history(operation_str):
        """Adiciona operação ao histórico com rolagem"""
        history.append(operation_str)
        # Limitar a 20 operações no histórico
        if len(history) > 20:
            history.pop(0)
        
        # Limpar e reconstruir a lista de histórico
        history_list.controls.clear()
        for item in history:
            history_list.controls.append(
                ft.Text(
                    value=item,
                    size=11,
                    color="#888888",
                    text_align=ft.TextAlign.END,
                )
            )
        page.update()
    
    def format_display_with_thousands(value):
        """Formata o valor para exibição com separador de milhares"""
        try:
            # Se contém vírgula decimal (separador decimal)
            if "," in value:
                parts = value.split(",")
                integer_part = parts[0]
                decimal_part = "," + parts[1]
            else:
                integer_part = value
                decimal_part = ""
            
            # Adicionar separador de milhares no inteiro
            # Tratar números negativos
            if integer_part.startswith("-"):
                sign = "-"
                integer_part = integer_part[1:]
            else:
                sign = ""
            
            # Adicionar pontos a cada 3 dígitos da direita (separador de milhares)
            integer_part = integer_part[::-1]  # Reverter
            formatted_integer = ""
            for i, digit in enumerate(integer_part):
                if i > 0 and i % 3 == 0:
                    formatted_integer += "."
                formatted_integer += digit
            formatted_integer = formatted_integer[::-1]  # Reverter de volta
            
            return sign + formatted_integer + decimal_part
        except:
            return value
    
    def append_number(num):
        if should_reset_display[0]:
            display_value[0] = str(num)
            should_reset_display[0] = False
        else:
            if display_value[0] == "0" and str(num) != ",":
                display_value[0] = str(num)
            elif str(num) == "," and "," in display_value[0]:
                return
            else:
                # Limitar a 15 caracteres
                if len(display_value[0]) < 15:
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
            
            # Converter para número removendo formatação (pontos de milhares) e convertendo vírgula para ponto
            prev_str = previous_value[0].replace(".", "").replace(",", ".")
            curr_str = display_value[0].replace(".", "").replace(",", ".")
            
            prev = float(prev_str)
            curr = float(curr_str)
            
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
            elif operation[0] == "**":
                result = prev ** curr
            else:
                result = curr
            
            # Formatar resultado
            if result == int(result):
                result_str = str(int(result))
            else:
                # Converter ponto para vírgula
                result_str = str(round(result, 10)).replace(".", ",")
            
            # Registrar no histórico
            operation_display = f"{previous_value[0]} {operation[0]} {display_value[0]} = {result_str}"
            add_to_history(operation_display)
            
            update_display(result_str)
            
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
        history.clear()
        history_list.controls.clear()
        page.update()
        update_display("0")
    
    def toggle_sign():
        try:
            num_str = display_value[0].replace(".", "").replace(",", ".")
            num = float(num_str)
            result_str = str(-num).replace(".", ",")
            update_display(result_str)
        except:
            pass
    
    def percentage():
        try:
            num_str = display_value[0].replace(".", "").replace(",", ".")
            num = float(num_str)
            result_str = str(num / 100).replace(".", ",")
            update_display(result_str)
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
            # Converter ponto para vírgula
            return str(round(result, decimals)).replace(".", ",")
    
    def math_operation(operation_func, decimals=10, check_negative=False, check_zero=False):
        """Executa operação matemática genérica"""
        try:
            # Remover formatação (pontos de milhares) e converter vírgula para ponto
            num_str = display_value[0].replace(".", "").replace(",", ".")
            num = float(num_str)
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
            num_str = display_value[0].replace(".", "").replace(",", ".")
            num = int(float(num_str))
            if num < 0:
                update_display("Erro")
                return
            result = math.factorial(num)
            update_display(str(result))
            should_reset_display[0] = True
        except:
            update_display("Erro")
    
    
    def celsius_to_fahrenheit():
        math_operation(lambda x: (x * 9/5) + 32, decimals=2)
    
    # Funções do modo 2nd (funções avançadas)
    def arcsine():
        try:
            num_str = display_value[0].replace(".", "").replace(",", ".")
            num = float(num_str)
            if num < -1 or num > 1:
                update_display("Erro")
                return
            result = math.degrees(math.asin(num))
            update_display(format_result(result, 10))
            should_reset_display[0] = True
        except:
            update_display("Erro")
    
    def arccosine():
        try:
            num_str = display_value[0].replace(".", "").replace(",", ".")
            num = float(num_str)
            if num < -1 or num > 1:
                update_display("Erro")
                return
            result = math.degrees(math.acos(num))
            update_display(format_result(result, 10))
            should_reset_display[0] = True
        except:
            update_display("Erro")
    
    def arctangent():
        math_operation(lambda x: math.degrees(math.atan(x)))
    
    def sinh_func():
        math_operation(math.sinh)
    
    def cosh_func():
        math_operation(math.cosh)
    
    def tanh_func():
        math_operation(math.tanh)
    
    def power_three():
        math_operation(lambda x: x ** 3)
    
    def cube_root():
        math_operation(lambda x: x ** (1/3) if x >= 0 else -(abs(x) ** (1/3)))
    
    def power_y():
        """Prepara para operação x^y"""
        set_operation("**")
    
    def power_2_10():
        """Calcula 2^x"""
        math_operation(lambda x: 2 ** x)
    
    def degrees_to_radians():
        """Converte graus para radianos"""
        math_operation(math.radians)
    
    def absolute_value():
        """Valor absoluto"""
        math_operation(abs)
    
    def toggle_second_mode():
        """Alterna entre modo normal e modo 2nd"""
        second_mode[0] = not second_mode[0]
        button_refs["second"].bgcolor = COLOR_OPERATION if second_mode[0] else COLOR_CLEAR
        button_refs["second"].update()
        
        # Atualizar rótulos e funções dos botões
        if second_mode[0]:
            # Row trigonométrica
            button_refs["trig"][0].content.value = "sin⁻¹"
            button_refs["trig"][1].content.value = "cos⁻¹"
            button_refs["trig"][2].content.value = "tan⁻¹"
            button_refs["trig"][3].content.value = "sinh"
            
            button_refs["trig"][0].on_click = lambda e: arcsine()
            button_refs["trig"][1].on_click = lambda e: arccosine()
            button_refs["trig"][2].on_click = lambda e: arctangent()
            button_refs["trig"][3].on_click = lambda e: sinh_func()
            
            # Row logarítmica
            button_refs["log"][0].content.value = "2^x"
            button_refs["log"][1].content.value = "cosh"
            button_refs["log"][2].content.value = "tanh"
            button_refs["log"][3].content.value = "x³"
            
            button_refs["log"][0].on_click = lambda e: power_2_10()
            button_refs["log"][1].on_click = lambda e: cosh_func()
            button_refs["log"][2].on_click = lambda e: tanh_func()
            button_refs["log"][3].on_click = lambda e: power_three()
            
            # Row extras
            button_refs["extra"][0].content.value = "³√x"
            button_refs["extra"][1].content.value = "°→ʳ"
            
            button_refs["extra"][0].on_click = lambda e: cube_root()
            button_refs["extra"][1].on_click = lambda e: degrees_to_radians()
        else:
            # Row trigonométrica
            button_refs["trig"][0].content.value = "sin"
            button_refs["trig"][1].content.value = "cos"
            button_refs["trig"][2].content.value = "tan"
            button_refs["trig"][3].content.value = "π"
            
            button_refs["trig"][0].on_click = lambda e: sine()
            button_refs["trig"][1].on_click = lambda e: cosine()
            button_refs["trig"][2].on_click = lambda e: tangent()
            button_refs["trig"][3].on_click = lambda e: pi_func()
            
            # Row logarítmica
            button_refs["log"][0].content.value = "log"
            button_refs["log"][1].content.value = "ln"
            button_refs["log"][2].content.value = "e^x"
            button_refs["log"][3].content.value = "10^x"
            
            button_refs["log"][0].on_click = lambda e: log10()
            button_refs["log"][1].on_click = lambda e: ln()
            button_refs["log"][2].on_click = lambda e: exponential()
            button_refs["log"][3].on_click = lambda e: power10()
            
            # Row extras
            button_refs["extra"][0].content.value = "n!"
            button_refs["extra"][1].content.value = "°C→°F"
            
            button_refs["extra"][0].on_click = lambda e: factorial_func()
            button_refs["extra"][1].on_click = lambda e: celsius_to_fahrenheit()
        
        page.update()
    
    def btn(text, on_click_func=None, bgcolor="#333333", text_color="#FFFFFF", size=16, expand=1):
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
            height=40,
            width= 45,
            expand=expand
        )
        return button
    
    # Cores do iPhone
    COLOR_NUMBER = "#333333"
    COLOR_OPERATION = "#FF9500"
    COLOR_EQUALS = "#34C759"
    COLOR_CLEAR = "#A5A5A5"
    
    # Criar botões que mudam com 2nd
    # Botão 2nd
    second_btn = ft.Container(
        content=ft.Text("2nd", size=14, color="#000000", weight="bold", text_align=ft.TextAlign.CENTER),
        on_click=lambda e: toggle_second_mode(),
        bgcolor=COLOR_CLEAR,
        border_radius=10,
        padding=10,
        height=40,
        width=45,
        expand=1,
    )
    button_refs["second"] = second_btn
    
    # Row trigonométrica
    trig_btns = []
    for i, (text, func) in enumerate([("sin", sine), ("cos", cosine), ("tan", tangent), ("π", pi_func)]):
        btn_container = ft.Container(
            content=ft.Text(text, size=16 if text != "π" else 18, color="#305815", weight="bold", text_align=ft.TextAlign.CENTER),
            on_click=lambda e, f=func: f(),
            bgcolor=COLOR_CLEAR,
            border_radius=10,
            padding=10,
            height=40,
            width=45,
            expand=1,
        )
        trig_btns.append(btn_container)
        button_refs["trig"].append(btn_container)
    
    # Row logarítmica
    log_btns = []
    for text, func in [("log", log10), ("ln", ln), ("e^x", exponential), ("10^x", power10)]:
        btn_container = ft.Container(
            content=ft.Text(text, size=16 if text != "10^x" else 14, color="#305815", weight="bold", text_align=ft.TextAlign.CENTER),
            on_click=lambda e, f=func: f(),
            bgcolor=COLOR_CLEAR,
            border_radius=10,
            padding=10,
            height=40,
            width=45,
            expand=1,
        )
        log_btns.append(btn_container)
        button_refs["log"].append(btn_container)
    
    # Row extras
    extra_btns = []
    for text, func in [("n!", factorial_func), ("°C→°F", celsius_to_fahrenheit)]:
        btn_container = ft.Container(
            content=ft.Text(text, size=18 if text == "n!" else 12, color="#305815", weight="bold", text_align=ft.TextAlign.CENTER),
            on_click=lambda e, f=func: f(),
            bgcolor=COLOR_CLEAR,
            border_radius=10,
            padding=10,
            height=40,
            width=45,
            expand=1,
        )
        extra_btns.append(btn_container)
        button_refs["extra"].append(btn_container)
    
    page.add(
        history_container,
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
                                content=ft.Text("0", size=16, color="#FFFFFF", weight="bold", text_align=ft.TextAlign.CENTER),
                                on_click=lambda e: append_number(0),
                                bgcolor=COLOR_NUMBER,
                                border_radius=10,
                                padding=10,
                                height=40,
                                width=150,
                                expand=2
                            ),
                            btn(",", lambda: append_number(","), COLOR_NUMBER, expand=1),
                            btn("=", calculate, COLOR_EQUALS, "#000000", 20, expand=1),
                        ]
                    ),
                    # Row 6: Funções adicionais
                    ft.Row(
                        spacing=8,
                        controls=[
                            btn("√", square_root, COLOR_CLEAR, "#000000", 18, expand=1),
                            btn("x²", power_two, COLOR_CLEAR, "#000000", 18, expand=1),
                            btn("1/x", reciprocal, COLOR_CLEAR, "#000000", 16, expand=1),
                            btn("⌫", backspace, "#FF3B30", "#FFFFFF", 18, expand=1),
                        ]
                    ),
                    # Row 7: 2nd e funções trigonométricas
                    ft.Row(
                        spacing=8,
                        controls=[second_btn] + trig_btns
                    ),
                    # Row 8: Funções logarítmicas
                    ft.Row(
                        spacing=8,
                        controls=log_btns
                    ),
                    # Row 9: Fatorial, Conversões e Extras
                    ft.Row(
                        spacing=8,
                        controls=extra_btns + [
                            btn("|x|", absolute_value, COLOR_CLEAR, "#000000", 16, expand=1),
                            btn("x^y", power_y, COLOR_CLEAR, "#000000", 14, expand=1),
                        ]
                    ),
                ],
            ),
            padding=8,
        ),
    )

if __name__ == "__main__":
    ft.app(target=main)
