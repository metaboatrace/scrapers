import re
import urllib.parse
from datetime import date

from bs4 import BeautifulSoup, Tag
from metaboatrace.models.stadium import StadiumTelCode

from metaboatrace.scrapers.official.website.exceptions import ScrapingError
from metaboatrace.scrapers.official.website.v1707 import BASE_URL


def format_stadium_tel_code_for_query_string(stadium_tel_code: StadiumTelCode) -> str:
    return str(stadium_tel_code.value).zfill(2)


def format_date_for_query_string(date: date) -> str:
    return date.strftime("%Y%m%d")


def build_race_page_url(
    path: str, race_holding_date: date, stadium_tel_code: StadiumTelCode, race_number: int
) -> str:
    """レース単位のページ (出走表・直前情報・オッズ・結果) の URL を組み立てる。

    これらのページは ``/owpc/pc/race/<path>`` 配下にあり、クエリ文字列の規約
    (``rno`` = レース番号, ``jcd`` = 2 桁ゼロ埋めの電話投票コード, ``hd`` = YYYYMMDD)
    を共有する。
    """
    query = urllib.parse.urlencode(
        {
            "rno": race_number,
            "jcd": format_stadium_tel_code_for_query_string(stadium_tel_code),
            "hd": format_date_for_query_string(race_holding_date),
        }
    )
    return f"{BASE_URL}/owpc/pc/race/{path}?{query}"


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


def split_racer_name(full_name: str) -> tuple[str, str]:
    """公式サイト表記のレーサー氏名を (姓, 名) に分割する。

    姓と名は全角 / 半角スペースで区切られるが、公式サイトは姓+名が長いと表示幅都合で
    区切りを落とすことがある (例: toban=4011 堀之内紀代子)。仮名側からの正確な漢字分割は
    復元不能なので、区切りが無い場合は姓に全体を入れて名は空文字にする。
    出走表・プロフィール・前検情報の各ページで同じ規則を使う。
    """
    name_parts = re.split(r"[\s　]+", full_name.strip(), maxsplit=1)
    last_name = name_parts[0]
    first_name = name_parts[1] if len(name_parts) > 1 else ""
    return last_name, first_name
