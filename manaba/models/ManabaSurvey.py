"""
manaba アンケート
"""

import datetime
from typing import Optional

from manaba.models.ManabaModel import ManabaModel
from manaba.models.ManabaTaskStatus import ManabaTaskStatus


class ManabaSurvey(ManabaModel):
    """
    manaba アンケート
    """

    def __init__(self,
                 course_id: int,
                 survey_id: int,
                 title: str,
                 status: ManabaTaskStatus,
                 status_lamp: bool,
                 reception_start_time: Optional[datetime.datetime],
                 reception_end_time: Optional[datetime.datetime]):
        """
        manaba アンケート

        Args:
            course_id: コース ID
            survey_id: アンケート ID
            title: アンケートタイトル
            status: ステータス
            status_lamp: ステータスランプ
            reception_start_time: 開始日時
            reception_end_time: 終了日時
        """
        self._course_id = course_id
        self._survey_id = survey_id
        self._title = title
        self._status = status
        self._status_lamp = status_lamp
        self._reception_start_time = reception_start_time
        self._reception_end_time = reception_end_time

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
    def survey_id(self) -> int:
        """
        アンケート ID

        Returns:
            int: ID
        """
        return self._survey_id

    @property
    def title(self) -> str:
        """
        アンケートタイトル

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
            Optional[datetime.datetime]: 開始日時
        """
        return self._reception_start_time

    @property
    def reception_end_time(self) -> Optional[datetime.datetime]:
        """
        終了日時

        Returns:
            Optional[datetime.datetime]: 終了日時
        """
        return self._reception_end_time

    def __str__(self) -> str:
        return "ManabaSurvey{course_id=%s,survey_id=%s,title=%s,status=%s,status_lamp=%s,reception_start_time=%s,reception_end_time=%s}" % (
            self._course_id, self._survey_id, self._title, self._status, self._status_lamp, self._reception_start_time,
            self._reception_end_time)
