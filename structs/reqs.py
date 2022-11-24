from typing import Optional

from pydantic import BaseModel

from structs.common import Metadata, Params, RequestType


class Request(BaseModel):
    request_type: RequestType
    ui_fields: Optional[list]
    user_tag: str
    user_id: int
    channel_id: int
    confirm_message_id: int

    params: Params
    metadata: Metadata
