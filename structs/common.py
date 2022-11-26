from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RequestType(str, Enum):
    GENERATE_REQUEST_TYPE = "generate"
    UPSCALE_REQUEST_TYPE = "upscale"
    VARIATION_REQUEST_TYPE = "generate variations of"
    REROLL_REQUEST_TYPE = "reroll"


class Metadata(BaseModel):
    author: str
    variation_ui_fields: bool
    simplified_interface: bool
    requested_at: datetime
    custom_metadata: dict
    metrics: dict = {}


class Params(BaseModel):
    prompt: str
    clip_skip: int
    cfg_scale: int
    negative_prompt: str
    steps: int
    aspect_ratio: str
    model: str
    hypernetwork: Optional[str]
    sampler: str
    grid: bool
    restore_faces: bool
    upscale: bool
    count: int
    seed: int
    variation_seed: int
    override_tensor: Optional[str]
    variation_strength: float
