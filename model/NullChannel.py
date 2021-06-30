from .CoarseChannel import CoarseChannel

from uuid import uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Fixture import Fixture


class NullChannel(CoarseChannel):
    '''Dummy channel used to represent `null` in a mode's channel list.'''

    def __init__(self, fixture: 'Fixture') -> None:
        super().__init__(f"null-{uuid4()}", {
            "name": "No Function",
            "capability": {
                "type": "NoFunction"
            }
        }, fixture)
