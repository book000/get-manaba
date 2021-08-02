"""
manaba 小テスト
"""

import datetime
from typing import Optional

from manaba.models.ManabaTaskStatus import ManabaTaskStatus


class ManabaQuery:
    """
    manaba 小テスト
    """

    def __init__(self,
                 query_id: int,
                 title: str,
                 status: ManabaTaskStatus,
                 status_lamp: bool,
                 reception_start_time: Optional[datetime.datetime],
                 reception_end_time: Optional[datetime.datetime]):
        """
        manaba 小テスト

        Args:
            query_id: 小テスト ID
            title: 小テストタイトル
            status: ステータス
            status_lamp: ステータスランプ
            reception_start_time: 受付開始日時
            reception_end_time: 受付終了日時
        """
        self._query_id = query_id
        self._title = title
        self._status = status
        self._status_lamp = status_lamp
        self._reception_start_time = reception_start_time
        self._reception_end_time = reception_end_time

    @property
    def query_id(self) -> int:
        """
        小テスト ID

        Returns:
            int: ID
        """
        return self._query_id

    @property
    def title(self) -> str:
        """
        小テストタイトル

        Returns:
            str: タイトル
        """
        return self._title

    @property
    def status(self) -> ManabaTaskStatus:
        """
        ステータス

        Returns:
            ManabaTaskStatus: ステータス
        """
        return self._status

    @property
    def status_lamp(self) -> bool:
        """
        ステータスランプ

        Returns:
            bool: ステータスランプが点いているか
        """
        return self._status_lamp

    @property
    def reception_start_time(self) -> Optional[datetime.datetime]:
        """
        開始日時

        Returns:
            Optional[datetime.datetime]: 受付開始日時
        """
        return self._reception_start_time

    @property
    def reception_end_time(self) -> Optional[datetime.datetime]:
        """
        終了日時

        Returns:
            Optional[datetime.datetime]: 受付終了日時
        """
        return self._reception_end_time
