"""
manaba コンテンツページ
"""
import datetime
from typing import Optional

from manaba.models.ManabaFile import ManabaFile
from manaba.models.ManabaModel import ManabaModel


class ManabaContentPage(ManabaModel):
    """
    manaba コンテンツページ
    """

    def __init__(self,
                 course_id: int,
                 content_id: str,
                 page_id: int,
                 title: Optional[str],
                 author: str,
                 version: float,
                 last_edited_at: datetime.datetime,
                 publish_start_at: datetime.datetime,
                 publish_end_at: Optional[datetime.datetime],
                 text: Optional[str],
                 html: Optional[str],
                 files: list[ManabaFile]):
        """
        manaba コンテンツページ

        Args:
            course_id: コース ID
            content_id: コンテンツ ID
            page_id: コンテンツページ ID
            title: ページタイトル
            author: 作成・更新者
            version: バージョン
            last_edited_at: 最終更新日時
            publish_start_at: 公開期間開始日時
            publish_end_at: 公開期間終了日時
            text: ページテキスト
            html: ページ HTML
            files: 添付ファイル
        """
        self._course_id = course_id
        self._content_id = content_id
        self._page_id = page_id
        self._title = title
        self._author = author
        self._version = version
        self._last_edited_at = last_edited_at
        self._publish_start_at = publish_start_at
        self._publish_end_at = publish_end_at
        self._text = text
        self._html = html
        self._files = files
