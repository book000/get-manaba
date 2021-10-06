"""
manaba レポート詳細
"""
import datetime
from typing import Optional

from manaba.models.ManabaModel import ManabaModel
from manaba.models.ManabaPortfolioType import ManabaPortfolioType
from manaba.models.ManabaResultViewType import ManabaResultViewType
from manaba.models.ManabaStudentReSubmitType import ManabaStudentReSubmitType
from manaba.models.ManabaTaskStatus import ManabaTaskStatus


class ManabaReportDetails(ManabaModel):
    """
    manaba レポート詳細
    """

    def __init__(self,
                 course_id: int,
                 report_id: int,
                 title: str,
                 description: Optional[str],
                 reception_start_time: Optional[datetime.datetime],
                 reception_end_time: Optional[datetime.datetime],
                 portfolio_type: Optional[ManabaPortfolioType],
                 result_view_type: Optional[ManabaResultViewType],
                 student_resubmit_type: Optional[ManabaStudentReSubmitType],
                 status: Optional[ManabaTaskStatus]):
        """
        manaba レポート詳細

        Args:
            course_id: コース ID
            report_id: レポート ID
            title: タイトル
            description: 課題に関する説明
            reception_start_time: 受付開始日時
            reception_end_time: 受付終了日時
            portfolio_type: ポートフォリオ
            result_view_type: 閲覧設定
            student_resubmit_type: 学生による再提出の許可
            status: 状態
        """
        self._course_id = course_id
        self._report_id = report_id
        self._title = title
        self._description = description
        self._reception_start_time = reception_start_time
        self._reception_end_time = reception_end_time
        self._portfolio_type = portfolio_type
        self._result_view_type = result_view_type
        self._student_resubmit_type = student_resubmit_type
        self._status = status

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
    def report_id(self) -> int:
        """
        レポート ID

        Returns:
            int: レポート ID
        """
        return self._report_id

    @property
    def title(self) -> str:
        """
        レポートタイトル

        Returns:
            str: レポートタイトル
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
    def portfolio_type(self) -> Optional[ManabaPortfolioType]:
        """
        ポートフォリオ種別

        Returns:
            Optional[ManabaPortfolioType]: ポートフォリオ
        """
        return self._portfolio_type

    @property
    def result_view_type(self) -> Optional[ManabaResultViewType]:
        """
        閲覧設定

        Returns:
            Optional[ManabaResultViewType]: 閲覧設定
        """
        return self._result_view_type

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

    def __str__(self) -> str:
        return "ManabaReportDetails{course_id=%s,report_id=%s,title=%s,description=%s,reception_start_time=%s,reception_end_time=%s,portfolio_type=%s,result_view_type=%s,student_resubmit_type=%s,status=%s}" % (
            self._course_id, self._report_id, self._title, self._description, self._reception_start_time,
            self._reception_end_time, self._portfolio_type, self._result_view_type, self._student_resubmit_type,
            self._status)
