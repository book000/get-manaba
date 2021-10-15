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
                 version: Optional[str],
                 viewable: Optional[bool],
                 last_edited_at: Optional[datetime.datetime],
                 publish_start_at: Optional[datetime.datetime],
                 publish_end_at: Optional[datetime.datetime],
                 html: Optional[str]):
        """
        manaba コンテンツページ

        Args:
            course_id: コース ID
            content_id: コンテンツ ID
            page_id: コンテンツページ ID
            title: ページタイトル
            author: 作成・更新者
            version: バージョン
            viewable: 閲覧可能か
            last_edited_at: 最終更新日時
            publish_start_at: 公開期間開始日時
            publish_end_at: 公開期間終了日時
            html: ページ HTML
        """
        self._course_id = course_id
        self._content_id = content_id
        self._page_id = page_id
        self._title = title
        self._author = author
        self._version = version
        self._viewable = viewable
        self._last_edited_at = last_edited_at
        self._publish_start_at = publish_start_at
        self._publish_end_at = publish_end_at
        self._html = html
        self._files: list[ManabaFile] = []

    def add_file(self,
                 file: ManabaFile) -> None:
        """
        添付ファイルを追加する

        Args:
            file: ManabaFile オブジェクト
        """
        self._files.append(file)

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
    def version(self) -> Optional[str]:
        """
        ページバージョン（版）

        Returns:
            Optional[str]: ページバージョン（版）

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
        """
        return self._version

    @property
    def viewable(self) -> Optional[bool]:
        """
        閲覧可能か

        Returns:
            Optional[bool]: 閲覧可能か

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。
        """
        return self._viewable

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
    def html(self) -> Optional[str]:
        """
        ページの HTML

        Returns:
            Optional[str]: ページの HTML

        Notes:
            Manaba.get_content_pages で取得した場合、この項目は None になります。Manaba.get_content_page でページ詳細情報を取得してください。

            viewable が false の場合、この項目は None になります。
        """
        return self._html

    @property
    def files(self) -> list[ManabaFile]:
        """
        ページに添付されているファイルの一覧

        Returns:
            list[ManabaFile]: ページに添付されているファイルの一覧

        Notes:
            この項目は、取得できない もしくは 存在しなかった としても空のリストになります。
        """
        return self._files

    def __str__(self) -> str:
        return "ManabaContentPage{course_id=%s,content_id=%s,page_id=%s,title=%s,author=%s,version=%s}" % (
            self._course_id, self._content_id, self._page_id, self._title, self._author, self._version)
