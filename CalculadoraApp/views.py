from django.shortcuts import render
from django.http import HttpResponse


#############################################
from django.shortcuts import render
from sympy import symbols, diff, latex, sympify
from sympy.parsing.sympy_parser import parse_expr
#############################################


# Create your views here.



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
            derivada = diff(funcion, x)
            
            # Generar pasos (personaliza según tus necesidades)
            pasos = [
                {"regla": "Función original", "expresion": f"\( {latex(funcion)} \)"},
                {"regla": "Aplicando reglas de derivación", "expresion": ""},
                {"regla": "Regla de la potencia", "expresion": r"\( \frac{d}{dx} x^n = n x^{n-1} \)"},
                {"regla": "Derivada final", "expresion": f"\( {latex(derivada)} \)"},
            ]
            
        except Exception as e:
            pasos = [{"regla": "Error", "expresion": f"Entrada no válida: {e}"}]
    
    return render(request, 'index.html', {
        'funcion': funcion_str,
        'derivada': latex(derivada) if derivada else "",
        'pasos': pasos,
    })