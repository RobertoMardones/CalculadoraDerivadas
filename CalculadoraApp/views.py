from django.shortcuts import render
from django.http import HttpResponse


#############################################
from django.shortcuts import render
from sympy import symbols, diff, latex, sympify
from sympy.parsing.sympy_parser import parse_expr
#############################################


# Create your views here.


#Derivadas
def inicio(request):
    funcion_str = ""
    derivada = ""
    pasos = []
    
    if request.method == 'POST':
        funcion_str = request.POST.get('funcion', '').strip()
        x = symbols('x')
        
        try:
            # Convertir entrada (ej: "x^2" -> "x**2")
            funcion_str_parsed = funcion_str.replace('^', '**')
            funcion = parse_expr(funcion_str_parsed)
            
            # Calcular derivada
            # Pasos a derivar CON REGLAS DE DERIVACION
            derivada = diff(funcion, x)
            #PARA DERIVAR UN PRODUCTO (BINOMIO)TIENES Q RESOLVERLO Y DESPUES DERIVAR
            #O
            #PARA DERIVAR UN PRODUCTO (BINOMIO) DERIVAS TODO LO DEL BINOMIO PARA DESPUES MULTIPLICAR POR EL PRIMERO MULTIPLICADO POR EL SEGUNDO DERIVADO + EL PRIMERO DERIVADO MULTIPLICADO POR EL SEGUNDO
            es = es_binomio(funcion)
            #PARA DERIVAR UNA FUNCION CON RAIZ SE DIVIDE EL EXPONENTE POR LA RAIZ YA SEA CUBICA O CUADRADA O A LA CUARTA, ETC, Y DESPUES DERIVAS
            eso = es_raiz(funcion)
            #PARA DERIVAR UNA FUNCION QUE ES UNA DIVISION SOLO SE SUBE EL EXPONENTE Y LO HACEMOS NEGATIVO, Y MULTIPLICAMOS N*X Y EL EXPONENTE, DESPUES SE DERIVA Y SE CONVIERTE EL EXPONENTE NEGATIVO A FRACCION
            #Y PARA DERIVAR UNA FUNCION CON UN NUMERO Y X SE USA LA REGLA DE EXPOTENTE: BAJAR EL EXPONENTE Y SI ES QUE HAY UN NUMERO QUE ACOMPAÑE LA X MULTIPLICARLO,DESPUES ESCRIBIR LA X Y RESTAR EL EXPONENTE CON UN -1
            esot = es_division_con_exponente(funcion)
            #PARA DERIVAR UNA FUNCION QUE SOLO SEA X SIEMPRE SERA 1
            esoti = es_solo_x_o_x_potencia(funcion)
            #PARA DERIVAR UNA FUNCION QUE SOLO SEA UN NUMERO SIEMPRE SERA 0
            esotil = es_solo_numero(funcion)
            #PRODUCTO TRIPLE LO DEJAMOS PARA OTRO DIA XDDD
            # Generar pasos (personaliza según tus necesidades)
            print(f"\nFUNCIÓN ORIGINAL: {funcion}")
            x = symbols('x')

            if es_raiz(funcion):
                print("🔹 TIPO: Función con raíz")
                print("   Reescribiendo como exponente y derivando...")
                pasos= [
                    {"Regla":"PASO A PASO LA RAIZ",
                     "expresion": "Expresion de ejemplo  --> √x"},
                    {"regla": "Paso 1: Convertir la raiz en un exponente", 
                    "expresion": "√x    -->  x^1/2"},
                    {"regla": "Paso 2: Baja el exponente", 
                    "expresion": "x^1/2    -->  1/2(x)^1/2"},
                    {"regla": "Paso 3: Resta el exponente", 
                    "expresion": "1/2(x)^1/2 -->  1/2(x)^1/2-1"},
                    {"regla": "Paso 4: Deriva lo que estaba en la raiz", 
                    "expresion": "x -->  1"},
                    {"regla": "Paso 5: Multiplica por la derivada", 
                    "expresion": "1/2(x)^1/2-1 -->  (1/2(x)^1/2-1)*(x)"},
                    {"Titulo":"PASOS EXTRA SI HAY EXPONENTE NEGATIVO"},
                    {"regla": "Paso 6: Cambia de signo el exponente negativo a base de una fraccion", 
                    "expresion": "(1/2(x)^1/2-1)*(x) -->  (1/2*(x)/(x)^1/2-1)"},
                ]
            elif es_binomio(funcion):
                print("🔹 TIPO: Binomio")
                print("   Aplicando regla de la cadena...")
                pasos= [
                    {"Regla":"PASO A PASO EL BINOMIO",
                     "expresion": "Expresion de ejemplo  -->(x^2-nx)(x^3+nx)"},
                    {"regla": "Paso 1: Derivar el Primero", 
                    "expresion": "(x^2-nx)    -->  (2x-n)"},
                    {"regla": "Paso 2: Deriva el segundo", 
                    "expresion": "(x^3+nx)    -->  (3x^2-n)"},
                    {"regla": "Paso 3: Multiplica el Primero por la derivada del segundo", 
                    "expresion": "(x^2-nx)(3x^2-n)"},
                    {"regla": "Paso 4: Sumar la Multiplicacion del Segundo por la derivada del Primero", 
                    "expresion": "(x^2-nx)(3x^2-n) -->  (x^2-nx)(3x^2-n)+(x^3+nx)(2x-n)"},
                    {"regla": "Paso 5: Multiplica los productos", 
                    "expresion": "(x^2-nx)(3x^2-n) -->  (3x^4-nx^2-3nx^2+2nx)"},
                    {"regla": "Paso 6: Suma", 
                    "expresion": "(3x^4-nx^2-3nx^2+2nx) -->  (3x^4-4nx^2+2nx)"},
                    {"regla": "Paso 7: Multiplica los otros productos", 
                    "expresion": "(x^3+nx)(2x-n) -->  (x^3*2x+x^3*(-n)+nx*2x+nx*(-n))"},
                    {"regla": "Paso 8: Suma", 
                    "expresion": "(x^3*2x+x^3*(-n)+nx*2x+nx*(-n)) -->  2x^4-nx^3+2x^2n-n^2x"},
                    {"regla": "Paso 9: Suma todo", 
                    "expresion": "3x^4-4nx^2+2nx+2x^4-nx^3+2x^2n-n^2x -->  5x^4-nx^3-2nx^2+(2n-n^2)x"},
                ]

            elif es_mono(funcion):
                print("🔹 TIPO: Polinomio simple (coeficiente * x^n)")
                print("   Paso 1: Aplicar regla de la potencia a cada término.")
                pasos= [
                    {"regla": "PASO A PASO MONOMIO", 
                    "expresion": "Expresion de ejemplo -->  3x^4"},
                    {"regla": "Bajar el exponente", 
                    "expresion": "3x^4    -->  4*3x^4"},
                    {"regla": "Restarle 1 al exponente", 
                    "expresion": "4*3x^4-1    -->  4*3x^3"},
                    {"regla": "Multiplicar", 
                    "expresion": "4*3x^3    -->  12x^3"},
                ]
            #por ahora no funciona
            elif es_solo_x_o_x_potencia(funcion):
                pasos= [
                    {"regla": "Paso 1: Divide el exponente  |   ", 
                    "expresion": "x^2    -->  2*x^2"},
                    {"regla": "Paso 2: Multiplicalo por coeficiente (x)", 
                    "expresion": "x^2    -->  2x^2"},
                    {"regla": "Paso 3: Resta el exponente", 
                    "expresion": "2x^2-1 -->  2x^1  --> 2x"},
                ]
                print(pasos)

            #tampoco funciona
            elif es_solo_numero(funcion):
                print("🔹 TIPO: Solo un número (constante)")
                print("   La derivada de una constante es 0")
                derivada = 0
                pasos= [
                    {"regla": "TODA FUNCION QUE SEA CONSTANTE SERA 0", 
                    "expresion": "2    -->  0"}
                ]
            else:
                print("🔹 TIPO: No reconocido (derivando genéricamente)")
                derivada = diff(funcion, x)

            print(f"   DERIVADA: {derivada}")
            
        except Exception as e:
            pasos = [{"regla": "Error", "expresion": f"Entrada no válida: {e}"}]
    
    return render(request, 'index.html', {
        'funcion': funcion_str,
        'derivada': latex(derivada) if derivada else "",
        'pasos': pasos,
    })

