from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / "content"
ASSETS_DIR = ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"

LANGUAGE_CHOICES = {
    "de": "German",
    "en": "English",
    "ru": "Russian",
}

TEMPLATE_FIELD_ORDER = {
    1: tuple(range(1, 14)),
    2: tuple(range(1, 8)),
    3: tuple(range(1, 12)),
}


@dataclass(frozen=True)
class TextStyle:
    family: str
    size: int
    fill: tuple[int, int, int, int]
    wrap: bool = True
    line_spacing: int = 2
    tracking: float = 0.0
    align: str = "left"
    valign: str = "top"


@dataclass(frozen=True)
class FieldSpec:
    box: tuple[int, int, int, int]
    style: str
    prompt: str
    background_text: str | None = None
    background_fill: tuple[int, int, int, int] | None = None
    background_radius: int = 0
    background_padding: tuple[int, int] = (0, 0)


TEXT_STYLES = {
    "title": TextStyle("bold", 10, (35, 76, 142, 255), wrap=False, line_spacing=0, tracking=0.7),
    "body": TextStyle("regular", 10, (62, 62, 70, 255), wrap=True, line_spacing=0.2),
    "meta": TextStyle("medium", 9, (124, 128, 140, 255), wrap=False, line_spacing=0),
    "meta_alt": TextStyle("medium", 9, (124, 128, 140, 255), wrap=False, line_spacing=0, tracking=0.2),
    "value": TextStyle("bold", 14, (30, 30, 34, 255), wrap=False, line_spacing=0, tracking=0.2),
    "status": TextStyle("bold", 14, (239, 151, 41, 255), wrap=False, line_spacing=0, tracking=0),
    "paragraph": TextStyle("regular", 11, (58, 58, 66, 255), wrap=True, line_spacing=4),
    "section": TextStyle("bold", 11, (31, 31, 36, 255), wrap=False, line_spacing=0),
    "bullet": TextStyle("regular", 10, (53, 53, 60, 255), wrap=True, line_spacing=0),
    "footnote": TextStyle("regular", 10, (125, 112, 60, 255), wrap=True, line_spacing=1),
    "button_primary": TextStyle("bold", 11, (255, 255, 255, 255), wrap=False, line_spacing=0, tracking=0.2),
    "button_secondary": TextStyle("bold", 11, (49, 49, 57, 255), wrap=False, line_spacing=0, tracking=0.2),
    
    "code2": TextStyle("medium", 15, (151, 153, 162, 255), wrap=False, line_spacing=0,),
    "name": TextStyle("bold", 15, (12, 15, 22, 255), wrap=False, line_spacing=0, ),
    "segment": TextStyle("medium", 15, (54, 131, 121, 255), wrap=False, line_spacing=0, ),
    "status2": TextStyle("bold", 13, (46, 100, 68, 255), wrap=False, line_spacing=0, align="center", valign="middle"),
    "amount": TextStyle("bold", 15, (31, 31, 36, 255), wrap=False, line_spacing=0, ),
    "count": TextStyle("medium", 15, (116, 116, 124, 255), wrap=False, line_spacing=0, ),
    "percent": TextStyle("bold", 15, (14, 12, 25, 255), wrap=False, line_spacing=0,),

    "t3_label": TextStyle("bold", 9, (194, 160, 78, 255), wrap=False, line_spacing=0, tracking=1.0),
    "t3_title": TextStyle("bold", 21, (255, 255, 255, 255), wrap=True, line_spacing=1.5, tracking=0.1),
    "t3_body": TextStyle("regular", 10, (179, 188, 205, 255), wrap=True, line_spacing=1.5, tracking=0.2),
    "t3_card_label": TextStyle("medium", 9, (123, 128, 138, 255), wrap=False, line_spacing=0, tracking=0.5),
    "t3_card_value": TextStyle("bold", 17, (34, 34, 39, 255), wrap=False, line_spacing=0, tracking=0.7),
    "t3_card_sub": TextStyle("medium", 9, (123, 128, 138, 255), wrap=False, line_spacing=0, tracking=0.5),
    "t3_section": TextStyle("bold", 10, (36, 40, 46, 255), wrap=False, line_spacing=0, tracking=0.8),
    "t3_section_body": TextStyle("regular", 10, (62, 67, 75, 255), wrap=True, line_spacing=4),
    "t3_button": TextStyle("bold", 11, (28, 28, 32, 255), wrap=False, line_spacing=0),
    
}


