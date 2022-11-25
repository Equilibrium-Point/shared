from pydantic import BaseModel
from typing import List
from structs.common import Metadata, Params, RequestType


class Request(BaseModel):
    request_type: RequestType
    user_tag: str
    user_id: int
    channel_id: int
    confirm_message_id: int

    params: Params
    metadata: Metadata


class UpscaleRequest(Request):
    request_type: RequestType = RequestType.UPSCALE_REQUEST_TYPE

    images: List[str]