"""
manaba タスク(小テスト・アンケート・レポート)のステータスフラグ
"""

from enum import Enum, auto
from typing import Optional


class ManabaTaskStatusFlag(Enum):
    """
    manaba タスク(小テスト・アンケート・レポート)のステータスフラグ
    """
    WAITING = (auto(), "受付開始待ち")
    OPENING = (auto(), "受付中")
    CLOSED = (auto(), "受付終了")

    def __init__(self, _id: int, showing_name: str):
        self.id = _id
        self.showing_name = showing_name


def get_task_status(showing_name: str) -> Optional[ManabaTaskStatusFlag]:
    """
    ID を指定して列挙メンバーを取得します

    Args:
        showing_name: メンバー ID

    Returns:
        Optional[dict]: 該当する列挙メンバー、なければ None
    """
    for item in ManabaTaskStatusFlag:
        if item.showing_name == showing_name:
            return item
    return None
