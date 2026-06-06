"""
================================================================
Problema 6: Permutaciones Circulares
Matemáticas Discretas I — Universidad Nacional de Colombia
Docente: Jhoan Sebastian Tenjo García
================================================================

DESCRIPCIÓN MATEMÁTICA:
    Una permutación circular es un arreglo de n objetos distintos
    alrededor de una mesa (o en un círculo), donde dos arreglos
    se consideran IGUALES si uno se puede obtener rotando el otro.

    Ejemplo: si tenemos 3 personas A, B, C sentadas en círculo,
    los arreglos (A,B,C), (B,C,A) y (C,A,B) son el MISMO arreglo
    porque son simplemente rotaciones uno del otro.

    Por eso dividimos entre n (las n rotaciones posibles de cada
    arreglo lineal), y obtenemos:

        Permutaciones circulares = n! / n = (n-1)!

RESTRICCIONES ADICIONALES:
    El programa también permite calcular casos con restricciones:
      a) Dos personas DEBEN quedar juntas  → se tratan como bloque
      b) Dos personas NO pueden quedar juntas → complemento
      c) k personas de un grupo deben estar separadas

FÓRMULA USADA:
    - Sin restricciones   : (n - 1)!
    - Con 2 juntos        : 2 * (n - 2)!   [bloque cuenta como 1 objeto,
                                             el 2 por las 2 formas del bloque]
    - Con 2 separados     : (n-1)! - 2*(n-2)!
"""


# ================================================================
# IMPORTACIONES
# ================================================================

import math  # usamos math.factorial para verificación interna


# ================================================================
# SECCIÓN 1: FUNCIÓN DE FACTORIAL
# Implementación propia para mostrar el proceso, sin depender
# de librerías externas en el cálculo principal.
# ================================================================

def factorial(n: int) -> int:
    """
    Calcula n! de forma iterativa.

    Complejidad temporal : O(n)  — un solo recorrido del bucle
    Complejidad espacial : O(1)  — solo una variable acumuladora

    Parámetros:
        n (int): Entero no negativo.

    Retorna:
        int: El valor de n!

    Lanza:
        ValueError: Si n es negativo.
        TypeError : Si n no es entero.
    """
    # --- Validación de tipo ---
    if not isinstance(n, int):
        raise TypeError(f"Se esperaba un entero, se recibió {type(n).__name__}.")

    # --- Validación de dominio ---
    if n < 0:
        raise ValueError(f"El factorial no está definido para n = {n}.")

    # --- Caso base: 0! = 1 (por definición matemática) ---
    if n == 0:
        return 1

    # --- Cálculo iterativo ---
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i  # acumula: 1 * 2 * 3 * ... * n

    return resultado


# ================================================================
# SECCIÓN 2: PERMUTACIONES CIRCULARES SIN RESTRICCIONES
# ================================================================

def perm_circular(n: int) -> int:
    """
    Calcula el número de permutaciones circulares de n objetos.

    Fórmula: (n - 1)!

    Intuición: fijamos un objeto en una posición para eliminar las
    n rotaciones equivalentes, y ordenamos los n-1 restantes: (n-1)!

    Parámetros:
        n (int): Número de objetos (debe ser ≥ 1).

    Retorna:
        int: Número de permutaciones circulares distintas.

    Lanza:
        ValueError: Si n < 1.
    """
    if not isinstance(n, int):
        raise TypeError("n debe ser un entero.")
    if n < 1:
        raise ValueError(f"Se necesita al menos 1 objeto (recibido n = {n}).")
    if n == 1:
        # Un solo objeto en círculo: solo 1 forma posible
        return 1

    return factorial(n - 1)


# ================================================================
# SECCIÓN 3: RESTRICCIONES
# ================================================================

def perm_circular_dos_juntos(n: int) -> int:
    """
    Cuenta permutaciones circulares donde DOS personas específicas
    DEBEN quedar juntas (adyacentes).

    Razonamiento:
        - Tratamos a las 2 personas como un bloque → quedan (n-1) objetos.
        - Permutaciones circulares de (n-1) objetos: (n-2)!
        - El bloque puede ordenarse internamente de 2 formas (AB o BA).
        - Total: 2 * (n - 2)!

    Parámetros:
        n (int): Total de personas en la mesa (n ≥ 2).

    Retorna:
        int: Número de arreglos donde las 2 personas quedan juntas.
    """
    if not isinstance(n, int):
        raise TypeError("n debe ser un entero.")
    if n < 2:
        raise ValueError(f"Se necesitan al menos 2 personas (recibido n = {n}).")

    return 2 * factorial(n - 2)


