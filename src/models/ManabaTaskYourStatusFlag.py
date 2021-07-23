"""
manaba タスク(小テスト・アンケート・レポート)の提出ステータスフラグ
"""

from enum import Enum, auto
from typing import Optional


class ManabaTaskYourStatusFlag(Enum):
    """
    manaba タスク(小テスト・アンケート・レポート)の提出ステータスフラグ
    """
    WAITING = (auto(), None)
    UNSUBMITTED = (auto(), "未提出")
    SUBMITTED = (auto(), "提出済み")

    def __init__(self, _id: int, showing_name: str):
        self._id = _id
        self.showing_name = showing_name


def get_your_status(showing_name: str) -> Optional[ManabaTaskYourStatusFlag]:
    """
    ID を指定して列挙メンバーを取得します

    Args:
        showing_name: メンバー ID

    Returns:
        Optional[dict]: 該当する列挙メンバー、なければ None
    """
    for item in ManabaTaskYourStatusFlag:
        if item.showing_name == showing_name:
            return item
    return None
