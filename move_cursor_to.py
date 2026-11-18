

import argparse
import ctypes
import json
import math
import sys
import time
import random
from ctypes import wintypes


def get_screen_size() -> tuple[int, int]:
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def get_cursor_pos() -> tuple[int, int]:
    point = wintypes.POINT()
    if not ctypes.windll.user32.GetCursorPos(ctypes.byref(point)):
        raise ctypes.WinError()
    return point.x, point.y


def set_cursor_pos(x: int, y: int) -> None:
    if not ctypes.windll.user32.SetCursorPos(x, y):
        raise ctypes.WinError()


def move_cursor_smoothly(x: int, y: int, duration: float, steps: int) -> None:
    start_x, start_y = get_cursor_pos()

    if duration <= 0 or steps <= 1:
        set_cursor_pos(x, y)
        return

    delay = duration / steps
    for step in range(1, steps + 1):
        progress = step / steps
        eased = 0.5 - 0.5 * math.cos(math.pi * progress)
        next_x = round(start_x + (x - start_x) * eased)
        next_y = round(start_y + (y - start_y) * eased)
        set_cursor_pos(next_x, next_y)
        time.sleep(delay)


def parse_points(raw_points: str) -> list[tuple[int, int]]:
    try:
        loaded = json.loads(raw_points)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"JSON invalido: {exc}") from exc

    if not isinstance(loaded, list) or not loaded:
        raise argparse.ArgumentTypeError("Los puntos deben ser un array no vacio.")

    points = []
    for index, item in enumerate(loaded, start=1):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise argparse.ArgumentTypeError(
                f"El punto #{index} debe tener formato [x, y]."
            )

        x, y = item
        if not isinstance(x, int) or not isinstance(y, int):
            raise argparse.ArgumentTypeError(
                f"El punto #{index} debe usar coordenadas enteras."
            )

        points.append((x, y))

    return points


def validate_points(points: list[tuple[int, int]], screen_width: int, screen_height: int) -> bool:
    valid = True
    for index, (x, y) in enumerate(points, start=1):
        if not 0 <= x < screen_width or not 0 <= y < screen_height:
            print(
                f"Punto #{index} fuera de pantalla: ({x}, {y}). "
                f"Rango valido: x=0..{screen_width - 1}, y=0..{screen_height - 1}.",
                file=sys.stderr,
            )
            valid = False
    return valid


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Mueve el cursor real de Windows a coordenadas explicitas de pantalla. "
            "No hace clics ni queda corriendo en segundo plano."
        )
    )
    parser.add_argument("x", type=int, nargs="?", help="Coordenada X destino.")
    parser.add_argument("y", type=int, nargs="?", help="Coordenada Y destino.")
    parser.add_argument(
        "--points",
        type=parse_points,
        default=None,
        help='Array JSON de coordenadas, por ejemplo: "[[200,300],[800,400]]".',
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Numero de veces que se recorre la lista de coordenadas.",
    )
    parser.add_argument(
        "--pause",
        type=float,
        default=0.0,
        help="Pausa en segundos despues de llegar a cada coordenada.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="Duracion de cada movimiento en segundos. Por defecto mueve inmediatamente.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=60,
        help="Cantidad de pasos para movimientos con duracion.",
    )
    parser.add_argument(
        "--show-screen",
        action="store_true",
        help="Muestra el tamano de pantalla detectado y sale.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida coordenadas y muestra lo que haria, sin mover el cursor.",
    )
    return parser.parse_args()


def main() -> int:
    if sys.platform != "win32":
        print("Este script usa APIs de Windows y solo funciona en Windows.", file=sys.stderr)
        return 1

    args = parse_args()
    screen_width, screen_height = get_screen_size()

    if args.show_screen:
        print(f"Pantalla detectada: {screen_width}x{screen_height}")
        return 0

    if args.points is not None and (args.x is not None or args.y is not None):
        print("Usa --points o x/y, pero no ambos al mismo tiempo.", file=sys.stderr)
        return 1

    if args.points is None:
        if args.x is None or args.y is None:
            print("Debes proporcionar x/y, --points, o usar --show-screen.", file=sys.stderr)
            return 1
        points = [(args.x, args.y)]
    else:
        points = args.points

    if args.repeat <= 0:
        print("--repeat debe ser mayor que 0.", file=sys.stderr)
        return 1

    if args.duration < 0:
        print("--duration no puede ser negativo.", file=sys.stderr)
        return 1

    if args.pause < 0:
        print("--pause no puede ser negativo.", file=sys.stderr)
        return 1

    if args.steps <= 0:
        print("--steps debe ser mayor que 0.", file=sys.stderr)
        return 1

    if not validate_points(points, screen_width, screen_height):
        return 1

    current_x, current_y = get_cursor_pos()
    print(f"Cursor actual: ({current_x}, {current_y})")
    print(f"Puntos: {points}")
    print(f"Repeticiones: {args.repeat}")

    if args.dry_run:
        print("Dry run: no se movio el cursor.")
        return 0

    while True:
        x = random.randint(1, 1000)
        y = random.randint(1, 1000)
        move_cursor_smoothly(x, y, args.duration, args.steps)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
