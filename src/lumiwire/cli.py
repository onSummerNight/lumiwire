from importlib import resources

import typer

from .decode import DecodeError, decode as decode_message
from .mask import mask
from .spec import SpecError, load_spec

DEFAULT_SPEC = resources.files("lumiwire") / "specs" / "iso8583_1987.json"

app = typer.Typer(help="ISO 8583 message toolkit.", no_args_is_help=True)


def _todo(name: str):
    typer.echo(f"{name}: not implemented yet", err=True)
    raise typer.Exit(2)


@app.command()
def decode(
    hex_message: str,
    spec: str = typer.Option(None, help="Spec JSON file"),
    unmask: bool = typer.Option(False, "--unmask", help="Show PAN and track data in full"),
):
    """Decode a hex message into fields."""
    try:
        loaded = load_spec(spec or DEFAULT_SPEC)
        result = decode_message(hex_message, loaded)
    except (DecodeError, SpecError) as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(1)
    if not unmask:
        result = mask(result, loaded)
    typer.echo(f"MTI {result['mti']}")
    for num, value in result["fields"].items():
        typer.echo(f"{num:03d} {loaded.fields[num].name}: {value}")


@app.command()
def encode(json_file: str, spec: str = typer.Option(None, help="Spec JSON file")):
    """Encode JSON fields into a hex message."""
    _todo("encode")


@app.command()
def validate(hex_message: str, spec: str = typer.Option(None, help="Spec JSON file")):
    """Validate a hex message against the spec."""
    _todo("validate")
