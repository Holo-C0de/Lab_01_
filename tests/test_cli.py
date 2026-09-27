import subprocess
import sys


def run_cli(*args):
    """Запускает py -m toolkit с переданными аргументами."""
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_help():
    result = run_cli("--help")
    assert result.returncode == 0


def test_cli_calc_success():
    result = run_cli("calc", "2+3*4")
    assert result.returncode == 0
    assert result.stdout.strip() == "14"


def test_cli_calc_error():
    result = run_cli("calc", "1/0")
    assert result.returncode == 2
    assert "Деление на ноль" in result.stderr


def test_cli_convert_success():
    result = run_cli("convert", "1000", "--from", "mm", "--to", "m")
    assert result.returncode == 0
    assert result.stdout.strip() == "1.0"


def test_cli_convert_incompatible():
    result = run_cli("convert", "1", "--from", "kg", "--to", "m")
    assert result.returncode == 2
    assert "Несовместимые единицы" in result.stderr
