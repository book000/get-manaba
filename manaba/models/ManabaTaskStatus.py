"""
    manaba タスク(小テスト・アンケート・レポート)のステータス
"""

from typing import Optional

from manaba.models.ManabaModel import ManabaModel
from manaba.models.ManabaTaskStatusFlag import ManabaTaskStatusFlag
from manaba.models.ManabaTaskYourStatusFlag import ManabaTaskYourStatusFlag


class ManabaTaskStatus(ManabaModel):
    """
    manaba タスク(小テスト・アンケート・レポート)のステータス
    """

    def __init__(self,
                 task_status: ManabaTaskStatusFlag,
                 your_status: Optional[ManabaTaskYourStatusFlag]):
        self._task_status = task_status
        self._your_status = your_status

    def __str__(self) -> str:
        return "ManabaTaskStatus{task_status=%s,your_status=%s}" % (self._task_status, self._your_status)

    @property
    def task_status(self) -> ManabaTaskStatusFlag:
        """
        タスク自体のステータス

        Returns:
            ManabaTaskStatusFlag: タスク自体のステータス
        """
        return self._task_status

    @property
    def your_status(self) -> Optional[ManabaTaskYourStatusFlag]:
        """
        ユーザー自身のタスクステータス

        Returns:
            Optional[ManabaTaskYourStatusFlag]: ユーザー自身のタスクステータス
        """
        return self._your_status
