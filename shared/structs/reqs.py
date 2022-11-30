from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from shared.structs.common import Metadata, Params, RequestType


class Request(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    request_type: RequestType
    user_tag: str
    user_id: int
    channel_id: int
    confirm_message_id: int

    params: Params
    metadata: Metadata

    def add_timestamp(self, moment_name: str, time: Optional[datetime] = None):
        """Adds a timestamp to the request, with the current time if no time is provided

        Args:
            moment_name (str): The name of the moment to add
            time (Optional[datetime]): the timestamp to add. Now if not specified
        """
        time = time or datetime.utcnow()
        self.metadata.metrics[moment_name] = time.timestamp()


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
