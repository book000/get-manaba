"""
manaba 成績ポジション
"""
from typing import Optional

from manaba.models.ManabaModel import ManabaModel


class ManabaGradePosition(ManabaModel):
    """
    manaba 成績ポジション
    """

    def __init__(self,
                 below_percent: Optional[int],
                 _my_pos_percent: int,
                 above_percent: Optional[int]):
        self._below_percent = below_percent
        self._my_pos_percent = _my_pos_percent
        self._above_percent = above_percent

    @property
    def below_percent(self) -> Optional[int]:
        """
        自分より下の成績割合

        Returns:
            int: 自分より下の成績割合
        """
        return self._below_percent

    @property
    def my_pos_percent(self) -> int:
        """
        自分の成績と同じメンバーの割合

        Returns:
            int: 自分の成績と同じメンバーの割合
        """
        return self._my_pos_percent

    @property
    def above_percent(self) -> Optional[int]:
        """
        自分より上の成績割合

        Returns:
            int: 自分より上の成績割合
        """
        return self._above_percent

    def __str__(self) -> str:
        return "ManabaGradePosition{below_percent=%s,my_pos_percent=%s,above_percent=%s}" % (
            self._below_percent, self._my_pos_percent, self._above_percent)
