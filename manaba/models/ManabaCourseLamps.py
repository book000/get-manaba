"""
manaba コース一覧ページに表示されるランプ管理クラス
"""
from manaba.models.ManabaModel import ManabaModel


class ManabaCourseLamps(ManabaModel):
    """
    manaba コース一覧ページに表示されるランプ管理クラス
    """

    def __init__(self,
                 news: bool,
                 deadline: bool,
                 grad: bool,
                 thread: bool,
                 individual: bool) -> None:
        self._news = news
        self._deadline = deadline
        self._grad = grad
        self._thread = thread
        self._individual = individual

    @property
    def news(self) -> bool:
        """
        コースニュースランプ

        Returns:
            bool: newsランプが点いているか
        """
        return self._news

    @property
    def deadline(self) -> bool:
        """
        デッドラインランプ (課題ランプ)

        Returns:
            bool: デッドラインランプが点いているか
        """
        return self._deadline

    @property
    def grad(self) -> bool:
        """
        グラッドランプ (成績ランプ)

        Returns:
            bool: 成績ランプが点いているか
        """
        return self._grad

    @property
    def thread(self) -> bool:
        """
        スレッドランプ

        Returns:
            bool: スレッドランプが点いているか
        """
        return self._thread

    @property
    def individual(self) -> bool:
        """
        個人ランプ (コレクション)

        Returns:
            bool: 個人ランプが点いているか
        """
        return self._individual

    def __str__(self) -> str:
        return "ManabaCourseLamps{news=%s,deadline=%s,grad=%s,thread=%s,individual=%s}" % (
            self._news, self._deadline, self._grad, self._thread, self._individual)
