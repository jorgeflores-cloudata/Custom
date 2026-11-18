import argparse
import ctypes
import sys
import time
from datetime import datetime, timedelta


ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002


def set_execution_state(flags: int) -> None:
    result = ctypes.windll.kernel32.SetThreadExecutionState(flags)
    if result == 0:
        raise ctypes.WinError()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Mantiene Windows despierto mientras el script esta en ejecucion, "
            "sin mover el mouse ni simular entrada de usuario."
        )
    )
    parser.add_argument(
        "--minutes",
        type=float,
        default=None,
        help="Cantidad de minutos a mantener despierto el equipo. Si se omite, corre hasta Ctrl+C.",
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="Tambien solicita mantener la pantalla encendida.",
    )
    parser.add_argument(
        "--heartbeat",
        type=int,
        default=60,
        help="Cada cuantos segundos mostrar un mensaje de estado. Usa 0 para silenciar.",
    )
    return parser.parse_args()


def main() -> int:
    if sys.platform != "win32":
        print("Este script usa una API de Windows y solo funciona en Windows.", file=sys.stderr)
        return 1

    args = parse_args()
    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    if args.display:
        flags |= ES_DISPLAY_REQUIRED

    end_at = None
    if args.minutes is not None:
        if args.minutes <= 0:
            print("--minutes debe ser mayor que 0.", file=sys.stderr)
            return 1
        end_at = datetime.now() + timedelta(minutes=args.minutes)

    set_execution_state(flags)
    print("Equipo mantenido despierto. Presiona Ctrl+C para detener.")
    if end_at:
        print(f"Finaliza aproximadamente a las {end_at:%H:%M:%S}.")

    try:
        while True:
            if end_at and datetime.now() >= end_at:
                break

            sleep_for = 1
            if args.heartbeat > 0:
                seconds_left = args.heartbeat
                if end_at:
                    seconds_until_end = max(0, int((end_at - datetime.now()).total_seconds()))
                    seconds_left = min(seconds_left, seconds_until_end or 1)
                sleep_for = seconds_left

            time.sleep(sleep_for)

            if args.heartbeat > 0:
                now = datetime.now()
                if end_at:
                    remaining = max(0, int((end_at - now).total_seconds()))
                    print(f"{now:%H:%M:%S} - activo, quedan {remaining // 60}m {remaining % 60}s")
                else:
                    print(f"{now:%H:%M:%S} - activo")
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    finally:
        set_execution_state(ES_CONTINUOUS)
        print("Permisos de suspension restaurados.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
