from __future__ import annotations

from pathlib import Path

from src.rendering.template_renderer import (
    CONTENT_DIR,
    OUTPUT_DIR,
    LANGUAGE_CHOICES,
    get_field_order,
    get_template_path,
    render_template_image_with_overrides,
    split_paragraphs,
)


def choose_language() -> str:
    print("Available languages:", ", ".join(sorted(LANGUAGE_CHOICES)))
    raw = input("Language: ").strip().lower()
    if raw not in LANGUAGE_CHOICES:
        print("Unknown language, using de.")
        return "de"
    return raw


def choose_template_number() -> int:
    raw = input("Template number: ").strip()
    if not raw:
        return 1
    try:
        return int(raw)
    except ValueError:
        print("Invalid template number, using 1.")
        return 1


def choose_output_path(language: str, template_number: int) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    return OUTPUT_DIR / f"{language}_template{template_number}.png"


def read_paragraph_block(field_count: int) -> list[str]:
    print("Paste all text now.")
    print("Separate fields with one blank line.")
    print("Finish input by typing END on a new line.")

    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    paragraphs = split_paragraphs("\n".join(lines))
    while len(paragraphs) < field_count:
        paragraphs.append("")
    return paragraphs[:field_count]


def main() -> None:
    language = choose_language()
    template_number = choose_template_number()
    field_order = get_field_order(template_number)
    if not field_order:
        raise ValueError(f"Template {template_number} is not configured yet.")

    template_path = get_template_path(language, template_number)
    print(f"Using template: {template_path}")

    paragraphs = read_paragraph_block(len(field_order))
    values: dict[int, str] = {}
    for index, field_number in enumerate(field_order):
        values[field_number] = paragraphs[index]

    image = render_template_image_with_overrides(language, template_number, values)
    output_path = choose_output_path(language, template_number)
    image.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