STATUS_BADGE_STYLES = {
    "blue": {
        "fill": (214, 233, 255, 255),
        "text": (31, 104, 205, 255),
    },
    "yellow": {
        "fill": (255, 240, 199, 255),
        "text": (201, 142, 16, 255),
    },
    "red": {
        "fill": (255, 226, 223, 255),
        "text": (209, 69, 57, 255),
    },
    "green": {
        "fill": (218, 253, 231, 255),
        "text": (46, 100, 68, 255),
    },
}


TEMPLATE_LAYOUTS = {
    1: {
        1: FieldSpec((467, 123, 857, 136), "title", "1"),
        2: FieldSpec((467, 140, 855, 162), "body", "2"),
        3: FieldSpec((433, 213, 632, 223), "meta_alt", "3"),
        4: FieldSpec((433, 227, 663, 243), "value", "4"),
        5: FieldSpec((661, 213, 862, 223), "meta_alt", "5"),
        6: FieldSpec((661, 227, 862, 243), "status", "6"),
        7: FieldSpec((419, 277, 862, 370), "paragraph", "7"),
        8: FieldSpec((454, 399, 840, 413), "section", "8"),
        9: FieldSpec((452, 417, 855, 448), "bullet", "9"),
        10: FieldSpec((452, 446, 855, 478), "bullet", "10"),
        11: FieldSpec((433, 521, 854, 551), "footnote", "11"),
        12: FieldSpec((465, 596, 685, 607), "button_primary", "12"),
        13: FieldSpec((749, 596, 860, 608), "button_secondary", "13"),
    },
    2: {
        1: FieldSpec((40, 88, 149, 108), "code2", "1"),
        2: FieldSpec((211, 88, 404, 108), "name", "2"),
        3: FieldSpec((450, 88, 554, 108), "segment", "3"),
        4: FieldSpec(
            (572, 81, 707, 110),
            "status2",
            "4",
            background_text="Genehmigt",
            background_fill=STATUS_BADGE_STYLES["green"]["fill"],
            background_radius=15,
            background_padding=(14, 7),
        ),
        5: FieldSpec((774, 87, 910, 108), "amount", "5"),
        6: FieldSpec((934, 87, 968, 108), "count", "6"),
        7: FieldSpec((1159, 88, 1218, 108), "percent", "7"),
    },
    3: {
        1: FieldSpec((370, 129, 570, 141), "t3_label", "1"),
        2: FieldSpec((370, 149, 903, 198), "t3_title", "2"),
        3: FieldSpec((370, 213, 890, 241), "t3_body", "3"),
        4: FieldSpec((386, 307, 625, 320), "t3_card_label", "4"),
        5: FieldSpec((386, 322, 625, 353), "t3_card_value", "5"),
        6: FieldSpec((666, 307, 906, 316), "t3_card_label", "6"),
        7: FieldSpec((666, 322, 795, 378), "t3_card_value", "7"),
        8: FieldSpec((666, 347, 820, 393), "t3_card_sub", "8"),
        9: FieldSpec((392, 409, 903, 425), "t3_section", "9"),
        10: FieldSpec((392, 432, 895, 538), "t3_section_body", "10"),
        11: FieldSpec((850, 592, 909, 603), "t3_button", "11"),
    },
}


FONT_PATTERNS = {
    "bold": [
        "**/Inter*Bold*.ttf",
        "**/Inter*Black*.ttf",
        "**/Roboto*Bold*.ttf",
        "**/Roboto*Black*.ttf",
        "calibrib.ttf",
        "arialbd.ttf",
    ],
    "medium": [
        "**/Inter*SemiBold*.ttf",
        "**/Inter*Medium*.ttf",
        "**/Roboto*SemiBold*.ttf",
        "**/Roboto*Medium*.ttf",
        "SegoeUI-Semibold.ttf",
        "calibri.ttf",
    ],
    "regular": [
        "**/Inter*Regular*.ttf",
        "**/Inter*Light*.ttf",
        "**/Roboto*Regular*.ttf",
        "**/Roboto*Light*.ttf",
        "segoeui.ttf",
        "calibri.ttf",
        "arial.ttf",
    ],
}


