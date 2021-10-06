"""
manaba コンテンツ
"""
import datetime
from typing import Optional

from manaba.models.ManabaContentPage import ManabaContentPage
from manaba.models.ManabaModel import ManabaModel


class ManabaContent(ManabaModel):
    """
    manaba コンテンツ
    """

    def __init__(self,
                 course_id: int,
                 content_id: str,
                 title: str,
                 description: str,
                 updated_at: Optional[datetime.datetime],
                 pages: Optional[list[ManabaContentPage]]):
        """
        manaba コンテンツ

        Args:
            course_id: コース ID
            content_id: コンテンツ ID
            title: コンテンツタイトル
            description: コンテンツ説明
            updated_at: 更新日時
            pages: コンテンツ内ページ
        """
        self._course_id = course_id
        self._content_id = content_id
        self._title = title
        self._description = description
        self._updated_at = updated_at
        self._pages = pages

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
    def title(self) -> str:
        """
        コンテンツタイトル

        Returns:
            str: コンテンツタイトル
        """
        return self._title

    @property
    def description(self) -> str:
        """
        説明文

        Returns:
            str: 説明文
        """
        return self._description

    @property
    def updated_at(self) -> Optional[datetime.datetime]:
        """
        更新日時

        Returns:
            Optional[datetime.datetime]: 更新日時
        """
        return self._updated_at

    @property
    def pages(self) -> Optional[list[ManabaContentPage]]:
        """
        コンテンツ内のページ

        Returns:
            Optional[list[ManabaContentPage]]: コンテンツ内のページ
        """
        return self._pages

    def __str__(self) -> str:
        return "ManabaContent{course_id=%s,content_id=%s,title=%s}" % (self._course_id, self._content_id, self._title)
