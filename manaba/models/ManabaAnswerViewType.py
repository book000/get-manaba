"""
manaba 正解の公開 (小テストドリル)
"""

from enum import Enum, auto
from typing import Optional


class ManabaAnswerViewType(Enum):
    """
    manaba 正解の公開 (小テストドリル)
    """
    PUBLISH_AT_SUBMIT = (auto(), "提出時に公開する")
    UNPUBLISH = (auto(), "公開しない")
    UNKNOWN = (auto(), None)

    def __init__(self,
                 _id: int,
                 showing_name: str):
        self.id = _id
        self.showing_name = showing_name

    def __str__(self) -> str:
        return "ManabaAnswerViewType{id=%s,showing_name=%s}" % (self.id, self.showing_name)


def get_answer_view_type_from_name(name: Optional[str]) -> Optional[ManabaAnswerViewType]:
    """
    メンバー名称を指定して列挙メンバーを取得します

    Args:
        name: メンバー名称

    Returns:
        Optional[ManabaResultViewType]: 該当する列挙メンバー、ないか、入力値が None なら None
    """
    if name is None:
        return None

    for e in ManabaAnswerViewType:
        if e.name == name:
            return e
    return None


def get_answer_view_type(showing_name: Optional[str]) -> Optional[ManabaAnswerViewType]:
    """
    表示名を指定して列挙メンバーを取得します

    Args:
        showing_name: 表示名

    Returns:
        Optional[ManabaStudentReSubmitType]: 該当する列挙メンバー、なければ None
    """
    if showing_name is None:
        return None

    for item in ManabaAnswerViewType:
        if item.showing_name == showing_name:
            return item
    return None
