"""
manaba 学生による再提出の許可 (アンケート)
"""

from enum import Enum, auto
from typing import Optional


class ManabaStudentReSubmitType(Enum):
    """
    manaba 学生による再提出の許可 (アンケート)
    """
    RESUBMITABLE = (auto(), "再提出を許可する")
    UNRESUBMITABLE = (auto(), "再提出を許可しない")
    UNKNOWN = (auto(), None)

    def __init__(self,
                 _id: int,
                 showing_name: str):
        self.id = _id
        self.showing_name = showing_name

    def __str__(self) -> str:
        return "ManabaStudentReSubmitType{id=%s,showing_name=%s}" % (self.id, self.showing_name)


def get_student_resubmit_type_from_name(name: Optional[str]) -> Optional[ManabaStudentReSubmitType]:
    """
    メンバー名称を指定して列挙メンバーを取得します

    Args:
        name: メンバー名称

    Returns:
        Optional[ManabaResultViewType]: 該当する列挙メンバー、ないか、入力値が None なら None
    """
    if name is None:
        return None

    for e in ManabaStudentReSubmitType:
        if e.name == name:
            return e
    return None


def get_student_resubmit_type(showing_name: Optional[str]) -> Optional[ManabaStudentReSubmitType]:
    """
    表示名を指定して列挙メンバーを取得します

    Args:
        showing_name: 表示名

    Returns:
        Optional[ManabaStudentReSubmitType]: 該当する列挙メンバー、なければ None
    """
    if showing_name is None:
        return None

    for item in ManabaStudentReSubmitType:
        if item.showing_name == showing_name:
            return item
    return None