def perm_circular_dos_separados(n: int) -> int:
    """
    Cuenta permutaciones circulares donde DOS personas específicas
    NO pueden quedar juntas (nunca adyacentes).

    Razonamiento (principio de complemento):
        Total sin restricción  = (n-1)!
        Casos donde SÍ quedan juntos = 2*(n-2)!
        Casos donde NO quedan juntos = (n-1)! - 2*(n-2)!

    Parámetros:
        n (int): Total de personas (n ≥ 2).

    Retorna:
        int: Número de arreglos donde las 2 personas NO quedan juntas.
    """
    if not isinstance(n, int):
        raise TypeError("n debe ser un entero.")
    if n < 2:
        raise ValueError(f"Se necesitan al menos 2 personas (recibido n = {n}).")

    total    = perm_circular(n)
    juntos   = perm_circular_dos_juntos(n)
    separados = total - juntos

    return separados


# ================================================================
# SECCIÓN 4: FUNCIONES DE PRESENTACIÓN
# ================================================================

def mostrar_resultado(titulo: str, valor: int) -> None:
    """Imprime un resultado con formato uniforme."""
    print(f"  {'─'*45}")
    print(f"  {titulo}")
    print(f"  Resultado : {valor:,}")
    print(f"  {'─'*45}\n")


def explicar_formula(n: int) -> None:
    """Muestra paso a paso el cálculo de (n-1)!"""
    print(f"\n  ┌─ Procedimiento para n = {n} ────────────────────┐")
    print(f"  │  Fórmula     : (n - 1)!                        │")
    print(f"  │  Sustitución : ({n} - 1)! = {n-1}!               │")
    print(f"  │  Cálculo     : {n-1}! = {factorial(n-1):,}{'':>10}│")
    print(f"  └────────────────────────────────────────────────┘\n")


# ================================================================
# SECCIÓN 5: LECTURA DE ENTRADAS DEL USUARIO
# ================================================================

def leer_entero(mensaje: str, minimo: int = 1) -> int:
    """
    Solicita al usuario un entero por teclado con validación.

    Sigue pidiendo hasta que el usuario ingrese un valor válido.

    Parámetros:
        mensaje (str): Texto que se muestra al usuario.
        minimo  (int): Valor mínimo aceptable.

    Retorna:
        int: El entero ingresado por el usuario.
    """
    while True:
        entrada = input(mensaje).strip()
        # Verificar que sea un número entero
        if not entrada.lstrip('-').isdigit():
            print(f"  ✗ '{entrada}' no es un número entero. Intenta de nuevo.")
            continue
        valor = int(entrada)
        if valor < minimo:
            print(f"  ✗ El valor debe ser mayor o igual a {minimo}. Recibido: {valor}.")
            continue
        return valor


def leer_opcion(opciones: list) -> str:
    """
    Muestra un menú y pide al usuario que elija una opción válida.

    Parámetros:
        opciones (list): Lista de strings con las opciones.

    Retorna:
        str: La opción elegida.
    """
    for i, op in enumerate(opciones, 1):
        print(f"    [{i}] {op}")
    while True:
        entrada = input("  Tu elección: ").strip()
        if entrada.isdigit() and 1 <= int(entrada) <= len(opciones):
            return opciones[int(entrada) - 1]
        print(f"  ✗ Opción inválida. Elige entre 1 y {len(opciones)}.")


# ================================================================
# SECCIÓN 6: PROGRAMA PRINCIPAL (INTERACTIVO)
# ================================================================

