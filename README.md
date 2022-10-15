## 概要

[ボートレース公式サイト](https://boatrace.jp/) のユーティリティパッケージ

以下の機能を備える

- URLの生成
- スクレイピング

## 使用例

### URLの生成

#### レースの出走表ページのURLを生成する

```python
>>> from datetime import date
>>> from boatrace.models import StadiumTelCode
>>> from boatrace.official.v1707.pages.race.entry_page.location import create_race_entry_page_url
>>> create_race_entry_page_url(race_holding_date=date(2022, 9, 19), stadium_tel_code=StadiumTelCode.HEIWAJIMA, race_number=12)
'https://boatrace.jp/owpc/pc/race/racelist?rno=12&jcd=04&hd=20220919'
```

前検情報やオッズなど別種のページのURL構造も location というモジュールで持っていて、使い方は各種ユニットテストを参照

```bash
$ find boatrace/official/v1707 -name 'test_location*py' -type f
boatrace/official/v1707/pages/monthly_schedule_page/tests/test_location.py
boatrace/official/v1707/pages/pre_inspection_information_page/tests/test_location.py
boatrace/official/v1707/pages/race/before_information_page/tests/test_location.py
boatrace/official/v1707/pages/race/odds/trifecta_page/tests/test_location.py
boatrace/official/v1707/pages/race/result_page/tests/test_location.py
boatrace/official/v1707/pages/race/entry_page/tests/test_location.py
boatrace/official/v1707/pages/racer/profile_page/tests/test_location.py
```

### スクレイピング

#### レース出走表をスクレイピングする

以下は取得の一例

https://github.com/BoatraceRepository/boatrace.official/blob/f0c4260d3fbbc781cd198acba647d41d6a6e4bc2/boatrace/official/v1707/pages/race/entry_page/tests/test_scraping.py#L19-L35

インターフェースの詳細は各種ユニットテスト参照

```bash
$ find boatrace/official/v1707 -name 'test_scraping*py' -type f
```
