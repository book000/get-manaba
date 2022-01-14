"""
manaba 小テスト (ドリル) 詳細
"""
import datetime
from typing import Optional

from manaba.models.ManabaAnswerViewType import ManabaAnswerViewType
from manaba.models.ManabaModel import ManabaModel
from manaba.models.ManabaPortfolioType import ManabaPortfolioType
from manaba.models.ManabaTaskStatus import ManabaTaskStatus


class ManabaDrillDetails(ManabaModel):
    """
    manaba 小テスト ドリル詳細
    """

    def __init__(self,
                 course_id: int,
                 drill_id: int,
                 title: str,
                 description: Optional[str],
                 reception_start_time: Optional[datetime.datetime],
                 reception_end_time: Optional[datetime.datetime],
                 submission_limit: int,
                 portfolio_type: Optional[ManabaPortfolioType],
                 answer_view_type: Optional[ManabaAnswerViewType],
                 status: Optional[ManabaTaskStatus],
                 count_exams: Optional[int],
                 max_score: Optional[int],
                 passing_conditions: Optional[int]):
        """
        manaba 小テスト ドリル詳細

        Args:
            course_id: コース ID
            drill_id: 小テスト ID
            title: タイトル
            description: 課題に関する説明
            reception_start_time: 受付開始日時
            reception_end_time: 受付終了日時
            submission_limit: 提出上限 (無制限の場合 -1)
            portfolio_type: ポートフォリオ
            answer_view_type: 正解の公開
            status: 状態
            count_exams: 受験回数 (未回答の場合 None)
            max_score: 最高得点 (未回答の場合 None)
            passing_conditions: 合格条件 (合格条件未指定の場合 -1)
        """
        self._course_id = course_id
        self._drill_id = drill_id
        self._title = title
        self._description = description
        self._reception_start_time = reception_start_time
        self._reception_end_time = reception_end_time
        self._submission_limit = submission_limit
        self._portfolio_type = portfolio_type
        self._answer_view_type = answer_view_type
        self._status = status
        self._count_exams = count_exams
        self._max_score = max_score
        self._passing_conditions = passing_conditions

    @property
    def course_id(self) -> int:
        """
        コース ID

        Returns:
            int: コース ID
        """
        return self._course_id

    @property
    def drill_id(self) -> int:
        """
        小テスト ID

        Returns:
            int: 小テスト ID
        """
        return self._drill_id

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
            Optional[str]: 課題に関する説明
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
    def submission_limit(self) -> Optional[int]:
        """
        提出上限

        Returns:
            Optional[int]: 提出上限
        """
        return self._submission_limit

    @property
    def portfolio_type(self) -> Optional[ManabaPortfolioType]:
        """
        ポートフォリオ

        Returns:
            Optional[ManabaPortfolioType]: ポートフォリオ
        """
        return self._portfolio_type

    @property
    def answer_view_type(self) -> Optional[ManabaAnswerViewType]:
        """
        正解の公開

        Returns:
            Optional[ManabaAnswerViewType]: 正解の公開
        """
        return self._answer_view_type

    @property
    def status(self) -> Optional[ManabaTaskStatus]:
        """
        状態

        Returns:
            Optional[ManabaTaskStatus]: 状態
        """
        return self._status

    @property
    def count_exams(self) -> Optional[int]:
        """
        受験回数

        Returns:
            Optional[int]:: 受験回数
        """
        return self._count_exams

    @property
    def max_score(self) -> Optional[int]:
        """
        最高得点

        Returns:
            Optional[int]: 最高得点
        """
        return self._max_score

    @property
    def passing_conditions(self) -> Optional[int]:
        """
        合格条件

        Returns:
            Optional[int]: 合格条件
        """
        return self._passing_conditions
