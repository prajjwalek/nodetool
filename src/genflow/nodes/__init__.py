import os
from genflow.common.environment import Environment

# import genflow.nodes.genflow.database
# import genflow.nodes.genflow.dataframe
import genflow.nodes.genflow.dictionary
import genflow.nodes.genflow.image
import genflow.nodes.genflow.agents
import genflow.nodes.genflow.audio
import genflow.nodes.genflow.audio.analysis
import genflow.nodes.genflow.audio.conversion
import genflow.nodes.genflow.audio.transform
import genflow.nodes.genflow.constant
import genflow.nodes.genflow.http
import genflow.nodes.genflow.image.source
import genflow.nodes.genflow.image.transform
import genflow.nodes.genflow.image.generate
import genflow.nodes.genflow.input
import genflow.nodes.genflow.list
import genflow.nodes.genflow.loop
import genflow.nodes.genflow.math
import genflow.nodes.genflow.output
import genflow.nodes.genflow.tensor
import genflow.nodes.genflow.text
import genflow.nodes.genflow.text.extract
import genflow.nodes.genflow.text.generate
import genflow.nodes.genflow.vector
import genflow.nodes.genflow.text.vector
import genflow.nodes.genflow.video
from genflow.workflows.workflow_node import WorkflowNode


if Environment.get_comfy_folder():
    import genflow.nodes.comfy
    import genflow.nodes.comfy.advanced
    import genflow.nodes.comfy.advanced.conditioning
    import genflow.nodes.comfy.advanced.loaders
    import genflow.nodes.comfy.conditioning
    import genflow.nodes.comfy.controlnet
    import genflow.nodes.comfy.controlnet.faces_and_poses
    import genflow.nodes.comfy.controlnet.semantic_segmentation
    import genflow.nodes.comfy.controlnet.normal_and_depth
    import genflow.nodes.comfy.controlnet.others
    import genflow.nodes.comfy.controlnet.line_extractors
    import genflow.nodes.comfy.controlnet.t2i
    import genflow.nodes.comfy.generate
    import genflow.nodes.comfy.image
    import genflow.nodes.comfy.image.animation
    import genflow.nodes.comfy.image.batch
    import genflow.nodes.comfy.image.preprocessors
    import genflow.nodes.comfy.image.transform
    import genflow.nodes.comfy.image.upscaling
    import genflow.nodes.comfy.ipadapter
    import genflow.nodes.comfy.latent
    import genflow.nodes.comfy.latent.advanced
    import genflow.nodes.comfy.latent.batch
    import genflow.nodes.comfy.latent.inpaint
    import genflow.nodes.comfy.latent.transform
    import genflow.nodes.comfy.loaders
    import genflow.nodes.comfy.mask
    import genflow.nodes.comfy.mask.compositing
    import genflow.nodes.comfy.sampling
    import genflow.nodes.comfy.sampling.samplers
    import genflow.nodes.comfy.sampling.schedulers
    import genflow.nodes.comfy.sampling.sigmas

if Environment.get_huggingface_token():
    import genflow.nodes.huggingface.audio.generate
    import genflow.nodes.huggingface.image.generate
    import genflow.nodes.huggingface.image.classify
    import genflow.nodes.huggingface.text.classify
    import genflow.nodes.huggingface.text.summarize
    import genflow.nodes.huggingface.text.generate

if Environment.get_openai_api_key():
    import genflow.nodes.openai.audio
    import genflow.nodes.openai.image
    import genflow.nodes.openai.text

if Environment.get_replicate_api_token():
    import genflow.nodes.replicate.audio.generate
    import genflow.nodes.replicate.audio.transcribe
    import genflow.nodes.replicate.image.generate
    import genflow.nodes.replicate.text.generate