#Limites
# def Limites()

#Binomio
from sympy import sympify, Add, Pow, Mul

def es_binomio(funcion):
    try:
        expr = sympify(funcion)
        
        # Caso 1: Es un binomio lineal (ej: x + 1)
        if isinstance(expr, Add) and len(expr.args) == 2:
            return True
        
        # Caso 2: Es una potencia de un binomio (ej: (x + 2)**3)
        elif isinstance(expr, Pow):
            base = expr.base
            if isinstance(base, Add) and len(base.args) == 2:
                return True
        
        # Caso 3: Es un binomio multiplicado por un escalar (ej: 5*(x - 1))
        elif isinstance(expr, Mul):
            for arg in expr.args:
                if isinstance(arg, Add) and len(arg.args) == 2:
                    return True
        
        return False
    
    except:
        return False  # Si no se puede parsear, no es binomio
    

from sympy import sympify, Pow, sqrt, Rational, Symbol
#Raiz
def es_raiz(funcion):
    try:
        expr = sympify(funcion)
        
        # Caso 1: Raíz cuadrada directa (sqrt(x))
        if expr.func == sqrt:
            return f"True (raíz cuadrada: {expr})"
        
        # Caso 2: Potencia con exponente fraccionario (x^(1/n))
        if isinstance(expr, Pow):
            base, exp = expr.base, expr.exp
            if isinstance(exp, Rational) and exp.denominator != 1:
                return f"True (raíz {exp.denominator}-ésima: {base}^(1/{exp.denominator}))"
        
        return False
    
    except:
        return False  # Si no se puede parsear, no es una raíz
    