def get_template_path(language: str, template_number: int) -> Path:
    return CONTENT_DIR / language / f"template{template_number}.png"


def get_field_order(template_number: int) -> tuple[int, ...]:
    return TEMPLATE_FIELD_ORDER.get(template_number, ())


def get_example_path(language: str, template_number: int) -> Path | None:
    base = CONTENT_DIR / language / f"template{template_number}_example"
    for suffix in (".png", ".jpg", ".jpeg", ".webp"):
        candidate = base.with_suffix(suffix)
        if candidate.exists():
            return candidate
    return None


def get_example_text_path(language: str, template_number: int) -> Path | None:
    candidate = CONTENT_DIR / language / f"template{template_number}_example.txt"
    return candidate if candidate.exists() else None


def read_example_text(language: str, template_number: int) -> str | None:
    path = get_example_text_path(language, template_number)
    if not path:
        return None
    return path.read_text(encoding="utf-8")


def font_candidates(style: str) -> list[Path]:
    patterns = FONT_PATTERNS[style]
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(sorted(FONTS_DIR.glob(pattern)))
        candidates.extend(sorted(FONTS_DIR.rglob(pattern)))
    system_font_dirs = [Path(r"C:\Windows\Fonts")]
    for system_dir in system_font_dirs:
        for pattern in patterns:
            candidates.extend(sorted(system_dir.glob(pattern)))
            candidates.extend(sorted(system_dir.rglob(pattern)))
    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
    return unique


def load_font(style: str, size: int) -> tuple[ImageFont.FreeTypeFont, Path]:
    for font_path in font_candidates(style):
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size), font_path
    raise FileNotFoundError(
        f"No font found for style '{style}'. Put a matching .ttf file in assets/fonts."
    )


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    if not text:
        return 0
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue

        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if text_width(draw, candidate, font) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return "\n".join(lines)


def measure_line_width(draw: ImageDraw.ImageDraw, line: str, font: ImageFont.FreeTypeFont, tracking: float) -> float:
    if not line:
        return 0
    width = 0.0
    for index, char in enumerate(line):
        char_bbox = draw.textbbox((0, 0), char, font=font)
        width += char_bbox[2] - char_bbox[0]
        if index < len(line) - 1:
            width += tracking
    return width


def measure_multiline(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    spacing: int,
    tracking: float,
) -> tuple[int, int]:
    if not text:
        return 0, 0
    lines = text.splitlines() or [text]
    widths = [measure_line_width(draw, line, font, tracking) for line in lines]
    ascent, descent = font.getmetrics()
    line_height = ascent + descent
    height = len(lines) * line_height + max(0, len(lines) - 1) * spacing
    return (max(widths) if widths else 0), height


def draw_tracked_text(
    draw: ImageDraw.ImageDraw,
    position: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    line_spacing: int,
    tracking: float,
) -> None:
    x0, y0 = position
    ascent, descent = font.getmetrics()
    line_height = ascent + descent
    for line_index, line in enumerate(text.splitlines() or [""]):
        x = x0
        y = y0 + line_index * (line_height + line_spacing)
        for char_index, char in enumerate(line):
            draw.text((x, y), char, font=font, fill=fill)
            char_bbox = draw.textbbox((0, 0), char, font=font)
            x += (char_bbox[2] - char_bbox[0]) + (tracking if char_index < len(line) - 1 else 0)


