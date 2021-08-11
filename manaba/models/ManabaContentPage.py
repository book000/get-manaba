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
                 title: str,
                 author: Optional[str],
                 version: Optional[float],
                 last_edited_at: Optional[datetime.datetime],
                 publish_start_at: Optional[datetime.datetime],
                 publish_end_at: Optional[datetime.datetime],
                 text: Optional[str],
                 html: Optional[str],
                 files: Optional[list[ManabaFile]]):
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

    @property
    def course_id(self) -> int:
        """
        コース ID (URLの一部)
        ※コースコードではない

        Returns:
            int: コース ID
        """
        return self._course_id

    @property
    def content_id(self) -> str:
        """
        コンテンツ ID (URLの一部)

        Returns:
            str: コンテンツ ID
        """
        return self._content_id

    @property
    def page_id(self) -> int:
        """
        ページ ID (URLの一部)

        Returns:
            str: ページ ID
        """
        return self._page_id

    @property
    def title(self) -> str:
        """
        コンテンツページタイトル

        Returns:
            str: コンテンツページタイトル
        """
        return self._title

    @property
    def author(self) -> Optional[str]:
        """
        ページの作成者

        Returns:
            str: ページ作成者

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
        """
        return self._author

    @property
    def version(self) -> Optional[float]:
        """
        ページバージョン（版）

        Returns:
            Optional[float]: ページバージョン（版）

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
        """
        return self._version

    @property
    def last_edited_at(self) -> Optional[datetime.datetime]:
        """
        最終更新日時

        Returns:
            Optional[datetime.datetime]: 最終更新日時

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
        """
        return self._last_edited_at

    @property
    def publish_start_at(self) -> Optional[datetime.datetime]:
        """
        公開期間開始日時

        Returns:
            Optional[datetime.datetime]: 公開期間開始日時

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
        """
        return self._publish_start_at

    @property
    def publish_end_at(self) -> Optional[datetime.datetime]:
        """
        公開期間終了日時

        Returns:
            Optional[datetime.datetime]: 公開期間終了日時

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
        """
        return self._publish_end_at

    @property
    def text(self) -> Optional[str]:
        """
        ページのテキスト

        Returns:
            Optional[str]: ページのテキスト

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
            作成者によって設定された太字や文字色等はこの項目では取得できません。ManabaContentPage.html を使用してください。
        """
        return self._text

    @property
    def html(self) -> Optional[str]:
        """
        ページの HTML

        Returns:
            Optional[str]: ページの HTML

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
        """
        return self._html

    @property
    def files(self) -> Optional[list[ManabaFile]]:
        """
        ページに添付されているファイルの一覧

        Returns:
            Optional[list[ManabaFile]: ページに添付されているファイルの一覧

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
        """
        return self._files
