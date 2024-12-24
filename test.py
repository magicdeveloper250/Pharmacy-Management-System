num1= input("Num1: ")
num2= input("Num2: ")
operator= input("opeartor: ")

def add(num1, num2):
    try:
        num1= int(num1)
        num2= int(num2)
        return num1 + num2
    except ValueError:
        print("Only number are allowed")
        return 1



def calculate(num1, num2, operator):
    if operator=="add":
        return add(num1, num2)
    
if __name__=="__main__":
    calculate()