def draw_text_in_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    style: TextStyle,
) -> None:
    x1, y1, x2, y2 = box
    max_width = x2 - x1
    max_height = y2 - y1
    font, resolved_text, _ = resolve_text(draw, text, style, max_width, max_height)
    lines = resolved_text.splitlines() if resolved_text else [""]
    text_w = max((measure_line_width(draw, line, font, style.tracking) for line in lines), default=0)
    ascent, descent = font.getmetrics()
    text_h = len(lines) * (ascent + descent) + max(0, len(lines) - 1) * style.line_spacing

    if style.align == "center":
        x = x1 + (max_width - text_w) / 2
    elif style.align == "right":
        x = x2 - text_w
    else:
        x = x1

    if style.valign == "middle":
        y = y1 + (max_height - text_h) / 2
    elif style.valign == "bottom":
        y = y2 - text_h
    else:
        y = y1

    draw_tracked_text(draw, (x, y), resolved_text, font, style.fill, style.line_spacing, style.tracking)


def draw_field(
    draw: ImageDraw.ImageDraw,
    spec: FieldSpec,
    text: str,
    style: TextStyle,
    background_fill: tuple[int, int, int, int] | None = None,
) -> None:
    actual_background = background_fill if background_fill is not None else spec.background_fill
    if actual_background is None:
        draw_text_in_box(draw, spec.box, text, style)
        return

    x1, y1, x2, y2 = spec.box
    max_width = x2 - x1
    max_height = y2 - y1
    pad_x, pad_y = spec.background_padding

    def draw_badge(badge_text: str, text_fill: tuple[int, int, int, int]) -> None:
        font, resolved_text, _ = resolve_text(draw, badge_text, style, max_width, max_height)
        lines = resolved_text.splitlines() if resolved_text else [""]
        text_w = max((measure_line_width(draw, line, font, style.tracking) for line in lines), default=0)
        ascent, descent = font.getmetrics()
        text_h = len(lines) * (ascent + descent) + max(0, len(lines) - 1) * style.line_spacing

        pill_w = text_w + pad_x * 2
        pill_h = text_h + pad_y * 2
        pill_x = x1 + max(0, (max_width - pill_w) / 2)
        pill_y = y1 + max(0, (max_height - pill_h) / 2)

        draw.rounded_rectangle(
            (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
            radius=spec.background_radius,
            fill=actual_background,
        )

        text_x = pill_x + (pill_w - text_w) / 2
        text_y = pill_y + (pill_h - text_h) / 2
        draw_tracked_text(draw, (text_x, text_y), resolved_text, font, text_fill, style.line_spacing, style.tracking)

    reference_text = spec.background_text if spec.background_text is not None else text
    if spec.background_text is not None:
        draw_badge(reference_text, actual_background)
    draw_badge(text, style.fill)


def resolve_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    style: TextStyle,
    max_width: int,
    max_height: int,
) -> tuple[ImageFont.FreeTypeFont, str, Path]:
    font, font_path = load_font(style.family, style.size)
    wrapped = wrap_text(draw, text, font, max_width) if style.wrap else text
    return font, wrapped, font_path


def split_paragraphs(text: str) -> list[str]:
    lines = text.splitlines()
    paragraphs: list[str] = []
    current: list[str] = []

    for line in lines:
        if line.strip() == "":
            if current:
                paragraphs.append("\n".join(current).strip())
                current = []
            continue
        current.append(line)

    if current:
        paragraphs.append("\n".join(current).strip())

    return paragraphs


def render_template_image(language: str, template_number: int, values: dict[int, str]) -> Image.Image:
    return render_template_image_with_overrides(language, template_number, values)


def render_template_image_with_overrides(
    language: str,
    template_number: int,
    values: dict[int, str],
    fill_overrides: dict[int, tuple[int, int, int, int]] | None = None,
    background_overrides: dict[int, tuple[int, int, int, int]] | None = None,
) -> Image.Image:
    template_path = get_template_path(language, template_number)
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    layout = TEMPLATE_LAYOUTS[template_number]
    for field_number in get_field_order(template_number):
        spec = layout[field_number]
        style = TEXT_STYLES[spec.style]
        if fill_overrides and field_number in fill_overrides:
            style = TextStyle(
                style.family,
                style.size,
                fill_overrides[field_number],
                wrap=style.wrap,
                line_spacing=style.line_spacing,
                tracking=style.tracking,
                align=style.align,
                valign=style.valign,
            )
        background_fill = background_overrides.get(field_number) if background_overrides else None
        draw_field(draw, spec, values.get(field_number, ""), style, background_fill=background_fill)

    return image
