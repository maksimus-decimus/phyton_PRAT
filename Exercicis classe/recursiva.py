def suma_digitos(n):

    if n < 10:
        return n
    else:
        return (n%10) + suma_digitos(n//10)

n = 256
resultado = suma_digitos(n)
print(f"{resultado}")