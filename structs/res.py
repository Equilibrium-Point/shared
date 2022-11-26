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
    grid_image: Optional[str]
    tensors: list
    # TODO: where is the error created? We may need another class for this
    error: Optional[str] = None  

    @classmethod
    def from_request(cls, req: Request, info: dict, images: list, tensors: list, grid_image: Optional[str] = None, error: Optional[str] = None):
        """
        Create a response from a request and info dict

        Args:
            req (Request): a request
            info (dict): a dict containing info about the generation
        """
        fields = req.dict()

        params = fields.pop("params")
        params["seed"] = info.get("seed", 0)
        params["variation_seed"] = info.get("subseed", 0)

        meta_data = fields.pop("metadata")
        meta_data["token_count"] = info.get("token_count", 0)

        return cls(
            **fields,
            images=images,
            grid_image=grid_image,
            tensors=tensors,
            params=params,
            metadata=ResponseMetadata(**meta_data),
            error=error
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

        fields.pop("images")
        meta_data = fields.pop("metadata")
        meta_data["token_count"] = 0    # Not used in upscale request

        return cls(
            **fields,
            images=images,
            tensors=tensors,
            metadata=ResponseMetadata(**meta_data),
            error=error,
        )