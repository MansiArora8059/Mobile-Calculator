
import tkinter as tk
import requests


API_URL = "http://127.0.0.1:8000/calculate"


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("430x650")
        self.root.minsize(350, 550)

        self.first_number = None
        self.current_op = None
        self.result_shown = False
        self.angle_mode = "DEG"


        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack(fill="both", expand=True)


        self.display = tk.Entry(
            self.main_frame,
            font=("Arial", 24),
            justify="right",
            relief="solid",
            bd=1
        )
        self.display.pack(fill="x", pady=(0, 10), ipady=12)


        self.mode_label = tk.Label(
            self.main_frame,
            text="Scientific | DEG",
            anchor="w"
        )
        self.mode_label.pack(fill="x", pady=(0, 5))


        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(fill="both", expand=True)


        button_rows = [
            [
                ("2nd", self.second_function),
                ("π", lambda: self.unary_operation("pi")),
                ("e", lambda: self.unary_operation("e")),
                ("CE", self.clear_entry),
                ("⌫", self.backspace),
            ],
            [
                ("x³", lambda: self.unary_operation("cube")),
                ("1/x", lambda: self.unary_operation("reciprocal")),
                ("|x|", lambda: self.unary_operation("absolute")),
                ("exp", lambda: self.unary_operation("e_power")),
                ("mod", lambda: self.set_operation("modulus")),
            ],
            [
                ("³√x", lambda: self.unary_operation("cbrt")),
                ("(", lambda: self.add_text("(")),
                (")", lambda: self.add_text(")")),
                ("n!", lambda: self.unary_operation("factorial")),
                ("÷", lambda: self.set_operation("divide")),
            ],
            [
                ("√x", lambda: self.unary_operation("sqrt")),
                ("7", lambda: self.add_number("7")),
                ("8", lambda: self.add_number("8")),
                ("9", lambda: self.add_number("9")),
                ("×", lambda: self.set_operation("multiply")),
            ],
            [
                ("x²", lambda: self.unary_operation("square")),
                ("4", lambda: self.add_number("4")),
                ("5", lambda: self.add_number("5")),
                ("6", lambda: self.add_number("6")),
                ("−", lambda: self.set_operation("subtract")),
            ],
            [
                ("10ˣ", lambda: self.unary_operation("ten_power")),
                ("1", lambda: self.add_number("1")),
                ("2", lambda: self.add_number("2")),
                ("3", lambda: self.add_number("3")),
                ("+", lambda: self.set_operation("add")),
            ],
            [
                ("log", lambda: self.unary_operation("log10")),
                ("sin", lambda: self.unary_operation("sin")),
                ("cos", lambda: self.unary_operation("cos")),
                ("tan", lambda: self.unary_operation("tan")),
                ("=", self.calculate),
            ],
            [
                ("ln", lambda: self.unary_operation("ln")),
                ("±", self.change_sign),
                ("0", lambda: self.add_number("0")),
                (".", self.add_decimal),
                ("%", lambda: self.unary_operation("percent")),
            ],
        ]


        for row_buttons in button_rows:
            row_frame = tk.Frame(self.buttons_frame)
            row_frame.pack(fill="both", expand=True, pady=2)

            for label, command in row_buttons:
                button = tk.Button(
                    row_frame,
                    text=label,
                    command=command,
                    font=("Arial", 12),
                    relief="raised"
                )
                button.pack(
                    side="left",
                    fill="both",
                    expand=True,
                    padx=2
                )


        self.mode_button = tk.Button(
            self.main_frame,
            text="Switch DEG / RAD",
            command=self.toggle_angle_mode
        )
        self.mode_button.pack(fill="x", pady=(8, 0))

        self.second_mode = False

    def get_display_number(self):
        text = self.display.get().strip()
        if not text:
            return None
        return float(text)

    def add_number(self, number):
        if self.result_shown:
            self.display.delete(0, tk.END)
            self.result_shown = False

        self.display.insert(tk.END, number)

    def add_text(self, text):
        if self.result_shown:
            self.display.delete(0, tk.END)
            self.result_shown = False
        self.display.insert(tk.END, text)

    def add_decimal(self):
        if self.result_shown:
            self.display.delete(0, tk.END)
            self.result_shown = False

        current = self.display.get()
        if "." not in current:
            self.display.insert(tk.END, ".")

    def set_operation(self, operation):
        try:
            number = self.get_display_number()
            if number is None:
                return

            self.first_number = number
            self.current_op = operation
            self.display.delete(0, tk.END)
            self.result_shown = False

        except ValueError:
            self.show_error("Enter a valid number")

    def call_api(self, number, operation, num2=0):
        data = {
            "num1": number,
            "num2": num2,
            "operation": operation,
            "angle_mode": self.angle_mode
        }

        response = requests.post(
            API_URL,
            json=data,
            timeout=5
        )

        response.raise_for_status()
        return response.json()["result"]

    def show_result(self, result):
        self.display.delete(0, tk.END)
        self.display.insert(0, str(result))
        self.result_shown = True

    def show_error(self, message):
        self.display.delete(0, tk.END)
        self.display.insert(0, message)
        self.result_shown = True

    def calculate(self):
        try:
            if self.first_number is None or self.current_op is None:
                return

            second_number = self.get_display_number()
            if second_number is None:
                return

            result = self.call_api(
                self.first_number,
                self.current_op,
                second_number
            )

            self.show_result(result)
            self.first_number = None
            self.current_op = None

        except (ValueError, requests.RequestException, KeyError) as error:
            self.show_error(f"Error: {error}")

    def unary_operation(self, operation):
        try:

            if operation == "pi":
                number = 0
            elif operation == "e":
                number = 0
            else:
                number = self.get_display_number()
                if number is None:
                    return

            result = self.call_api(number, operation)
            self.show_result(result)

        except (ValueError, requests.RequestException, KeyError) as error:
            self.show_error(f"Error: {error}")

    def clear_entry(self):
        self.display.delete(0, tk.END)
        self.result_shown = False

    def backspace(self):
        if self.result_shown:
            self.clear_entry()
            return

        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, current[:-1])

    def change_sign(self):
        try:
            number = self.get_display_number()
            if number is None:
                return
            self.show_result(-number)
        except ValueError:
            self.show_error("Enter a valid number")

    def toggle_angle_mode(self):
        self.angle_mode = (
            "RAD" if self.angle_mode == "DEG" else "DEG"
        )
        self.mode_label.config(
            text=f"Scientific | {self.angle_mode}"
        )

    def second_function(self):
        self.second_mode = not self.second_mode

        if self.second_mode:
            self.mode_label.config(
                text=f"Scientific | {self.angle_mode} | 2nd ON"
            )
        else:
            self.mode_label.config(
                text=f"Scientific | {self.angle_mode}"
            )


root = tk.Tk()
calc = Calculator(root)
root.mainloop()
