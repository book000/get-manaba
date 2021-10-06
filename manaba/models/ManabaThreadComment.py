"""
manaba スレッドコメント
"""

import datetime
from typing import Optional

from manaba import ManabaFile
from manaba.models.ManabaModel import ManabaModel


class ManabaThreadComment(ManabaModel):
    """
    manaba スレッドコメント
    """

    def __init__(self,
                 course_id: int,
                 thread_id: int,
                 comment_id: int,
                 title: Optional[str],
                 author: Optional[str],
                 posted_at: Optional[datetime.datetime],
                 reply_to_id: Optional[int],
                 deleted: bool,
                 html: Optional[str]):
        """
        manaba スレッドコメント

        Args:
            course_id: コース ID
            thread_id: スレッド ID
            comment_id: コメント ID
            title: コメントタイトル
            author: 投稿者
            posted_at: 投稿日時
            reply_to_id: リプライ先コメント ID
            deleted: 削除済みか
            html: コメント HTML
        """
        self._course_id = course_id
        self._thread_id = thread_id
        self._comment_id = comment_id
        self._title = title
        self._author = author
        self._posted_at = posted_at
        self._reply_to_id = reply_to_id
        self._deleted = deleted
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
    def thread_id(self) -> int:
        """
        スレッド ID (URLの一部)

        Returns:
            int: スレッド ID
        """
        return self._thread_id

    @property
    def comment_id(self) -> int:
        """
        コメント ID (URLの一部)

        Returns:
            int: コメント ID
        """
        return self._comment_id

    @property
    def title(self) -> Optional[str]:
        """
        コメントタイトル

        Returns:
            Optional[str]: コメントタイトル

        Notes:
            コメントが削除されている場合、この項目は None になります。
        """
        return self._title

    @property
    def author(self) -> Optional[str]:
        """
        投稿者名

        Returns:
            Optional[str]: 投稿者名

        Notes:
            コメントが削除されている場合、この項目は None になります。
        """
        return self._author

    @property
    def posted_at(self) -> Optional[datetime.datetime]:
        """
        投稿時刻

        Returns:
            Optional[datetime.datetime]: 投稿時刻

        Notes:
            コメントが削除されている場合、この項目は None になります。
        """
        return self._posted_at

    @property
    def reply_to_id(self) -> Optional[int]:
        """
        リプライ先コメント ID (リプライではない場合 None)

        Returns:
            リプライ先コメント ID
        """
        return self._reply_to_id

    @property
    def deleted(self) -> bool:
        """
        削除済みかどうか

        Returns:
            bool: 削除されている場合は True、削除されていない場合は False
        """
        return self._deleted

    @property
    def html(self) -> Optional[str]:
        """
        コメントの HTML

        Returns:
            Optional[str]: コメントの HTML
        """
        return self._html

    @property
    def files(self) -> list[ManabaFile]:
        """
        コメントに添付されているファイルの一覧

        Returns:
            list[ManabaFile]: コメントに添付されているファイルの一覧

        Notes:
            この項目は、取得できない もしくは 存在しなかった としても空のリストになります。
        """
        return self._files

    def __str__(self) -> str:
        return "ManabaThreadComment{course_id=%s,thread_id=%s,comment_id=%s,title=%s,author=%s,posted_at=%s,reply_to_id=%s,deleted=%s}" % (
            self._course_id, self._thread_id, self._comment_id, self._title, self._author, self._posted_at,
            self._reply_to_id, self._deleted)
