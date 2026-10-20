import tkinter as tk
import requests



class Calculator:
    def __init__(self, root):
        self.root= root
        self.display= tk.Entry(root, font=("Arial", 12), justify= "right")
        self.display.pack()

        self.first_number= None   # Initialize first operand as None to indicate no number stored yet
        self.current_op= None     # Initialize current operation as None to indicate no operation selected
        self.result_shown= None    # Initialize flag to track whether a result is currently displayed

    def set_operation(self, op):
        if self.display.get().strip() == "":
            return
        self.first_number = float(self.display.get())
        self.current_op = op
        self.display.delete(0, tk.END)
        self.result_shown = False

    def add_number(self, num):
        if self.result_shown:
            self.display.delete(0, tk.END)
            self.result_shown = False
        self.display.insert(tk.END, str(num))

    def calculate_from_api(self):
        if self.first_number is None:
            return
        if self.display.get().strip() == "":
            return
        num2 = float(self.display.get())
        data= {
            "num1":self.first_number,
            "num2": num2,
            "operation":self.current_op,
        }

        try:
            response= requests.post("http://127.0.0.1:8000/calculate", json=data)
            result= response.json()["result"]

            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.first_number= result
            self.result_shown= True
        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
root = tk.Tk()
calc = Calculator(root)



'''def calculate_from_api(op):
    try:
        n1 = float(entry1.get())
        n2 = float(entry2.get())

        data= {"num1": n1, "num2": n2, "operation": op}
        response= requests.post("http://127.0.0.1:8000/calculate", json= data)
        result= response.json()["result"]
        label_result.config(text=f"Result: {result}")
    except Exception as e:
        label_result.config(text= f"Error= {e}")

root= tk.Tk()
root.title("Calculator")
root.geometry("250x300")
entry1= tk.Entry(root, width=20, font=('Arial', 12))
entry1.pack(pady=5)
entry1.insert(0, "First number")
entry2= tk.Entry(root, width=20, font=('Arial', 12))
entry2.pack(pady=5)
entry2.insert(0, "Second number")'''

tk.Button(root, text="+", width=10, command=lambda: calc.set_operation("add")).pack(pady=2)
tk.Button(root, text="-", width=10, command=lambda: calc.set_operation("subtract")).pack(pady=2)
tk.Button(root, text="x", width=10, command=lambda: calc.set_operation("multiply")).pack(pady=2)
tk.Button(root, text="/", width=10, command=lambda: calc.set_operation("divide")).pack(pady=2)
tk.Button(root, text="=", width=10, command=calc.calculate_from_api).pack(pady=2)
tk.Button(root, text="0", command=lambda: calc.add_number(0)).pack()
tk.Button(root, text="1", command=lambda: calc.add_number(1)).pack()
tk.Button(root, text="2", command=lambda: calc.add_number(2)).pack()
tk.Button(root, text="3", command=lambda: calc.add_number(3)).pack()
tk.Button(root, text="4", command=lambda: calc.add_number(4)).pack()
tk.Button(root, text="5", command=lambda: calc.add_number(5)).pack()
tk.Button(root, text="6", command=lambda: calc.add_number(6)).pack()
tk.Button(root, text="7", command=lambda: calc.add_number(7)).pack()
tk.Button(root, text="8", command=lambda: calc.add_number(8)).pack()
tk.Button(root, text="9", command=lambda: calc.add_number(9)).pack()


root.mainloop()
