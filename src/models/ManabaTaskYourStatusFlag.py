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

    def __init__(self,
                 _id: int,
                 showing_name: str):
        self._id = _id
        self.showing_name = showing_name


def get_your_status(showing_name: str) -> Optional[ManabaTaskYourStatusFlag]:
    """
    表示名を指定して列挙メンバーを取得します (合致、もしくは前方一致)

    Args:
        showing_name: 表示名

    Returns:
        Optional[ManabaTaskYourStatusFlag]: 該当する列挙メンバー、なければ None
    """
    for item in ManabaTaskYourStatusFlag:
        if item.showing_name == showing_name:
            return item
        if item.showing_name is not None and showing_name.startswith(item.showing_name):
            return item
    return None
