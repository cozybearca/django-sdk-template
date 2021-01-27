from logging import getLogger

from src.common import models as m
from src.common import permissions as p

LOG = getLogger(__name__)


def reset_site():
    """
    Some reset code for the entire site.
    """
    LOG.info("resetting some data...")
    m.Enum.refresh_db()
    p.setup_permissions()
