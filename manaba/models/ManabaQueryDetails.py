"""
manaba 小テスト詳細
"""

import datetime
from typing import Optional, Union

from manaba.models.ManabaGradePosition import ManabaGradePosition
from manaba.models.ManabaModel import ManabaModel
from manaba.models.ManabaPortfolioType import ManabaPortfolioType
from manaba.models.ManabaResultViewType import ManabaResultViewType
from manaba.models.ManabaTaskStatus import ManabaTaskStatus


class ManabaQueryDetails(ManabaModel):
    """
    manaba 小テスト詳細
    """

    def __init__(self,
                 course_id: int,
                 query_id: int,
                 title: str,
                 description: Optional[str],
                 reception_start_time: Optional[datetime.datetime],
                 reception_end_time: Optional[datetime.datetime],
                 portfolio_type: Optional[ManabaPortfolioType],
                 result_view_type: Optional[ManabaResultViewType],
                 status: Optional[ManabaTaskStatus],
                 grade: Union[None, int],
                 position: Optional[ManabaGradePosition]):
        """
        manaba 小テスト詳細

        Args:
            course_id: コース ID
            query_id: 小テスト ID
            title: タイトル
            description: 課題に関する説明
            reception_start_time: 受付開始日時
            reception_end_time: 受付終了日時
            portfolio_type: ポートフォリオ
            result_view_type: 採点結果と正解の公開
            status: 状態
            grade: 成績
            position: 成績ポジション
        """
        self._course_id = course_id
        self._query_id = query_id
        self._title = title
        self._description = description
        self._reception_start_time = reception_start_time
        self._reception_end_time = reception_end_time
        self._portfolio_type = portfolio_type
        self._result_view_type = result_view_type
        self._status = status
        self._grade = grade
        self._position = position

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
        タイトル

        Returns:
            str: タイトル
        """
        return self._title

    @property
    def description(self) -> Optional[str]:
        """
        課題に関する説明

        Returns:
            str: 課題に関する説明
        """
        return self._description

    @property
    def reception_start_time(self) -> Optional[datetime.datetime]:
        """
        受付開始日時

        Returns:
            Optional[datetime.datetime]: 受付開始日時
        """
        return self._reception_start_time

    @property
    def reception_end_time(self) -> Optional[datetime.datetime]:
        """
        受付終了日時

        Returns:
            Optional[datetime.datetime]: 受付終了日時
        """
        return self._reception_end_time

    @property
    def portfolio_type(self) -> Optional[ManabaPortfolioType]:
        """
        ポートフォリオ種別

        Returns:
            ManabaPortfolioType: ポートフォリオ種別
        """
        return self._portfolio_type

    @property
    def result_view_type(self) -> Optional[ManabaResultViewType]:
        """
        採点結果と正解の公開

        Returns:
            ManabaResultViewType: 採点結果と正解の公開
        """
        return self._result_view_type

    @property
    def status(self) -> Optional[ManabaTaskStatus]:
        """
        課題の状態

        Returns:
            ManabaTaskStatus: 状態
        """
        return self._status

    @property
    def grade(self) -> Union[None, int]:
        """
        成績

        Returns:
            Union[None, int]: 成績 (点数が付けられていない場合は None。例えば未提出、回答公開待ち)
        """
        return self._grade

    @property
    def position(self) -> Optional[ManabaGradePosition]:
        """
        成績のポジション

        Returns:
            ManabaGradePosition: 成績のポジション
        """
        return self._position

    def __str__(self) -> str:
        return "ManabaQueryDetails{course_id=%s,query_id=%s,title=%s,description=%s,reception_start_time=%s,reception_end_time=%s,portfolio_type=%s,result_view_type=%s,status=%s,grade=%s,position=%s}" % (
            self._course_id, self._query_id, self._title, self._description, self._reception_start_time,
            self._reception_end_time, self._portfolio_type, self._result_view_type, self._status, self._grade,
            self._position)
