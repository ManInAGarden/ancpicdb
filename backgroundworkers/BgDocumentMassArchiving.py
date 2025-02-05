
from PersistClasses import Document, DataGroup
from DocArchiver import DocArchiver

from backgroundworkers.BgMassArchivingBase import BgMassArchivingBase
from backgroundworkers.BgBasics import *

class BgDocumentMassArchiving(BgMassArchivingBase):

    def __init__(self, notifywin, paras : dict):
        super().__init__(notifywin, paras)
        self._logger.debug("Initialising BgDocumentMassArchiving")

    def _calc_group(self, fpath : str) -> DataGroup:
        """ Try to find the document group the document should be
            assiciated to
        """
        return super()._calc_group(fpath, "DOC")


    