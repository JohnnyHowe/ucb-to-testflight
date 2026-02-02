from pathlib import Path
from typing import Type


REGULAR=None
WARNING="#f1c40f"
ERROR="#e06c75"
SUCCESS="#98c379"
TODO="#4F37D7"


def raise_pretty_exception(error: Type[Exception], message: str) -> None:
    pretty_print(message, color=ERROR)
    raise error(message)


def pretty_print(*args, color=None, **kwargs) -> None:
    text = " ".join(str(a) for a in args)  # join everything manually
    if not color:
        print(text, **kwargs)
        return

    color = color.lstrip("#")
    r, g, b = (int(color[i:i+2], 16) for i in (0, 2, 4))
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", **kwargs)


def get_pretty_path_string(path: Path) -> str:
    return f"{path} ({path.absolute()})"