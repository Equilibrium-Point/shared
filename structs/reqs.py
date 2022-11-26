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

    @classmethod
    def from_request(cls, request: "Request", images: List[str], image_index: int = 0):
        """
        Create an upscale request from a request

        Args:
            request (Request): a request
        """
        fields = request.dict()
        fields["request_type"] = RequestType.UPSCALE_REQUEST_TYPE
        fields["params"]["upscale"] = True
        fields["params"]["seed"] = fields["params"]["seed"] + image_index
        fields["metadata"]["variation_ui_fields"] = False
        return cls(**fields, images=[images[image_index]])
