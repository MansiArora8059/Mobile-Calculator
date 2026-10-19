from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
            raise HTTPException(status_code=400, detail= "wrong operation")
        result= a/b
    else:
        raise HTTPException(status_code=400, detail="wrong operation")


    return {"result": result}


