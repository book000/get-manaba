"""
manaba 採点結果と正解の公開 種別 (小テスト) / 閲覧設定 (レポート)
"""

from enum import Enum, auto
from typing import Optional


class ManabaResultViewType(Enum):
    """
    manaba 採点結果と正解の公開 種別 (小テスト)
    """
    ENDED_RESULT_VIEWABLE = (auto(), "受付終了時に採点結果と正解を公開")
    SUBMIT_RESULT_VIEWABLE = (auto(), "提出時に採点結果と正解を公開")
    YOU_AND_TEACHER_VIEWABLE = (auto(), "提出者本人と教員のみ閲覧・コメント可（個別指導）")
    SUBMITTED_MEMBER_AND_TEACHER_VIEWABLE = (auto(), "同じ課題の提出者と教員が閲覧・コメント可")
    ALL_MEMBER_VIEWABLE = (auto(), "コースメンバー全員が閲覧・コメント可")
    COLLECT_ONLY = (auto(), "回収のみ行なう")
    UNKNOWN = (auto(), None)

    def __init__(self,
                 _id: int,
                 showing_name: str):
        self.id = _id
        self.showing_name = showing_name

    def __str__(self) -> str:
        return "ManabaResultViewType{id=%s,showing_name=%s}" % (self.id, self.showing_name)


def get_result_view_type_from_name(name: Optional[str]) -> Optional[ManabaResultViewType]:
    """
    メンバー名称を指定して列挙メンバーを取得します

    Args:
        name: メンバー名称

    Returns:
        Optional[ManabaResultViewType]: 該当する列挙メンバー、ないか、入力値が None なら None
    """
    if name is None:
        return None

    for e in ManabaResultViewType:
        if e.name == name:
            return e
    return None


def get_result_view_type(showing_name: Optional[str]) -> Optional[ManabaResultViewType]:
    """
    表示名を指定して列挙メンバーを取得します (合致、もしくは包含)

    Args:
        showing_name: 表示名

    Returns:
        Optional[ManabaResultViewType]: 該当する列挙メンバー、なければ None
    """
    if showing_name is None:
        return None

    for item in ManabaResultViewType:
        if item.showing_name == showing_name:
            return item
        if item.showing_name is not None and item.showing_name in showing_name:
            return item
    return None
