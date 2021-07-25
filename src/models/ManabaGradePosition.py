"""
manaba 成績ポジション
"""
from typing import Optional


class ManabaGradePosition:
    """
    manaba 成績ポジション
    """

    def __init__(self,
                 below_percent: Optional[int],
                 my_position_percent: int,
                 above_percent: Optional[int]):
        self._below_percent = below_percent
        self._my_position_percent = my_position_percent
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
    def my_position_percent(self) -> int:
        """
        自分の成績と同じメンバーの割合

        Returns:
            int: 自分の成績と同じメンバーの割合
        """
        return self._my_position_percent

    @property
    def above_percent(self) -> Optional[int]:
        """
        自分より上の成績割合

        Returns:
            int: 自分より上の成績割合
        """
        return self._above_percent