def main():
    """
    Punto de entrada del programa.
    Guía al usuario paso a paso para calcular permutaciones circulares.
    """
    print("\n" + "=" * 55)
    print("  PROBLEMA 6 — Permutaciones Circulares")
    print("  Matemáticas Discretas I · UNAL")
    print("=" * 55)

    print("""
  ¿Qué cuenta este programa?
  ─────────────────────────────────────────────────────
  Imagina n personas sentadas alrededor de una mesa
  circular. ¿De cuántas formas distintas pueden
  acomodarse, si dos arreglos que son rotaciones
  entre sí se consideran IGUALES?

  Respuesta: (n - 1)!
  ─────────────────────────────────────────────────────
    """)

    # ── Pedir n al usuario ────────────────────────────────────
    n = leer_entero("  Ingresa el número de personas (n ≥ 2): ", minimo=2)

    # ── Mostrar fórmula paso a paso ───────────────────────────
    explicar_formula(n)

    # ── Resultado sin restricciones ───────────────────────────
    total = perm_circular(n)
    mostrar_resultado(
        f"Sin restricciones → ({n}-1)! = {n-1}! = {total:,}",
        total
    )

    # ── Preguntar si el usuario quiere restricciones ──────────
    print("  ¿Deseas calcular con restricciones?\n")
    opciones_rest = [
        "Sí, dos personas DEBEN quedar juntas",
        "Sí, dos personas NO pueden quedar juntas",
        "No, solo quería el resultado básico"
    ]
    eleccion = leer_opcion(opciones_rest)
    print()

    if "juntas" in eleccion and "NO" not in eleccion:
        # ── Dos juntos ────────────────────────────────────────
        resultado = perm_circular_dos_juntos(n)
        print(f"  Razonamiento:")
        print(f"    • Tratamos a las 2 personas como un bloque.")
        print(f"    • Quedan {n-1} objetos en círculo → ({n-2})! = {factorial(n-2):,} arreglos.")
        print(f"    • El bloque puede ordenarse de 2 formas (AB o BA).")
        print(f"    • Total = 2 × {factorial(n-2):,} = {resultado:,}\n")
        mostrar_resultado(
            f"Dos personas JUNTAS → 2 × ({n}-2)! = {resultado:,}",
            resultado
        )

    elif "NO" in eleccion:
        # ── Dos separados ─────────────────────────────────────
        resultado  = perm_circular_dos_separados(n)
        juntos_val = perm_circular_dos_juntos(n)
        print(f"  Razonamiento (complemento):")
        print(f"    • Total sin restricción        = ({n}-1)! = {total:,}")
        print(f"    • Casos donde SÍ quedan juntos = 2×({n}-2)! = {juntos_val:,}")
        print(f"    • Casos donde NO quedan juntos = {total:,} - {juntos_val:,} = {resultado:,}\n")
        mostrar_resultado(
            f"Dos personas SEPARADAS → {total:,} - {juntos_val:,} = {resultado:,}",
            resultado
        )

    # ── Tabla comparativa para distintos valores de n ─────────
    print("  Tabla: permutaciones circulares para distintos n")
    print(f"  {'n':>4}  {'(n-1)!':>15}  {'2 juntos':>12}  {'2 separados':>14}")
    print(f"  {'─'*4}  {'─'*15}  {'─'*12}  {'─'*14}")
    for k in range(2, n + 1):
        t  = perm_circular(k)
        j  = perm_circular_dos_juntos(k)
        s  = perm_circular_dos_separados(k)
        # Para k=2 o k=3, "separados" puede ser 0 o negativo:
        # con 2 personas en círculo siempre son adyacentes.
        s_str = f"{s:,}" if s >= 0 else "N/A"
        print(f"  {k:>4}  {t:>15,}  {j:>12,}  {s_str:>14}")

    # ── Nota de eficiencia ────────────────────────────────────
    print(f"""
  ── Eficiencia del algoritmo ──────────────────────────
  • Calcular (n-1)! requiere O(n) multiplicaciones.
  • Todas las restricciones se calculan con O(1) llamadas
    al factorial, así que el costo total sigue siendo O(n).
  • Para n muy grandes, los números crecen muy rápido
    (factoriales), pero Python maneja enteros de precisión
    arbitraria, así que no hay desbordamiento.
  ──────────────────────────────────────────────────────
    """)


# ================================================================
# PUNTO DE ENTRADA
# ================================================================

if __name__ == "__main__":
    main()
