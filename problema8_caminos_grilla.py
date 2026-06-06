"""
================================================================
Problema 8: Caminos Mínimos en una Grilla
Matemáticas Discretas I — Universidad Nacional de Colombia
Docente: Jhoan Sebastian Tenjo García
================================================================

DESCRIPCIÓN MATEMÁTICA:
    Queremos contar cuántos caminos distintos existen desde la
    esquina (0,0) hasta la esquina (a,b) en una grilla rectangular,
    moviéndose ÚNICAMENTE hacia la derecha (→) o hacia arriba (↑).

    Cada camino mínimo consiste exactamente en:
        • a movimientos a la derecha  (→)
        • b movimientos hacia arriba  (↑)
    En total: a + b movimientos.

    El problema se reduce a: ¿de cuántas formas podemos ordenar
    'a' símbolos → y 'b' símbolos ↑ en una secuencia de (a+b)?

    Eso es exactamente el coeficiente binomial:

        C(a+b, a) = (a+b)! / (a! * b!)

    También escrito como C(a+b, b), pues C(n,r) = C(n, n-r).

EXTENSIÓN:
    El programa también permite:
      • Pasar por un punto obligatorio (px, py): se multiplican
        los caminos de (0,0)→(px,py) con los de (px,py)→(a,b).
      • Bloquear un punto (bx, by) para grillas pequeñas:
        se usan programación dinámica (tabla DP).

FÓRMULA USADA:
    Caminos(a, b) = C(a+b, a) = (a+b)! / (a! * b!)
"""


# ================================================================
# IMPORTACIONES
# ================================================================

# No se usan librerías externas: todo se implementa desde cero.


# ================================================================
# SECCIÓN 1: FACTORIAL Y COMBINACIONES
# ================================================================

def factorial(n: int) -> int:
    """
    Calcula n! de forma iterativa.

    Por qué iterativo y no recursivo:
        Python tiene un límite en la profundidad de recursión
        (~1000 niveles por defecto). Para grillas grandes,
        necesitamos factoriales de números como 200 o más,
        y la versión iterativa no tiene ese problema.

    Complejidad: O(n) tiempo, O(1) espacio.

    Parámetros:
        n (int): Entero no negativo.

    Retorna:
        int: Valor de n!
    """
    if not isinstance(n, int):
        raise TypeError(f"Se esperaba int, se recibió {type(n).__name__}.")
    if n < 0:
        raise ValueError(f"factorial no definido para n = {n}.")
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def combinacion(n: int, r: int) -> int:
    """
    Calcula C(n, r) = n! / (r! * (n-r)!)

    Esta es la fórmula central del problema: el número de
    caminos mínimos en una grilla de a×b es C(a+b, a).

    Parámetros:
        n (int): Total de movimientos (a + b).
        r (int): Movimientos en una dirección (a o b).

    Retorna:
        int: Número de combinaciones C(n, r).

    Lanza:
        ValueError: Si r > n o alguno es negativo.
    """
    if not isinstance(n, int) or not isinstance(r, int):
        raise TypeError("n y r deben ser enteros.")
    if n < 0 or r < 0:
        raise ValueError("n y r deben ser no negativos.")
    if r > n:
        raise ValueError(f"r no puede ser mayor que n (n={n}, r={r}).")

    # Optimización: usar min(r, n-r) para reducir operaciones
    r = min(r, n - r)
    resultado = 1
    for i in range(r):
        # C(n,r) = n/1 * (n-1)/2 * (n-2)/3 * ... * (n-r+1)/r
        resultado = resultado * (n - i) // (i + 1)
    return resultado


# ================================================================
# SECCIÓN 2: CAMINOS SIN RESTRICCIONES
# ================================================================

