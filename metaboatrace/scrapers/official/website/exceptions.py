class ScrapingError(Exception):
    pass


class DataNotFound(Exception):
    pass


class RaceCanceled(Exception):
    pass


class DataNotReady(ScrapingError):
    """ページは公開済みだが、速報段階でデータがまだ確定していない状態.

    公式サイトはレース直前・直後にページを先行公開し、払戻金や水面気象などの
    一部の値を「確定前（空欄 / プレースホルダ）」のまま返すことがある。取得の
    タイミングが早すぎただけで、時間を置けば確定するので、呼び出し側は後追い
    （リトライ / 日次 sweep）で取り直せばよい。

    恒久的にデータが存在しない ``DataNotFound`` や、レース中止 ``RaceCanceled``
    とは原因も対処も異なるため、別の例外型として区別する。
    """

    pass
