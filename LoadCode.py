import pandas

def load_code():
    return pandas.read_csv('stocks-code-name.csv', header=None)

def load_code_ex():
    return pandas.read_csv('stocks-code.ex-name.csv', header=None)

