import typer

app = typer.Typer(help="ISO 8583 message toolkit.", no_args_is_help=True)


def _todo(name: str):
    typer.echo(f"{name}: not implemented yet", err=True)
    raise typer.Exit(2)


@app.command()
def decode(hex_message: str, spec: str = typer.Option(None, help="Spec JSON file")):
    """Decode a hex message into fields."""
    _todo("decode")


@app.command()
def encode(json_file: str, spec: str = typer.Option(None, help="Spec JSON file")):
    """Encode JSON fields into a hex message."""
    _todo("encode")


@app.command()
def validate(hex_message: str, spec: str = typer.Option(None, help="Spec JSON file")):
    """Validate a hex message against the spec."""
    _todo("validate")
