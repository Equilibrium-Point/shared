from datetime import datetime
from typing import Optional, List

from pydantic import Field

from structs.common import Metadata
from structs.reqs import Request


class ResponseMetadata(Metadata):
    token_count: int
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class Response(Request):
    metadata: ResponseMetadata

    images: List[str]
    grid_images: Optional[bool]
    tensors: list
    # TODO: where is the error created? We may need another class for this
    error: Optional[str] = None  

    @classmethod
    def from_request(cls, req: Request, info: dict, images: list, grid_images: bool, tensors: list):
        """
        Create a response from a request and info dict

        Args:
            req (Request): a request
            info (dict): a dict containing info about the generation
        """
        fields = req.dict()

        params = fields.pop("params")
        params["seed"] = info["seed"] 
        params["variation_seed"] = info["subseed"]

        meta_data = fields.pop("metadata")
        meta_data["token_count"] = info["token_count"]

        return cls(
            **fields,
            images=images,
            grid_images=grid_images,
            tensors=tensors,
            params=params,
            metadata=ResponseMetadata(**meta_data),
        )

    @classmethod
    def from_upscale_request(cls, req: Request, images: list, tensors: list, error: Optional[str] = None):
        """
        Create a response from a request and info dict

        Args:
            req (Request): a request
            info (dict): a dict containing info about the generation
        """
        fields = req.dict()

        meta_data = fields.pop("metadata")
        meta_data["token_count"] = 0    # Not used in upscale request

        return cls(
            **fields,
            images=images,
            tensors=tensors,
            metadata=ResponseMetadata(**meta_data),
            error=error,
        )