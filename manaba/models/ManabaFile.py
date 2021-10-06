"""
manaba ファイル
"""
import datetime
from typing import Optional

from manaba.models.ManabaModel import ManabaModel


class ManabaFile(ManabaModel):
    """
    manaba ファイル

    Notes:
        このモデルは :class:`manaba.models.ManabaContentPage`・:class:`manaba.models.ManabaCourseNews`・:class:`manaba.models.ManabaThreadComment` で使用されます。
    """

    def __init__(self,
                 parent: ManabaModel,
                 name: str,
                 uploaded_at: Optional[datetime.datetime],
                 download_url: str):
        """
        manaba ファイル

        Args:
            parent: 親モデル (例えば、ManabaContentPage・ManabaCourseNews・ManabaThreadComment)
            name: ファイル名
            uploaded_at: アップロード日時
            download_url: ファイルダウンロード URL
        """
        self._parent = parent
        self._name = name
        self._uploaded_at = uploaded_at
        self._download_url = download_url

    @property
    def parent(self) -> ManabaModel:
        """
        親モデル
        (例えば、ManabaContentPage・ManabaCourseNews・ManabaThreadComment)

        Returns:
            ManabaModel: 親モデル
        """
        return self._parent

    @property
    def name(self) -> str:
        """
        ファイル名

        Returns:
            str: ファイル名
        """
        return self._name

    @property
    def uploaded_at(self) -> Optional[datetime.datetime]:
        """
        アップロード日時

        Returns:
            Optional[datetime.datetime]: アップロード日時
        """
        return self._uploaded_at

    @property
    def download_url(self) -> str:
        """
        ファイルダウンロード URL

        Returns:
            str: ファイルダウンロード URL
        """
        return self._download_url

    def __str__(self) -> str:
        return "ManabaFile{parent=%s,name=%s,uploaded_at=%s,download_url=%s}" % (
            self._parent, self._name, self.uploaded_at, self._download_url)
