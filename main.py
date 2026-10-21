from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math
app= FastAPI()

class Calculation(BaseModel):
    num1: float
    num2:float
    operation: str

@app.post("/calculate")
async def calculate(data: Calculation):
    a= data.num1
    b= data.num2
    op= data.operation
    if op=="add":
        result= a+ b
    elif op=="subtract":
        result= a-b
    elif op=="multiply":
        result= a*b
    elif op=="divide":
        if b==0:
            raise HTTPException(status_code=400, detail= "can't be divided by 0")
        result= a/b
    elif op == "sqrt":
        if a < 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot calculate square root of a negative number"
            )
        result = math.sqrt(a)
    elif op == "exponent":
        result = a ** b
    elif op == "cube":
        result = a ** 3
    elif op == "reciprocal":
        if a == 0:
            raise HTTPException(400, "Cannot divide by zero")
        result = 1 / a
    elif op == "absolute":
        result = abs(a)
    elif op == "factorial":
        if a < 0 or not a.is_integer() or a > 170:
            raise HTTPException(400, "Factorial requires an integer from 0 to 170")
        result = math.factorial(int(a))
    elif op == "sin":
        x = math.radians(a) if mode == "DEG" else a
        result = math.sin(x)
    elif op == "cos":
        x = math.radians(a) if mode == "DEG" else a
        result = math.cos(x)
    elif op == "tan":
        x = math.radians(a) if mode == "DEG" else a
        if mode == "DEG" and abs(math.cos(x)) < 1e-12:
            raise HTTPException(400, "Tangent is undefined at this angle")
        result = math.tan(x)
    elif op == "log10":
        if a <= 0:
            raise HTTPException(400, "Logarithm requires a positive number")
        result = math.log10(a)
    elif op == "ln":
        if a <= 0:
            raise HTTPException(400, "Natural logarithm requires a positive number")
        result = math.log(a)
    elif op == "ten_power":
        result = 10 ** a
    elif op == "e_power":
        result = math.exp(a)
    elif op == "pi":
        result = math.pi
    elif op == "e":
        result = math.e
    elif op == "negate":
        result = -a
    elif op == "percent":
        result = a / 100

    else:
        raise HTTPException(status_code=400, detail="invalid operation")


    return {"result": result}


