def formato_anotacao(label: str, x: int, y: int) -> dict:
    """Formata os dados de anotação para persistência."""
    if not label:
        raise ValueError("A label não pode ser vazia.")
    return {"label": label, "coordinates": {"x": x, "y": y}}