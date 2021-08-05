"""
manaba コンテンツ
"""

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
                 title: Optional[str],
                 description: Optional[str],
                 updated_at: Optional[str],
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
