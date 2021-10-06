"""
manaba スレッド
"""

from typing import Optional

from manaba.models.ManabaModel import ManabaModel
from manaba.models.ManabaThreadComment import ManabaThreadComment


class ManabaThread(ManabaModel):
    """
    manaba スレッド
    """

    def __init__(self,
                 course_id: int,
                 thread_id: int,
                 title: Optional[str],
                 comments: Optional[list[ManabaThreadComment]]):
        """
        manaba スレッド

        Args:
            course_id: コース ID
            thread_id: スレッド ID
            title: スレッドタイトル (1件目のコメントタイトルと同じ)
            comments: コメント一覧
        """
        self._course_id = course_id
        self._thread_id = thread_id
        self._title = title
        self._comments = comments

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
    def thread_id(self) -> int:
        """
        スレッド ID (URLの一部)

        Returns:
            int: スレッド ID
        """
        return self._thread_id

    @property
    def title(self) -> Optional[str]:
        """
        スレッドタイトル (1件目のコメントタイトルと同じ)

        Returns:
            str: スレッドタイトル
        """
        return self._title

    @property
    def comments(self) -> Optional[list[ManabaThreadComment]]:
        """
        コメント一覧

        Returns:
            Optional[list[ManabaThreadComment]]: コメント一覧

        Notes:
            この項目は、Manaba.get_threads で取得した場合必ず None になります。
            取得するには、 Manaba.get_thread メソッドを使用してください。
        """
        return self._comments

    def __str__(self) -> str:
        return "ManabaThread{course_id=%s,thread_id=%s,title=%s,comments=%s}" % (
            self._course_id, self._thread_id, self._title, self._comments)
