"""
    manaba タスク(小テスト・アンケート・レポート)のステータス
"""

from typing import Optional

from src.models.ManabaTaskStatusFlag import ManabaTaskStatusFlag
from src.models.ManabaTaskYourStatusFlag import ManabaTaskYourStatusFlag


class ManabaTaskStatus:
    """
    manaba タスク(小テスト・アンケート・レポート)のステータス
    """

    def __init__(self, task_status: ManabaTaskStatusFlag, your_status: Optional[ManabaTaskYourStatusFlag]):
        self.task_status = task_status
        self.your_status = your_status
