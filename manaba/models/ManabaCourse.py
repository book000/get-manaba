"""
manaba コース情報
"""

from typing import Optional

from manaba.models.ManabaCourseLamps import ManabaCourseLamps
from manaba.models.ManabaModel import ManabaModel


class ManabaCourse(ManabaModel):
    """
    manaba コース情報
    """

    def __init__(self,
                 name: str,
                 course_id: int,
                 year: Optional[int],
                 lecture_at: Optional[str],
                 teacher: Optional[str],
                 status_lamps: Optional[ManabaCourseLamps]):
        """
        manaba コース情報

        Args:
            name: コース名
            course_id: コース ID
            year: コース年度
            lecture_at: 時限
            teacher: 担当教員名
            status_lamps: ステータスランプ
        """
        self._name = name
        self._course_id = course_id
        self._year = year
        self._lecture_at = lecture_at
        self._teacher = teacher
        self._status_lamps = status_lamps

    @property
    def name(self) -> str:
        """
        コース名

        Returns:
            str: コースの名称
        """
        return self._name

    @property
    def course_id(self) -> int:
        """
        コース ID (URLの一部)
        ※コースコードではない

        Returns:
            int: コース ID
        """
        return self._course_id

    @property
    def year(self) -> Optional[int]:
        """
        コースの年度

        Returns:
            Optional[int]: コースの年度

        Notes:
            コース一覧にて曜日表示を利用している場合、この項目は None になる可能性があります。
        """
        return self._year

    @property
    def lecture_at(self) -> Optional[str]:
        """
        コース年度・時限

        Returns:
            Optional[str]: コースの年度および時限 (取得できない場合 None)
        """
        return self._lecture_at

    @property
    def teacher(self) -> Optional[str]:
        """
        コースの担当教員名

        Returns:
            Optional[str]: コースの担当教員名 (取得できない場合 None)
        """
        return self._teacher

    @property
    def status_lamps(self) -> Optional[ManabaCourseLamps]:
        """
        コースのステータスランプ

        Returns:
            Optional[ManabaCourseLamps]: コースのステータスランプ

        Notes:
            コース一覧にて曜日表示を利用している場合、この項目は None になる可能性があります。
        """
        return self._status_lamps

    def __str__(self) -> str:
        return "ManabaCourse{course_id=%s,name=%s,year=%s,teacher=%s}" % (
            self._course_id, self._name, self._year, self._teacher)
