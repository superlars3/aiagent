import sys

def calculate(expression):
    tokens = expression
    
    # Handle multiplication and division first
    i = 1
    while i < len(tokens) - 1:
        if tokens[i] == '*':
            tokens[i-1] = float(tokens[i-1]) * float(tokens[i+1])
            del tokens[i:i+2]
            i = 1
        elif tokens[i] == '/':
            tokens[i-1] = float(tokens[i-1]) / float(tokens[i+1])
            del tokens[i:i+2]
            i = 1
        else:
            i += 2

    # Handle addition and subtraction
    result = float(tokens[0])
    i = 1
    while i < len(tokens) - 1:
        if tokens[i] == '+':
            result += float(tokens[i+1])
        elif tokens[i] == '-':
            result -= float(tokens[i+1])
        i += 2

    return result

if __name__ == "__main__":
    expression = sys.argv[1:]
    result = calculate(expression)
    print(result)
