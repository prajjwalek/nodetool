from typing import Any
from nodetool.common.comfy_node import ComfyNode
import nodetool.nodes.comfy
import nodetool.nodes.comfy.advanced
import nodetool.nodes.comfy.advanced.conditioning
import nodetool.nodes.comfy.advanced.loaders
import nodetool.nodes.comfy.advanced.model
import nodetool.nodes.comfy.conditioning
import nodetool.nodes.comfy.controlnet
import nodetool.nodes.comfy.controlnet.faces_and_poses
import nodetool.nodes.comfy.controlnet.semantic_segmentation
import nodetool.nodes.comfy.controlnet.normal_and_depth
import nodetool.nodes.comfy.controlnet.others
import nodetool.nodes.comfy.controlnet.line_extractors
import nodetool.nodes.comfy.controlnet.t2i
import nodetool.nodes.comfy.flux
import nodetool.nodes.comfy.generate
import nodetool.nodes.comfy.image
import nodetool.nodes.comfy.image.animation
import nodetool.nodes.comfy.image.batch
import nodetool.nodes.comfy.image.preprocessors
import nodetool.nodes.comfy.image.transform
import nodetool.nodes.comfy.image.upscaling
import nodetool.nodes.comfy.ipadapter
import nodetool.nodes.comfy.latent
import nodetool.nodes.comfy.latent.advanced
import nodetool.nodes.comfy.latent.batch
import nodetool.nodes.comfy.latent.inpaint
import nodetool.nodes.comfy.latent.transform
import nodetool.nodes.comfy.loaders
import nodetool.nodes.comfy.mask
import nodetool.nodes.comfy.mask.compositing
import nodetool.nodes.comfy.sampling
import nodetool.nodes.comfy.sampling.samplers
import nodetool.nodes.comfy.sampling.schedulers
import nodetool.nodes.comfy.sampling.sigmas
import nodetool.nodes.comfy.sampling.guiders
import nodetool.nodes.comfy.sampling.noise


class PrimitiveNode(ComfyNode):
    _comfy_class = "PrimitiveNode"

    @classmethod
    def return_type(cls):
        return Any


class Note(ComfyNode):
    _comfy_class = "Note"
