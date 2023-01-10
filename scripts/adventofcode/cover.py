import logging
from argparse import ArgumentParser
from pathlib import Path

import cssutils
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from PIL import Image, ImageDraw, ImageFont

BACKGROUND_COLOR = "#0f0f23"


def calendar_styles(soup: BeautifulSoup) -> dict[str, str]:
    styles = {}
    sheet = cssutils.parseString(soup.string)
    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            selectors = rule.selectorText.split()
            if ".calendar" in selectors:
                selectors.remove(".calendar")
                key = next(iter(selectors))
                value = rule.style.getPropertyValue("color")
                if key and value:
                    styles[key[1:]] = value
    styles["calendar-mark-complete"] = styles["calendar-mark-verycomplete"] = "#ffff66"
    return styles


def generate(year: int, session_cookie: str, font_path: Path) -> Image:
    response = requests.get(
        f"https://adventofcode.com/{year}", cookies={"session": session_cookie}
    )
    soup = BeautifulSoup(response.content, features="html.parser")
    styles = calendar_styles(soup.find("style"))

    # generate ascii art image
    font = ImageFont.truetype(str(font_path), size=30)
    sizes: list[tuple[int, ...]] = []
    for a in soup.find("pre", class_="calendar").find_all("a"):
        for line in a.text.splitlines():
            sizes.append(font.getbbox(line))
    w = max(map(lambda x: x[2], sizes))
    h = max(map(lambda x: x[3], sizes))
    padding = 8
    image = Image.new(
        "RGB", (w + padding * 2, h * len(sizes) + padding * 2), BACKGROUND_COLOR
    )
    draw = ImageDraw.Draw(image)
    x, y = (padding, padding)
    for a in soup.find("pre", class_="calendar").find_all("a"):
        for child in a.children:
            text = child.text
            color = "#ffffff"
            if isinstance(child, Tag):
                if c := styles.get(child["class"][0]):
                    color = c
            draw.text((x, y), text, font=font, fill=color)
            if text.endswith("\n"):
                x, y = padding, y + h
            else:
                x += draw.textlength(text, font=font)
        x, y = padding, y + h

    w, h = image.size
    scale = w / 500.0
    resized = image.resize((round(w / scale), round(h / scale)), resample=Image.LANCZOS)

    # generate title part
    title = Image.new("RGB", (500, 700 - resized.height), BACKGROUND_COLOR)
    title_font = ImageFont.truetype(str(font_path), size=50)
    title_draw = ImageDraw.Draw(title)
    bboxes = [title_font.getbbox("Advent of Code"), title_font.getbbox(f"{year}")]
    title_draw.text(
        ((500 - bboxes[0][2]) / 2, (title.height / 2 - bboxes[0][3]) / 2),
        "Advent of Code",
        font=title_font,
        fill="#00cc00",
    )
    title_draw.text(
        ((500 - bboxes[1][2]) / 2, (title.height * 1.2 - sizes[1][3]) / 2),
        f"{year}",
        font=title_font,
        fill="#00cc00",
    )

    # generate cover image
    cover = Image.new("RGB", (500, 700), "#0f0f23")
    cover.paste(title, (0, 0))
    cover.paste(resized, (0, title.height))
    return cover


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("--out", type=Path, default=Path("cover.png"))
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--session-cookie", type=str, required=True)
    args = parser.parse_args()

    cssutils.log.setLevel(logging.CRITICAL)
    image = generate(args.year, args.session_cookie, args.font)
    image.save(args.out)
