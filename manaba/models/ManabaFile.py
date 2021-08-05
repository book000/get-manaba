"""
manaba ファイル
"""
from typing import Optional

from manaba.models.ManabaModel import ManabaModel


class ManabaFile(ManabaModel):
    """
    manaba ファイル

    Notes:
        このモデルは ManabaContentPage・ManabaCourseNews・ManabaThreadComment で使用されますが、現在サポートされているのは ManabaContentPage のみです。
    """

    def __init__(self,
                 parent: ManabaModel,
                 name: Optional[str],
                 download_url: str):
        """
        manaba ファイル

        Args:
            parent: 親モデル (例えば、ManabaContentPage・ManabaCourseNews・ManabaThreadComment)
            name: ファイル名
            download_url: ファイルダウンロード URL
        """
        self.parent = parent
        self._name = name
        self._download_url = download_url
