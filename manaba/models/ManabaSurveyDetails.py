"""
manaba アンケート詳細
"""
import datetime
from typing import Optional

from manaba.models.ManabaPortfolioType import ManabaPortfolioType
from manaba.models.ManabaStudentReSubmitType import ManabaStudentReSubmitType
from manaba.models.ManabaTaskStatus import ManabaTaskStatus


class ManabaSurveyDetails:
    """
    manaba アンケート詳細
    """

    def __init__(self,
                 survey_id: int,
                 title: str,
                 reception_start_time: Optional[datetime.datetime],
                 reception_end_time: Optional[datetime.datetime],
                 portfolio_type: Optional[ManabaPortfolioType],
                 student_resubmit_type: Optional[ManabaStudentReSubmitType],
                 status: Optional[ManabaTaskStatus]):
        """
        manaba アンケート詳細

        Args:
            survey_id: 小テスト ID
            title: タイトル
            reception_start_time: 受付開始日時
            reception_end_time: 受付終了日時
            portfolio_type: ポートフォリオ
            student_resubmit_type: 学生による再提出の許可
            status: 状態
        """
        self._survey_id = survey_id
        self._title = title
        self._reception_start_time = reception_start_time
        self._reception_end_time = reception_end_time
        self._portfolio_type = portfolio_type
        self._student_resubmit_type = student_resubmit_type
        self._status = status

    @property
    def survey_id(self) -> int:
        """
        アンケート ID

        Returns:
            int: アンケート ID
        """
        return self._survey_id

    @property
    def title(self) -> str:
        """
        アンケートタイトル

        Returns:
            str: アンケートタイトル
        """
        return self._title

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
            Optional[ManabaPortfolioType]: ポートフォリオ
        """
        return self._portfolio_type

    @property
    def student_resubmit_type(self) -> Optional[ManabaStudentReSubmitType]:
        """
        学生による再提出の許可

        Returns:
            Optional[ManabaStudentReSubmitType]: 学生による再提出の許可
        """
        return self._student_resubmit_type

    @property
    def status(self) -> Optional[ManabaTaskStatus]:
        """
        状態

        Returns:
            Optional[ManabaTaskStatus]: 状態
        """
        return self._status