def caminos_minimos(a: int, b: int) -> int:
    """
    Cuenta caminos mínimos de (0,0) a (a,b) moviéndose solo
    → (derecha) o ↑ (arriba).

    Fórmula: C(a+b, a)

    Intuición: un camino es una secuencia de (a+b) movimientos,
    de los cuales exactamente 'a' son hacia la derecha.
    Escoger cuáles de los (a+b) pasos son '→' determina
    completamente el camino. Hay C(a+b, a) formas de hacerlo.

    Parámetros:
        a (int): Columnas a recorrer (movimientos →). a ≥ 0.
        b (int): Filas a recorrer (movimientos ↑).    b ≥ 0.

    Retorna:
        int: Número de caminos mínimos.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("a y b deben ser enteros.")
    if a < 0 or b < 0:
        raise ValueError("a y b deben ser no negativos.")

    # Caso borde: grilla degenerada (línea recta)
    # Si a=0, el único camino es ir todo hacia arriba.
    # Si b=0, el único camino es ir todo hacia la derecha.
    return combinacion(a + b, a)


# ================================================================
# SECCIÓN 3: CAMINO CON PUNTO OBLIGATORIO
# ================================================================

def caminos_con_punto_obligatorio(a: int, b: int,
                                   px: int, py: int) -> int:
    """
    Cuenta caminos de (0,0) a (a,b) que PASAN por el punto (px,py).

    Técnica: multiplicar los caminos de dos subproblemas independientes.
        Caminos(0,0)→(px,py) × Caminos(px,py)→(a,b)

    El segundo subproblema es equivalente a Caminos(a-px, b-py).

    Parámetros:
        a, b   : Destino final.
        px, py : Punto obligatorio por el que debe pasar el camino.

    Retorna:
        int: Número de caminos que pasan por (px, py).

    Lanza:
        ValueError: Si (px,py) está fuera del rectángulo (0,0)→(a,b).
    """
    for val, nombre in [(a,'a'),(b,'b'),(px,'px'),(py,'py')]:
        if not isinstance(val, int) or val < 0:
            raise ValueError(f"{nombre} debe ser entero no negativo.")
    if px > a or py > b:
        raise ValueError(
            f"El punto ({px},{py}) está fuera de la grilla "
            f"(0,0)→({a},{b})."
        )

    # Caminos de (0,0) a (px,py)
    tramo1 = caminos_minimos(px, py)
    # Caminos de (px,py) a (a,b)  ≡  caminos de (0,0) a (a-px, b-py)
    tramo2 = caminos_minimos(a - px, b - py)

    return tramo1 * tramo2


# ================================================================
# SECCIÓN 4: CAMINOS CON PUNTO BLOQUEADO (programación dinámica)
# ================================================================

def caminos_con_bloqueo(a: int, b: int, bx: int, by: int) -> int:
    """
    Cuenta caminos de (0,0) a (a,b) que EVITAN el punto (bx,by),
    usando programación dinámica (tabla DP).

    Algoritmo:
        dp[i][j] = número de caminos de (0,0) a (i,j).
        dp[i][j] = dp[i-1][j] + dp[i][j-1]   (desde abajo o desde la izquierda)
        dp[bx][by] = 0  (el punto bloqueado no es alcanzable)

    Complejidad: O(a*b) tiempo y espacio.

    Parámetros:
        a, b   : Destino final.
        bx, by : Punto bloqueado.

    Retorna:
        int: Número de caminos que evitan (bx,by).
    """
    for val, nombre in [(a,'a'),(b,'b'),(bx,'bx'),(by,'by')]:
        if not isinstance(val, int) or val < 0:
            raise ValueError(f"{nombre} debe ser entero no negativo.")
    if bx > a or by > b:
        raise ValueError(
            f"El punto bloqueado ({bx},{by}) está fuera de la grilla."
        )
    if (bx == 0 and by == 0) or (bx == a and by == b):
        raise ValueError("No puedes bloquear el origen o el destino.")

    # Construir tabla DP de tamaño (a+1) x (b+1)
    dp = [[0] * (b + 1) for _ in range(a + 1)]
    dp[0][0] = 1  # Hay 1 forma de estar en el punto de partida

    for i in range(a + 1):
        for j in range(b + 1):
            if i == 0 and j == 0:
                continue  # ya inicializado
            if i == bx and j == by:
                dp[i][j] = 0  # punto bloqueado
                continue
            # Sumar caminos que llegan desde la izquierda y desde abajo
            desde_izquierda = dp[i - 1][j] if i > 0 else 0
            desde_abajo     = dp[i][j - 1] if j > 0 else 0
            dp[i][j] = desde_izquierda + desde_abajo

    return dp[a][b]


# ================================================================
# SECCIÓN 5: VISUALIZACIÓN DE LA GRILLA (texto)
# ================================================================

def dibujar_grilla(a: int, b: int) -> None:
    """
    Dibuja en texto la grilla con los números de caminos
    desde (0,0) hasta cada celda. Solo para grillas pequeñas (≤10).
    """
    if a > 10 or b > 10:
        print("  (Grilla muy grande para dibujar)")
        return

    # Calcular la tabla completa
    dp = [[0] * (b + 1) for _ in range(a + 1)]
    dp[0][0] = 1
    for i in range(a + 1):
        for j in range(b + 1):
            if i == 0 and j == 0:
                continue
            dp[i][j] = (dp[i-1][j] if i > 0 else 0) + (dp[i][j-1] if j > 0 else 0)

    # Imprimir de arriba (b) hacia abajo (0) para que sea intuitivo
    ancho = len(str(dp[a][b])) + 1
    print(f"\n  Tabla de caminos hasta cada celda (origen abajo-izquierda):\n")
    for j in range(b, -1, -1):
        fila = f"  j={j}  "
        for i in range(a + 1):
            fila += str(dp[i][j]).rjust(ancho) + " "
        print(fila)
    print("       " + "".join(f"i={i}".rjust(ancho+1) for i in range(a + 1)))
    print()


# ================================================================
# SECCIÓN 6: LECTURA DE ENTRADAS
# ================================================================

def leer_entero(mensaje: str, minimo: int = 0) -> int:
    """
    Pide un entero al usuario con validación.
    Sigue preguntando hasta recibir un valor válido.
    """
    while True:
        entrada = input(mensaje).strip()
        if not entrada.lstrip('-').isdigit():
            print(f"  ✗ '{entrada}' no es un número entero válido.")
            continue
        valor = int(entrada)
        if valor < minimo:
            print(f"  ✗ El valor mínimo aceptado es {minimo}.")
            continue
        return valor


def leer_opcion_si_no(mensaje: str) -> bool:
    """Pide una respuesta s/n al usuario."""
    while True:
        entrada = input(mensaje + " (s/n): ").strip().lower()
        if entrada in ("s", "si", "sí", "yes", "y"):
            return True
        if entrada in ("n", "no"):
            return False
        print("  ✗ Responde 's' para sí o 'n' para no.")


# ================================================================
# SECCIÓN 7: PROGRAMA PRINCIPAL (INTERACTIVO)
# ================================================================

def main():
    print("\n" + "=" * 55)
    print("  PROBLEMA 8 — Caminos Mínimos en una Grilla")
    print("  Matemáticas Discretas I · UNAL")
    print("=" * 55)

    print("""
  ¿Qué cuenta este programa?
  ─────────────────────────────────────────────────────
  Dada una grilla de a columnas × b filas, cuenta
  cuántos caminos mínimos hay desde (0,0) hasta (a,b)
  moviéndose solo → (derecha) o ↑ (arriba).

  La fórmula es: C(a+b, a) = (a+b)! / (a! · b!)
  ─────────────────────────────────────────────────────
    """)

    # ── Pedir dimensiones ─────────────────────────────────────
    a = leer_entero("  Ingresa a (columnas a recorrer, a ≥ 1): ", minimo=1)
    b = leer_entero("  Ingresa b (filas a recorrer,    b ≥ 1): ", minimo=1)

    # ── Resultado básico con procedimiento ───────────────────
    print(f"\n  {'─'*50}")
    print(f"  Grilla: desde (0,0) hasta ({a},{b})")
    print(f"  {'─'*50}")
    print(f"  Total de movimientos : a + b = {a} + {b} = {a+b}")
    print(f"  Movimientos → (derecha) : {a}")
    print(f"  Fórmula : C({a+b}, {a}) = ({a+b})! / ({a}! × {b}!)")
    print(f"  Cálculo : {factorial(a+b):,} / ({factorial(a):,} × {factorial(b):,})")
    resultado_base = caminos_minimos(a, b)
    print(f"  Resultado : {resultado_base:,} caminos mínimos")
    print(f"  {'─'*50}\n")

    # ── Dibujar grilla si es pequeña ──────────────────────────
    if a <= 10 and b <= 10:
        dibujar_grilla(a, b)

    # ── Tabla para distintos tamaños de grilla ────────────────
    print("  Tabla comparativa de caminos para distintas grillas:\n")
    print(f"  {'(a,b)':>10}  {'C(a+b,a)':>15}")
    print(f"  {'─'*10}  {'─'*15}")
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            if i + j <= a + b:  # solo mostrar grillas menores o iguales
                c = caminos_minimos(i, j)
                print(f"  ({i},{j}){'':<6}  {c:>15,}")
    print()

    # ── Punto obligatorio ─────────────────────────────────────
    if leer_opcion_si_no("\n  ¿Deseas agregar un punto OBLIGATORIO por el que debe pasar el camino?"):
        print(f"  (El punto debe estar dentro de la grilla: 0 ≤ px ≤ {a}, 0 ≤ py ≤ {b})")
        px = leer_entero(f"  Ingresa px (0 a {a}): ", minimo=0)
        py = leer_entero(f"  Ingresa py (0 a {b}): ", minimo=0)
        try:
            r_oblig = caminos_con_punto_obligatorio(a, b, px, py)
            tramo1  = caminos_minimos(px, py)
            tramo2  = caminos_minimos(a - px, b - py)
            print(f"\n  Razonamiento:")
            print(f"    Caminos (0,0)→({px},{py})         = {tramo1:,}")
            print(f"    Caminos ({px},{py})→({a},{b})  = {tramo2:,}")
            print(f"    Total = {tramo1:,} × {tramo2:,} = {r_oblig:,} caminos\n")
        except ValueError as e:
            print(f"  ✗ Error: {e}")

    # ── Punto bloqueado ───────────────────────────────────────
    if leer_opcion_si_no("  ¿Deseas bloquear un punto por el que el camino NO puede pasar?"):
        print(f"  (El punto no puede ser el origen ni el destino)")
        bx = leer_entero(f"  Ingresa bx (0 a {a}): ", minimo=0)
        by = leer_entero(f"  Ingresa by (0 a {b}): ", minimo=0)
        try:
            r_bloq = caminos_con_bloqueo(a, b, bx, by)
            print(f"\n  Caminos que evitan ({bx},{by}): {r_bloq:,}")
            print(f"  Caminos bloqueados por el punto : {resultado_base - r_bloq:,}\n")
        except ValueError as e:
            print(f"  ✗ Error: {e}")

    # ── Eficiencia ────────────────────────────────────────────
    print(f"""
  ── Eficiencia del algoritmo ──────────────────────────
  • Fórmula directa C(a+b,a): O(min(a,b)) operaciones.
    Muy eficiente para cualquier tamaño de grilla.

  • Tabla DP (para puntos bloqueados): O(a×b) tiempo y
    espacio. Crece con el área de la grilla, pero es
    manejable para grillas de cientos de celdas.

  • Python usa enteros de precisión arbitraria, así que
    no hay desbordamiento incluso para grillas enormes
    como (100, 100) → C(200,100) ≈ 9 × 10^58.
  ──────────────────────────────────────────────────────
    """)


# ================================================================
# PUNTO DE ENTRADA
# ================================================================

if __name__ == "__main__":
    main()
