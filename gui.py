import tkinter as tk
import requests

def calculate_from_api(op):
    try:
        n1 = float(entry1.get())
        n2 = float(entry2.get())

        data= {"num1": n1, "num2": n2, "operation": op}
        response= requests.post("http://127.0.0.1:8000/calculate", json= data)
        result= response.json()["result"]
        label_result.config(text=f"Result: {result}")
    except Exception as e:
        label_result.config(f"Error= {e}")

root= tk.Tk()
root.title("Calculator")
root.geometry("250x300")
entry1= tk.Entry(root, width=20, font=('Arial', 12))
entry1.pack(pady=5)
entry1.insert(0, "First number")
entry2= tk.Entry(root, width=20, font=('Arial', 12))
entry2.pack(pady=5)
entry2.insert(0, "Second number")

tk.Button(root, text= "+",width=10, command=lambda: calculate_from_api("add") ).pack(pady=2)
tk.Button(root, text= "-",width=10, command= lambda: calculate_from_api("subtract")).pack(pady=2)
tk.Button(root, text= "x",width=10, command= lambda:calculate_from_api("multiply")).pack(pady=2)
tk.Button(root, text="/",width=10, command= lambda: calculate_from_api("divide")).pack(pady=2)

label_result = tk.Label(root, text="Result",font=('Arial', 14, 'bold'))
label_result.pack(pady= 20)

root.mainloop()
