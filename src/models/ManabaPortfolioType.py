"""
manaba ポートフォリオ種別 (小テスト・アンケート・レポート)
"""

from enum import Enum, auto
from typing import Optional


class ManabaPortfolioType(Enum):
    """
    manaba ポートフォリオ種別 (小テスト)
    """
    ADD = (auto(), "ポートフォリオに追加")
    NOT_ADD = (auto(), "ポートフォリオに追加しない")
    UNKNOWN = (auto(), None)

    def __init__(self,
                 _id: int,
                 showing_name: str):
        self.id = _id
        self.showing_name = showing_name


def get_portfolio_type(showing_name: Optional[str]) -> Optional[ManabaPortfolioType]:
    """
    表示名を指定して列挙メンバーを取得します (合致、もしくは包含)

    Args:
        showing_name: 表示名

    Returns:
        Optional[ManabaPortfolioType]: 該当する列挙メンバー、なければ None
    """
    if showing_name is None:
        return None

    for item in ManabaPortfolioType:
        if item.showing_name == showing_name:
            return item
        if item.showing_name is not None and item.showing_name in showing_name:
            return item
    return None
