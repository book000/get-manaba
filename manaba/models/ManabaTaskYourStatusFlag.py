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
    UNSUBMITTED = (auto(), "未提出", "まだ提出していません")
    SUBMITTED = (auto(), "提出済み")

    def __init__(self,
                 _id: int,
                 *showing_name: str):
        self._id = _id
        self.showing_name = showing_name

    def __str__(self) -> str:
        return "ManabaTaskYourStatusFlag{id=%s,showing_name=%s}" % (self._id, self.showing_name)


def get_your_status_from_name(name: Optional[str]) -> Optional[ManabaTaskYourStatusFlag]:
    """
    メンバー名称を指定して列挙メンバーを取得します

    Args:
        name: メンバー名称

    Returns:
        Optional[ManabaTaskYourStatusFlag]: 該当する列挙メンバー、ないか、入力値が None なら None
    """
    if name is None:
        return None

    for e in ManabaTaskYourStatusFlag:
        if e.name == name:
            return e
    return None


def get_your_status(showing_name: str) -> Optional[ManabaTaskYourStatusFlag]:
    """
    表示名を指定して列挙メンバーを取得します (合致、もしくは前方一致)

    Args:
        showing_name: 表示名

    Returns:
        Optional[ManabaTaskYourStatusFlag]: 該当する列挙メンバー、なければ None
    """
    for item in ManabaTaskYourStatusFlag:
        if showing_name in item.showing_name:
            return item

        if item.showing_name is not None and \
                len(list(filter(lambda x: x is not None and showing_name.startswith(x), item.showing_name))) >= 1:
            return item
    return None