from sympy import sympify, Pow, Rational, Mul, S

#Division con exponente n/x^n
def es_division_con_exponente(funcion):
    try:
        expr = sympify(funcion)
        
        # Caso 1: La expresión es una potencia con exponente negativo (x**(-n))
        if isinstance(expr, Pow) and expr.exp.is_negative:
            return f"True (división como exponente negativo: {expr})"
        
        # Caso 2: La expresión es una multiplicación por un exponente negativo (ej: 2*x**(-3))
        if isinstance(expr, Mul):
            for arg in expr.args:
                if isinstance(arg, Pow) and arg.exp.is_negative:
                    return f"True (multiplicación con exponente negativo: {expr})"
        
        # Caso 3: División clásica (1/x, 1/(x + 1), etc.)
        if expr.is_Pow and expr.exp == -1:
            return f"True (división directa: {expr})"
        
        return False
    
    except:
        return False  # Si no se puede parsear, no es una división con exponente
    

from sympy import sympify, symbols, Pow
#Funcion solo con x

def es_solo_x_o_x_potencia(funcion):
    try:
        expr = sympify(funcion)
        x = symbols('x')
        
        # Caso 1: Es exactamente 'x'
        if expr == x:
            return True
        
        # Caso 2: Es 'x' elevado a un número (como x^2, x^3, etc.)
        if isinstance(expr, Pow) and expr.base == x and expr.exp.is_number:
            return True
        
        return False
    
    except:
        return False  # Si no se puede parsear, no es válido
    
from sympy import sympify, Number, Symbol
#Solo un numero
def es_solo_numero(funcion):
    try:
        expr = sympify(funcion)
        
        # Verifica si es un número y no contiene símbolos (como 'x', 'y', etc.)
        if isinstance(expr, Number) and not expr.free_symbols:
            return True
        return False
    
    except:
        return False  # Si no se puede parsear, no es un número válido
#der

from sympy import symbols, Add, Mul, Pow, Number
from sympy.core.numbers import Integer, Rational, Float


def es_mono(expr):
    # Si es monomio, retorna True
    if is_monomial(expr):
        return True
    # Si es una suma, verificamos que todos sus términos sean monomios (ej: x + y → False)
    elif isinstance(expr, Add):
        return all(is_monomial(term) for term in expr.args)
    # Si no es ni monomio ni suma, retornamos False
    else:
        return False
    
def is_monomial(expr):
    # Caso 1: Es un número (constante) → monomio (ej: 5, -3, 0.5)
    if isinstance(expr, (Number, Integer, Rational, Float)):
        return True
    # Caso 2: Es un símbolo puro (ej: x, y) → monomio
    elif expr.is_Symbol:
        return True
    # Caso 3: Es una potencia x**n, donde n es entero no negativo (ej: x**2)
    elif isinstance(expr, Pow) and expr.exp.is_integer and expr.exp >= 0:
        return is_monomial(expr.base)  # Verificamos que la base sea monomio
    # Caso 4: Es una multiplicación (ej: 2*x*y)
    elif isinstance(expr, Mul):
        return all(is_monomial(arg) for arg in expr.args)
    # Si no cumple ninguno, no es monomio
    else:
        return False