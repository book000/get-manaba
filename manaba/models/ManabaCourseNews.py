"""
manaba コースニュース
"""

import datetime
from typing import Optional

from manaba.models.ManabaModel import ManabaModel


class ManabaCourseNews(ManabaModel):
    """
    manaba コースニュース
    """

    def __init__(self,
                 course_id: int,
                 news_id: int,
                 title: str,
                 author: str,
                 posted_at: Optional[datetime.datetime],
                 last_edited_author: Optional[str],
                 last_edited_at: Optional[datetime.datetime],
                 text: Optional[str],
                 html: Optional[str]):
        """
        manaba コースニュース

        Args:
            course_id: コース ID
            news_id: ニュース ID
            title: ニュースタイトル
            author: 投稿者
            posted_at: 投稿日時
            last_edited_author: 最終更新者
            last_edited_at: 最終更新日時
            text: ニューステキスト
            html: ニュース HTML
        """
        self._course_id = course_id
        self._news_id = news_id
        self._title = title
        self._author = author
        self._posted_at = posted_at
        self._last_edited_author = last_edited_author
        self._last_edited_at = last_edited_at
        self._text = text
        self._html = html

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
    def news_id(self) -> int:
        """
        ニュース ID (URLの一部)

        Returns:
            int: ニュース ID
        """
        return self._news_id

    @property
    def title(self) -> str:
        """
        ニュースタイトル

        Returns:
            str: ニュースタイトル
        """
        return self._title

    @property
    def author(self) -> str:
        """
        投稿者名

        Returns:
            str: 投稿者名
        """
        return self._author

    @property
    def posted_at(self) -> Optional[datetime.datetime]:
        """
        投稿時刻

        Returns:
            Optional[datetime.datetime]: 投稿時刻
        """
        return self._posted_at

    @property
    def last_edited_author(self) -> Optional[str]:
        """
        最終更新者

        Returns:
            Optional[str]: 最終更新者
        """
        return self._last_edited_author

    @property
    def last_edited_at(self) -> Optional[datetime.datetime]:
        """
        最終更新日時

        Returns:
            Optional[datetime.datetime]: 最終更新日時
        """
        return self._last_edited_at

    @property
    def text(self) -> Optional[str]:
        """
        コメントのテキスト

        Returns:
            Optional[str]: コメントのプレーンテキスト

        Notes:
            投稿者によって設定された太字や文字色等はこの項目では取得できません。ManabaNews.html を使用してください。
        """
        return self._text

    @property
    def html(self) -> Optional[str]:
        """
        コメントの HTML

        Returns:
            Optional[str]: コメントの HTML
        """
        return self._html
