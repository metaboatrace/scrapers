from datetime import date

from bs4 import BeautifulSoup, Tag
from metaboatrace.models.stadium import StadiumTelCode

from metaboatrace.scrapers.official.website.exceptions import ScrapingError


def format_stadium_tel_code_for_query_string(stadium_tel_code: StadiumTelCode) -> str:
    return str(stadium_tel_code.value).zfill(2)


def format_date_for_query_string(date: date) -> str:
    return date.strftime("%Y%m%d")


def select_one_or_raise(soup: BeautifulSoup | Tag, selector: str) -> Tag:
    """CSS セレクタで要素を1つ取得する。見つからなければ ``ScrapingError`` を送出する。

    ``BeautifulSoup.select_one`` は要素が見つからないと ``None`` を返すが、本スクレイパは
    「想定した HTML 構造が存在しなければ例外」という方針なので、必須要素の取得をこの
    ヘルパに集約することで ``Tag | None`` の None チェックを一本化し、型安全にする。
    """
    element = soup.select_one(selector)
    if element is None:
        raise ScrapingError(f"required element not found for selector: {selector!r}")
    return element


def get_attribute_or_raise(tag: Tag, name: str) -> str:
    """Tag の単一値属性を文字列として取得する。属性が無い / 複数値の場合は ``ScrapingError``。

    ``Tag.__getitem__`` / ``Tag.get`` は ``href`` のような単一値属性でも ``class`` のような
    複数値属性と同じく ``str | list[str]`` 型を返すため、``str`` を要求する箇所（``re`` や
    ``urlparse`` など）へ渡す際の型を一本化する。
    """
    value = tag.get(name)
    if not isinstance(value, str):
        raise ScrapingError(f"required string attribute not found: {name!r}")
    return value


def get_optional_attribute(tag: Tag, name: str) -> str | None:
    """Tag の単一値属性を取得する。属性が無ければ ``None``、複数値なら ``ScrapingError``。

    ``colspan`` のように「存在しないこと」が正常系として意味を持つ属性を、複数値属性と
    同じ ``str | list[str]`` 型から ``str | None`` に正規化する。
    """
    value = tag.get(name)
    if value is None or isinstance(value, str):
        return value
    raise ScrapingError(f"attribute is not single-valued: {name!r}")
