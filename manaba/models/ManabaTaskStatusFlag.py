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

    def __init__(self,
                 _id: int,
                 showing_name: str):
        self.id = _id
        self.showing_name = showing_name

    def __str__(self) -> str:
        return "ManabaTaskStatusFlag{id=%s,showing_name=%s}" % (self.id, self.showing_name)


def get_task_status_from_name(name: Optional[str]) -> Optional[ManabaTaskStatusFlag]:
    """
    メンバー名称を指定して列挙メンバーを取得します

    Args:
        name: メンバー名称

    Returns:
        Optional[ManabaTaskStatusFlag]: 該当する列挙メンバー、ないか、入力値が None なら None
    """
    if name is None:
        return None

    for e in ManabaTaskStatusFlag:
        if e.name == name:
            return e
    return None


def get_task_status(showing_name: str) -> Optional[ManabaTaskStatusFlag]:
    """
    表示名を指定して列挙メンバーを取得します

    Args:
        showing_name: メンバー ID

    Returns:
        Optional[ManabaTaskStatusFlag]: 該当する列挙メンバー、なければ None
    """
    for item in ManabaTaskStatusFlag:
        if item.showing_name == showing_name:
            return item
    return None
