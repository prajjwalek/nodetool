from enum import Enum
import io
import numpy as np
import PIL.Image
from nodetool.common.comfy_node import ComfyNode
from nodetool.metadata.types import (
    BoundingBox,
    DataframeRef,
    ImageRef,
    ImageSegmentationResult,
    ObjectDetectionResult,
)
from nodetool.nodes.huggingface.huggingface_pipeline import HuggingFacePipelineNode
from nodetool.providers.huggingface.huggingface_node import HuggingfaceNode
from nodetool.providers.huggingface.huggingface_node import progress_callback
from nodetool.workflows.processing_context import ProcessingContext
from pydantic import Field
from typing import Any
import asyncio
from nodetool.workflows.base_node import BaseNode
from nodetool.metadata.types import ImageRef
from nodetool.workflows.types import NodeProgress
import torch
from diffusers import AuraFlowPipeline  # type: ignore
from diffusers import AutoPipelineForText2Image, AutoPipelineForImage2Image  # type: ignore
from diffusers import (
    KandinskyV22Pipeline,  # type: ignore
    KandinskyV22PriorPipeline,  # type: ignore
    KandinskyV22Img2ImgPipeline,  # type: ignore
    KandinskyV22ControlnetPipeline,  # type: ignore
)
from diffusers import StableCascadeDecoderPipeline, StableCascadePriorPipeline  # type: ignore
from diffusers import StableDiffusion3ControlNetPipeline  # type: ignore
from diffusers.models import SD3ControlNetModel  # type: ignore
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel, AutoencoderKL  # type: ignore
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline  # type: ignore
from diffusers import StableDiffusionInpaintPipeline  # type: ignore
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline  # type: ignore
from diffusers import PixArtAlphaPipeline  # type: ignore
from diffusers.schedulers import (
    DPMSolverSDEScheduler,  # type: ignore
    EulerDiscreteScheduler,  # type: ignore
    LMSDiscreteScheduler,  # type: ignore
    DDIMScheduler,  # type: ignore
    DDPMScheduler,  # type: ignore
    HeunDiscreteScheduler,  # type: ignore
    DPMSolverMultistepScheduler,  # type: ignore
    DEISMultistepScheduler,  # type: ignore
    PNDMScheduler,  # type: ignore
    EulerAncestralDiscreteScheduler,  # type: ignore
    UniPCMultistepScheduler,  # type: ignore
    KDPM2DiscreteScheduler,  # type: ignore
    DPMSolverSinglestepScheduler,  # type: ignore
    KDPM2AncestralDiscreteScheduler,  # type: ignore
)
from diffusers import AutoPipelineForInpainting  # type: ignore
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel  # type: ignore
from diffusers import StableDiffusionControlNetInpaintPipeline  # type: ignore
from diffusers import StableDiffusionControlNetImg2ImgPipeline  # type: ignore


class ImageClassifier(HuggingFacePipelineNode):
    """
    Classifies images into predefined categories.
    image, classification, labeling, categorization

    Use cases:
    - Content moderation by detecting inappropriate images
    - Organizing photo libraries by automatically tagging images
    - Visual quality control in manufacturing to identify defective products
    - Medical image analysis to assist in diagnosing conditions
    """

    class ImageClassifierModelId(str, Enum):
        GOOGLE_VIT_BASE_PATCH16_224 = "google/vit-base-patch16-224"
        MICROSOFT_RESNET_50 = "microsoft/resnet-50"
        MICROSOFT_RESNET_18 = "microsoft/resnet-18"
        APPLE_MOBILEVIT_SMALL = "apple/mobilevit-small"
        NATERAW_VIT_AGE_CLASSIFIER = "nateraw/vit-age-classifier"
        FALCONSAI_NSFW_IMAGE_DETECTION = "Falconsai/nsfw_image_detection"
        MICROSOFT_BEIT_BASE_PATCH16_224_PT22K_FT22K = (
            "microsoft/beit-base-patch16-224-pt22k-ft22k"
        )
        TIMM_VIT_LARGE_PATCH14_CLIP_224_OPENAI_FT_IN12K_IN1K = (
            "timm/vit_large_patch14_clip_224.openai_ft_in12k_in1k"
        )
        ORGANIKA_SDXL_DETECTOR = "Organika/sdxl-detector"
        RIZVANDWIKI_GENDER_CLASSIFICATION_2 = "rizvandwiki/gender-classification-2"

    model: ImageClassifierModelId = Field(
        default=ImageClassifierModelId.GOOGLE_VIT_BASE_PATCH16_224,
        title="Model ID on Huggingface",
        description="The model ID to use for the classification",
    )
    inputs: ImageRef = Field(
        default=ImageRef(),
        title="Image",
        description="The input image to classify",
    )

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return "image-classification"

    async def get_inputs(self, context: ProcessingContext):
        return await context.image_to_pil(self.inputs)

    async def process_remote_result(
        self, context: ProcessingContext, result: Any
    ) -> dict[str, float]:
        return {item["label"]: item["score"] for item in result}

    async def process_local_result(
        self, context: ProcessingContext, result: Any
    ) -> dict[str, float]:
        return {item["label"]: item["score"] for item in result}

    async def process(self, context: ProcessingContext) -> dict[str, float]:
        return await super().process(context)


class ZeroShotImageClassifier(HuggingFacePipelineNode):
    """
    Classifies images into categories without the need for training data.
    image, classification, labeling, categorization

    Use cases:
    - Quickly categorize images without training data
    - Identify objects in images without predefined labels
    - Automate image tagging for large datasets
    """

    class ZeroShotImageClassifierModelId(str, Enum):
        OPENAI_CLIP_VIT_LARGE_PATCH14 = "openai/clip-vit-large-patch14"
        GOOGLE_SIGLIP_SO400M_PATCH14_384 = "google/siglip-so400m-patch14-384"
        OPENAI_CLIP_VIT_BASE_PATCH16 = "openai/clip-vit-base-patch16"
        OPENAI_CLIP_VIT_BASE_PATCH32 = "openai/clip-vit-base-patch32"
        PATRICKJOHNCYH_FASHION_CLIP = "patrickjohncyh/fashion-clip"
        LAION_CLIP_VIT_H_14_LAION2B_S32B_B79K = "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"

    model: ZeroShotImageClassifierModelId = Field(
        default=ZeroShotImageClassifierModelId.OPENAI_CLIP_VIT_LARGE_PATCH14,
        title="Model ID on Huggingface",
        description="The model ID to use for the classification",
    )
    inputs: ImageRef = Field(
        default=ImageRef(),
        title="Image",
        description="The input image to classify",
    )
    candidate_labels: str = Field(
        default="",
        title="Candidate Labels",
        description="The candidate labels to classify the image against, separated by commas",
    )

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return "zero-shot-image-classification"

    def get_params(self):
        return {
            "candidate_labels": self.candidate_labels.split(","),
        }

    async def get_inputs(self, context: ProcessingContext):
        return await context.image_to_pil(self.inputs)

    async def process_remote_result(
        self, context: ProcessingContext, result: Any
    ) -> dict[str, float]:
        return {item["label"]: item["score"] for item in result}

    async def process_local_result(
        self, context: ProcessingContext, result: Any
    ) -> dict[str, float]:
        return {item["label"]: item["score"] for item in result}

    async def process(self, context: ProcessingContext) -> dict[str, float]:
        return await super().process(context)


class StableDiffusionScheduler(str, Enum):
    DPMSolverSDEScheduler = "DPMSolverSDEScheduler"
    EulerDiscreteScheduler = "EulerDiscreteScheduler"
    LMSDiscreteScheduler = "LMSDiscreteScheduler"
    DDIMScheduler = "DDIMScheduler"
    DDPMScheduler = "DDPMScheduler"
    HeunDiscreteScheduler = "HeunDiscreteScheduler"
    DPMSolverMultistepScheduler = "DPMSolverMultistepScheduler"
    DEISMultistepScheduler = "DEISMultistepScheduler"
    PNDMScheduler = "PNDMScheduler"
    EulerAncestralDiscreteScheduler = "EulerAncestralDiscreteScheduler"
    UniPCMultistepScheduler = "UniPCMultistepScheduler"
    KDPM2DiscreteScheduler = "KDPM2DiscreteScheduler"
    DPMSolverSinglestepScheduler = "DPMSolverSinglestepScheduler"
    KDPM2AncestralDiscreteScheduler = "KDPM2AncestralDiscreteScheduler"


def get_scheduler_class(scheduler: StableDiffusionScheduler):
    if scheduler == StableDiffusionScheduler.DPMSolverSDEScheduler:
        return DPMSolverSDEScheduler
    elif scheduler == StableDiffusionScheduler.EulerDiscreteScheduler:
        return EulerDiscreteScheduler
    elif scheduler == StableDiffusionScheduler.LMSDiscreteScheduler:
        return LMSDiscreteScheduler
    elif scheduler == StableDiffusionScheduler.DDIMScheduler:
        return DDIMScheduler
    elif scheduler == StableDiffusionScheduler.DDPMScheduler:
        return DDPMScheduler
    elif scheduler == StableDiffusionScheduler.HeunDiscreteScheduler:
        return HeunDiscreteScheduler
    elif scheduler == StableDiffusionScheduler.DPMSolverMultistepScheduler:
        return DPMSolverMultistepScheduler
    elif scheduler == StableDiffusionScheduler.DEISMultistepScheduler:
        return DEISMultistepScheduler
    elif scheduler == StableDiffusionScheduler.PNDMScheduler:
        return PNDMScheduler
    elif scheduler == StableDiffusionScheduler.EulerAncestralDiscreteScheduler:
        return EulerAncestralDiscreteScheduler
    elif scheduler == StableDiffusionScheduler.UniPCMultistepScheduler:
        return UniPCMultistepScheduler
    elif scheduler == StableDiffusionScheduler.KDPM2DiscreteScheduler:
        return KDPM2DiscreteScheduler
    elif scheduler == StableDiffusionScheduler.DPMSolverSinglestepScheduler:
        return DPMSolverSinglestepScheduler
    elif scheduler == StableDiffusionScheduler.KDPM2AncestralDiscreteScheduler:
        return KDPM2AncestralDiscreteScheduler
    else:
        raise ValueError(f"Invalid scheduler: {scheduler}")


class VisualizeSegmentation(BaseNode):
    """
    Visualizes segmentation masks on images.
    """

    image: ImageRef = Field(
        default=ImageRef(),
        title="Image",
        description="The input image to visualize",
    )

    segments: list[ImageSegmentationResult] = Field(
        default={},
        title="Segmentation Masks",
        description="The segmentation masks to visualize",
    )

    async def process(self, context: ProcessingContext) -> ImageRef:
        import matplotlib.pyplot as plt

        image = await context.image_to_pil(self.image)

        color_map = plt.cm.get_cmap("rainbow")(np.linspace(0, 1, len(self.segments)))
        color_map = (color_map[:, :3] * 255).astype(np.uint8)
        mask = np.zeros((image.size[1], image.size[0], 3), dtype=np.uint8)

        # Fill the mask with segmentation results
        for i, segment in enumerate(self.segments):
            segment_mask = await context.image_to_numpy(segment.mask)
            # reduce channel dimension if present
            if segment_mask.ndim == 3:
                segment_mask = segment_mask[:, :, 0]
            color = color_map[i % len(color_map)]
            mask[segment_mask > 0] = color

        mask_image = PIL.Image.fromarray(mask)
        blended_image = PIL.Image.blend(image.convert("RGB"), mask_image, alpha=0.5)

        return await context.image_from_pil(blended_image)


class Segmentation(HuggingFacePipelineNode):
    """
    Performs semantic segmentation on images, identifying and labeling different regions.
    image, segmentation, object detection, scene parsing

    Use cases:
    - Segmenting objects in images
    - Segmenting facial features in images
    """

    class SegmentationModelId(str, Enum):
        NVIDIA_SEGFORMER_B3_FINETUNED_ADE_512_512 = (
            "nvidia/segformer-b3-finetuned-ade-512-512"
        )
        NVIDIA_SEGFORMER_B3_FINETUNED_COCO_512_512 = "mattmdjaga/segformer_b2_clothes"

    model: SegmentationModelId = Field(
        default=SegmentationModelId.NVIDIA_SEGFORMER_B3_FINETUNED_ADE_512_512,
        title="Model ID on Huggingface",
        description="The model ID to use for the segmentation",
    )
    image: ImageRef = Field(
        default=ImageRef(),
        title="Image",
        description="The input image to segment",
    )

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return "image-segmentation"

    async def get_inputs(self, context: ProcessingContext):
        return await context.image_to_pil(self.image)

    async def process_local_result(
        self, context: ProcessingContext, result: Any
    ) -> list[ImageSegmentationResult]:
        async def convert_output(item: dict[str, Any]):
            mask = await context.image_from_pil(item["mask"])
            return ImageSegmentationResult(mask=mask, label=item["label"])

        return await asyncio.gather(*[convert_output(item) for item in result])

    async def process(
        self, context: ProcessingContext
    ) -> list[ImageSegmentationResult]:
        return await super().process(context)


class FindSegment(BaseNode):
    """
    Extracts a specific segment from a list of segmentation masks.
    """

    segments: list[ImageSegmentationResult] = Field(
        default={},
        title="Segmentation Masks",
        description="The segmentation masks to search",
    )

    label: str = Field(
        default="",
        title="Label",
        description="The label of the segment to extract",
    )

    async def process(self, context: ProcessingContext) -> ImageRef:
        for segment in self.segments:
            if segment.label == self.label:
                return segment.mask
        raise ValueError(f"Segment not found: {self.label}")


class ObjectDetection(HuggingFacePipelineNode):
    """
    Detects and localizes objects in images.
    image, object detection, bounding boxes, huggingface

    Use cases:
    - Identify and count objects in images
    - Locate specific items in complex scenes
    - Assist in autonomous vehicle vision systems
    - Enhance security camera footage analysis
    """

    class ObjectDetectionModelId(str, Enum):
        FACEBOOK_DETR_RESNET_50 = "facebook/detr-resnet-50"

    model: ObjectDetectionModelId = Field(
        default=ObjectDetectionModelId.FACEBOOK_DETR_RESNET_50,
        title="Model ID on Huggingface",
        description="The model ID to use for object detection",
    )
    inputs: ImageRef = Field(
        default=ImageRef(),
        title="Inputs",
        description="The input image for object detection",
    )
    threshold: float = Field(
        default=0.9,
        title="Confidence Threshold",
        description="Minimum confidence score for detected objects",
    )
    top_k: int = Field(
        default=5,
        title="Top K",
        description="The number of top predictions to return",
    )

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return "object-detection"

    async def get_inputs(self, context: ProcessingContext):
        return await context.image_to_pil(self.inputs)

    def get_params(self):
        return {
            "threshold": self.threshold,
        }

    async def process_local_result(
        self, context: ProcessingContext, result: Any
    ) -> list[ObjectDetectionResult]:
        return [
            ObjectDetectionResult(
                label=item["label"],
                score=item["score"],
                box=BoundingBox(
                    xmin=item["box"]["xmin"],
                    ymin=item["box"]["ymin"],
                    xmax=item["box"]["xmax"],
                    ymax=item["box"]["ymax"],
                ),
            )
            for item in result
        ]

    async def process(self, context: ProcessingContext) -> list[ObjectDetectionResult]:
        return await super().process(context)


class VisualizeObjectDetection(BaseNode):
    """
    Visualizes object detection results on images.
    """

    image: ImageRef = Field(
        default=ImageRef(),
        title="Image",
        description="The input image to visualize",
    )

    objects: list[ObjectDetectionResult] = Field(
        default={},
        title="Detected Objects",
        description="The detected objects to visualize",
    )

    async def process(self, context: ProcessingContext) -> ImageRef:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import io

        image = await context.image_to_pil(self.image)

        # Get the size of the input image
        width, height = image.size

        # Create figure with the same size as the input image
        fig, ax = plt.subplots(
            figsize=(width / 100, height / 100)
        )  # Convert pixels to inches
        ax.imshow(image)

        for obj in self.objects:
            xmin = obj.box.xmin
            ymin = obj.box.ymin
            xmax = obj.box.xmax
            ymax = obj.box.ymax

            rect = patches.Rectangle(
                (xmin, ymin),
                xmax - xmin,
                ymax - ymin,
                linewidth=1,
                edgecolor="r",
                facecolor="none",
            )
            ax.add_patch(rect)
            ax.text(
                xmin,
                ymin,
                f"{obj.label} ({obj.score:.2f})",
                color="r",
                fontsize=8,
                backgroundcolor="w",
            )

        ax.axis("off")

        # Remove padding around the image
        plt.tight_layout(pad=0)

        if fig is None:
            raise ValueError("Invalid plot")
        img_bytes = io.BytesIO()
        fig.savefig(img_bytes, format="png", dpi=100, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        return await context.image_from_bytes(img_bytes.getvalue())


class ZeroShotObjectDetection(HuggingFacePipelineNode):
    """
    Detects objects in images without the need for training data.
    image, object detection, bounding boxes, zero-shot

    Use cases:
    - Quickly detect objects in images without training data
    - Identify objects in images without predefined labels
    - Automate object detection for large datasets
    """

    class ZeroShotObjectDetectionModelId(str, Enum):
        GOOGLE_OWL_VIT_BASE_PATCH32 = "google/owlvit-base-patch32"
        GOOGLE_OWL_VIT_LARGE_PATCH14 = "google/owlvit-large-patch14"
        GOOGLE_OWL_VIT_BASE_PATCH16 = "google/owlvit-base-patch16"
        GOOGLE_OWL_V2_BASE_PATCH16 = "google/owlv2-base-patch16"
        GOOGLE_OWL_VIT_BASE_PATCH16_ENSEMBLE = "google/owlv2-base-patch16-ensemble"
        IDEA_RESEARCH_GROUNDING_DINO_TINY = "IDEA-Research/grounding-dino-tiny"

    model: ZeroShotObjectDetectionModelId = Field(
        default=ZeroShotObjectDetectionModelId.GOOGLE_OWL_V2_BASE_PATCH16,
        title="Model ID on Huggingface",
        description="The model ID to use for object detection",
    )

    inputs: ImageRef = Field(
        default=ImageRef(),
        title="Inputs",
        description="The input image for object detection",
    )

    threshold: float = Field(
        default=0.1,
        title="Confidence Threshold",
        description="Minimum confidence score for detected objects",
    )

    top_k: int = Field(
        default=5,
        title="Top K",
        description="The number of top predictions to return",
    )

    candidate_labels: str = Field(
        default="",
        title="Candidate Labels",
        description="The candidate labels to detect in the image, separated by commas",
    )

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return "zero-shot-object-detection"

    def get_params(self):
        return {
            "candidate_labels": self.candidate_labels.split(","),
            "threshold": self.threshold,
        }

    async def get_inputs(self, context: ProcessingContext):
        return await context.image_to_pil(self.inputs)

    async def process_remote_result(
        self, context: ProcessingContext, result: Any
    ) -> DataframeRef:
        return await self.process_local_result(context, result)

    async def process_local_result(
        self, context: ProcessingContext, result: Any
    ) -> list[ObjectDetectionResult]:
        return [
            ObjectDetectionResult(
                label=item["label"],
                score=item["score"],
                box=BoundingBox(
                    xmin=item["box"]["xmin"],
                    ymin=item["box"]["ymin"],
                    xmax=item["box"]["xmax"],
                    ymax=item["box"]["ymax"],
                ),
            )
            for item in result
        ]

    async def process(self, context: ProcessingContext) -> list[ObjectDetectionResult]:
        return await super().process(context)


class DepthEstimation(HuggingFacePipelineNode):
    """
    Estimates depth from a single image.
    image, depth estimation, 3D, huggingface

    Use cases:
    - Generate depth maps for 3D modeling
    - Assist in augmented reality applications
    - Enhance computer vision systems for robotics
    - Improve scene understanding in autonomous vehicles
    """

    class DepthEstimationModelId(str, Enum):
        DEPTH_ANYTHING = "LiheYoung/depth-anything-base-hf"
        DEPTH_ANYTHING_V2_SMALL = "depth-anything/Depth-Anything-V2-Small"
        INTEL_DPT_LARGE = "Intel/dpt-large"

    model: DepthEstimationModelId = Field(
        default=DepthEstimationModelId.DEPTH_ANYTHING,
        title="Model ID on Huggingface",
        description="The model ID to use for depth estimation",
    )
    inputs: ImageRef = Field(
        default=ImageRef(),
        title="Image",
        description="The input image for depth estimation",
    )

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return "depth-estimation"

    async def get_inputs(self, context: ProcessingContext):
        return await context.image_to_pil(self.inputs)

    async def process_remote_result(
        self, context: ProcessingContext, result: Any
    ) -> ImageRef:
        depth_map = await context.image_from_base64(result["depth"])
        return depth_map

    async def process_local_result(
        self, context: ProcessingContext, result: Any
    ) -> ImageRef:
        depth_ref = await context.image_from_pil(result["depth"])
        return depth_ref

    async def process(self, context: ProcessingContext) -> ImageRef:
        return await super().process(context)


class BaseImageToImage(HuggingFacePipelineNode):
    """
    Base class for image-to-image transformation tasks.
    image, transformation, generation, huggingface
    """

    @classmethod
    def is_visible(cls) -> bool:
        return cls is not BaseImageToImage

    inputs: ImageRef = Field(
        default=ImageRef(),
        title="Input Image",
        description="The input image to transform",
    )
    prompt: str = Field(
        default="",
        title="Prompt",
        description="The text prompt to guide the image transformation (if applicable)",
    )

    @property
    def pipeline_task(self) -> str:
        return "image-to-image"

    async def get_inputs(self, context: ProcessingContext):
        return await context.image_to_pil(self.inputs)

    async def process_remote_result(
        self, context: ProcessingContext, result: Any
    ) -> ImageRef:
        return await context.image_from_base64(result)

    async def process_local_result(
        self, context: ProcessingContext, result: Any
    ) -> ImageRef:
        return await context.image_from_pil(result)


class Swin2SR(BaseImageToImage):
    """
    Performs image super-resolution using the Swin2SR model.
    image, super-resolution, enhancement, huggingface

    Use cases:
    - Enhance low-resolution images
    - Improve image quality for printing or display
    - Upscale images for better detail
    """

    def get_model_id(self):
        return "caidas/swin2SR-classical-sr-x2-64"

    def get_params(self):
        return {}


class RealESRGAN(BaseImageToImage):
    """
    Performs image super-resolution using the Real-ESRGAN model.
    image, super-resolution, enhancement, huggingface

    Use cases:
    - Enhance low-resolution images
    - Restore details in blurry or pixelated images
    - Improve visual quality of old or compressed images
    """

    def get_model_id(self):
        return "qualcomm/Real-ESRGAN-x4plus"

    def get_params(self):
        return {}


class InstructPix2Pix(BaseImageToImage):
    """
    Performs image editing based on text instructions using the InstructPix2Pix model.
    image, editing, transformation, huggingface

    Use cases:
    - Apply specific edits to images based on text instructions
    - Modify image content or style guided by text prompts
    - Create variations of existing images with controlled changes
    """

    prompt: str = Field(
        default="Remove the background.",
        description="The text prompt to guide the image transformation.",
    )
    negative_prompt: str = Field(
        default="",
        description="The negative text prompt to avoid in the transformation.",
    )
    num_inference_steps: int = Field(
        default=50, description="The number of denoising steps.", ge=1, le=100
    )
    guidance_scale: float = Field(
        default=7.0, description="The guidance scale for the transformation.", ge=1.0
    )
    image_guidance_scale: float = Field(
        default=7.0,
        description="The image guidance scale for the transformation.",
        ge=1.0,
    )

    def get_model_id(self):
        return "timbrooks/instruct-pix2pix"

    def get_params(self):
        return {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "num_inference_steps": self.num_inference_steps,
            "guidance_scale": self.guidance_scale,
            "image_guidance_scale": self.image_guidance_scale,
        }


class AuraFlow(BaseNode):
    """
    Generates images using the AuraFlow pipeline.
    image, generation, AI, text-to-image

    Use cases:
    - Create unique images from text descriptions
    - Generate illustrations for creative projects
    - Produce visual content for digital media
    """

    prompt: str = Field(
        default="A cat holding a sign that says hello world",
        description="A text prompt describing the desired image.",
    )
    negative_prompt: str = Field(
        default="", description="A text prompt describing what to avoid in the image."
    )
    guidance_scale: float = Field(
        default=7.0, description="The guidance scale for the transformation.", ge=1.0
    )
    num_inference_steps: int = Field(
        default=25, description="The number of denoising steps.", ge=1, le=100
    )
    width: int = Field(
        default=768, description="The width of the generated image.", ge=128, le=1024
    )
    height: int = Field(
        default=768, description="The height of the generated image.", ge=128, le=1024
    )
    seed: int = Field(
        default=-1,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )

    _pipeline: AuraFlowPipeline | None = None

    async def initialize(self, context: ProcessingContext):
        self._pipeline = AuraFlowPipeline.from_pretrained(
            "fal/AuraFlow", torch_dtype=torch.float16
        )  # type: ignore

    async def move_to_device(self, device: str):
        pass

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipeline is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility if a seed is provided
        generator = None
        if self.seed != -1:
            generator = torch.Generator(device=self._pipeline.device).manual_seed(
                self.seed
            )

        self._pipeline.enable_sequential_cpu_offload()

        output = self._pipeline(
            self.prompt,
            negative_prompt=self.negative_prompt,
            guidance_scale=self.guidance_scale,
            num_inference_steps=self.num_inference_steps,
            width=self.width,
            height=self.height,
            generator=generator,
        )
        image = output.images[0]  # type: ignore

        return await context.image_from_pil(image)


class PixArtAlpha(BaseNode):
    """
    Generates images from text prompts using the PixArt-Alpha model.
    image, generation, AI, text-to-image

    Use cases:
    - Create unique images from detailed text descriptions
    - Generate concept art for creative projects
    - Produce visual content for digital media and marketing
    - Explore AI-generated imagery for artistic inspiration
    """

    prompt: str = Field(
        default="An astronaut riding a green horse",
        description="A text prompt describing the desired image.",
    )
    num_inference_steps: int = Field(
        default=50,
        description="The number of denoising steps.",
        ge=1,
        le=100,
    )
    guidance_scale: float = Field(
        default=7.5,
        description="The scale for classifier-free guidance.",
        ge=1.0,
        le=20.0,
    )
    width: int = Field(
        default=768,
        description="The width of the generated image.",
        ge=128,
        le=1024,
    )
    height: int = Field(
        default=768,
        description="The height of the generated image.",
        ge=128,
        le=1024,
    )
    seed: int = Field(
        default=-1,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )

    _pipeline: PixArtAlphaPipeline | None = None

    async def initialize(self, context: ProcessingContext):
        self._pipeline = PixArtAlphaPipeline.from_pretrained(
            "PixArt-alpha/PixArt-XL-2-1024-MS",
            torch_dtype=torch.float16,
        )  # type: ignore

    async def move_to_device(self, device: str):
        if self._pipeline is not None:
            self._pipeline.to(device)

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipeline is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = None
        if self.seed != -1:
            generator = torch.Generator(device=self._pipeline.device).manual_seed(
                self.seed
            )

        def callback(step: int, timestep: int, latents: torch.FloatTensor) -> None:
            context.post_message(
                NodeProgress(
                    node_id=self.id,
                    progress=step,
                    total=self.num_inference_steps,
                )
            )

        # Generate the image
        output = self._pipeline(
            prompt=self.prompt,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            generator=generator,
            callback=callback,  # type: ignore
            callback_steps=1,
        )

        image = output.images[0]  # type: ignore

        return await context.image_from_pil(image)


class Kandinsky2(BaseNode):
    """
    Generates images using the Kandinsky 2.2 model from text prompts.
    image, generation, AI, text-to-image

    Use cases:
    - Create high-quality images from text descriptions
    - Generate detailed illustrations for creative projects
    - Produce visual content for digital media and art
    - Explore AI-generated imagery for concept development
    """

    @classmethod
    def get_title(cls) -> str:
        return "Kandinsky 2.2"

    prompt: str = Field(
        default="A photograph of the inside of a subway train. There are raccoons sitting on the seats. One of them is reading a newspaper. The window shows the city in the background.",
        description="A text prompt describing the desired image.",
    )
    negative_prompt: str = Field(
        default="", description="A text prompt describing what to avoid in the image."
    )
    num_inference_steps: int = Field(
        default=50, description="The number of denoising steps.", ge=1, le=100
    )
    width: int = Field(
        default=768, description="The width of the generated image.", ge=128, le=1024
    )
    height: int = Field(
        default=768, description="The height of the generated image.", ge=128, le=1024
    )
    seed: int = Field(
        default=-1,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )

    _prior_pipeline: KandinskyV22PriorPipeline | None = None
    _pipeline: KandinskyV22Pipeline | None = None

    async def initialize(self, context: ProcessingContext):
        self._pipeline = KandinskyV22Pipeline.from_pretrained(
            "kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float16
        )  # type: ignore

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._prior_pipeline is None or self._pipeline is None:
            raise ValueError("Pipelines not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        # Enable sequential CPU offload for memory efficiency
        self._pipeline.enable_sequential_cpu_offload()

        # Generate image embeddings
        prior_output = self._prior_pipeline(
            self.prompt, negative_prompt=self.negative_prompt, generator=generator
        )
        image_emb, negative_image_emb = prior_output.to_tuple()  # type: ignore

        output = self._pipeline(
            image_embeds=image_emb,
            negative_image_embeds=negative_image_emb,
            height=self.height,
            width=self.width,
            num_inference_steps=self.num_inference_steps,
            generator=generator,
            callback=progress_callback(self.id, self.num_inference_steps, context),
            callback_steps=1,
        )

        image = output.images[0]  # type: ignore

        return await context.image_from_pil(image)


class Kandinsky2Img2Img(BaseNode):
    """
    Transforms existing images based on text prompts using the Kandinsky 2.2 model.
    image, generation, AI, image-to-image

    Use cases:
    - Transform existing images based on text prompts
    - Apply specific styles or concepts to existing images
    - Modify photographs or artworks with AI-generated elements
    - Create variations of existing visual content
    """

    @classmethod
    def get_title(cls) -> str:
        return "Kandinsky 2.2 Image-to-Image"

    prompt: str = Field(
        default="A photograph of the inside of a subway train. There are raccoons sitting on the seats. One of them is reading a newspaper. The window shows the city in the background.",
        description="A text prompt describing the desired image transformation.",
    )
    negative_prompt: str = Field(
        default="", description="A text prompt describing what to avoid in the image."
    )
    num_inference_steps: int = Field(
        default=50, description="The number of denoising steps.", ge=1, le=100
    )
    strength: float = Field(
        default=0.5,
        description="The strength of the transformation. Use a value between 0.0 and 1.0.",
        ge=0.0,
        le=1.0,
    )
    image: ImageRef = Field(
        default=ImageRef(),
        title="Input Image",
        description="The input image to transform",
    )
    seed: int = Field(
        default=-1,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )

    _prior_pipeline: KandinskyV22PriorPipeline | None = None
    _pipeline: KandinskyV22Img2ImgPipeline | None = None

    async def initialize(self, context: ProcessingContext):
        self._prior_pipeline = KandinskyV22PriorPipeline.from_pretrained(
            "kandinsky-community/kandinsky-2-2-prior", torch_dtype=torch.float16
        )  # type: ignore
        self._pipeline = KandinskyV22Img2ImgPipeline.from_pretrained(
            "kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float16
        )  # type: ignore

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._prior_pipeline is None or self._pipeline is None:
            raise ValueError("Pipelines not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        # Enable sequential CPU offload for memory efficiency
        self._prior_pipeline.enable_sequential_cpu_offload()
        self._pipeline.enable_sequential_cpu_offload()

        # Generate image embeddings
        prior_output = self._prior_pipeline(
            self.prompt, negative_prompt=self.negative_prompt, generator=generator
        )
        image_emb, negative_image_emb = prior_output.to_tuple()  # type: ignore

        input_image = await context.image_to_pil(self.image)
        output = self._pipeline(
            image=input_image,
            image_embeds=image_emb,
            negative_image_embeds=negative_image_emb,
            num_inference_steps=self.num_inference_steps,
            generator=generator,
            callback=progress_callback(self.id, self.num_inference_steps, context),
            callback_steps=1,
        )

        image = output.images[0]  # type: ignore

        return await context.image_from_pil(image)


def make_hint(image: PIL.Image.Image) -> torch.Tensor:
    np_array = np.array(image)
    detected_map = torch.from_numpy(np_array).float() / 255.0
    hint = detected_map.permute(2, 0, 1)
    return hint[:3, :, :].unsqueeze(0)


class Kandinsky2ControlNet(BaseNode):
    """
    Transforms existing images based on text prompts and control images using the Kandinsky 2.2 model with ControlNet.
    image, generation, AI, image-to-image, controlnet

    Use cases:
    - Transform existing images based on text prompts with precise control
    - Apply specific styles or concepts to existing images guided by control images
    - Modify photographs or artworks with AI-generated elements while maintaining specific structures
    - Create variations of existing visual content with controlled transformations
    """

    @classmethod
    def get_title(cls) -> str:
        return "Kandinsky 2.2 with ControlNet"

    prompt: str = Field(
        default="A photograph of the inside of a subway train. There are raccoons sitting on the seats. One of them is reading a newspaper. The window shows the city in the background.",
        description="The prompt to guide the image generation.",
    )
    negative_prompt: str = Field(
        default="", description="The prompt not to guide the image generation."
    )
    hint: ImageRef = Field(
        default=ImageRef(),
        title="Control Image",
        description="The controlnet condition image.",
    )
    height: int = Field(
        default=512,
        description="The height in pixels of the generated image.",
        ge=64,
        le=2048,
    )
    width: int = Field(
        default=512,
        description="The width in pixels of the generated image.",
        ge=64,
        le=2048,
    )
    num_inference_steps: int = Field(
        default=30, description="The number of denoising steps.", ge=1, le=100
    )
    guidance_scale: float = Field(
        default=4.0,
        description="Guidance scale as defined in Classifier-Free Diffusion Guidance.",
        ge=1.0,
        le=20.0,
    )
    seed: int = Field(
        default=-1,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )
    output_type: str = Field(
        default="pil",
        description="The output format of the generated image.",
    )

    _prior_pipeline: KandinskyV22PriorPipeline | None = None
    _pipeline: KandinskyV22ControlnetPipeline | None = None

    async def initialize(self, context: ProcessingContext):
        self._prior_pipeline = KandinskyV22PriorPipeline.from_pretrained(
            "kandinsky-community/kandinsky-2-2-prior", torch_dtype=torch.float16
        )  # type: ignore
        self._pipeline = KandinskyV22ControlnetPipeline.from_pretrained(
            "kandinsky-community/kandinsky-2-2-controlnet-depth",
            torch_dtype=torch.float16,
        )  # type: ignore

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._prior_pipeline is None or self._pipeline is None:
            raise ValueError("Pipelines not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        # Enable sequential CPU offload for memory efficiency
        self._prior_pipeline.enable_sequential_cpu_offload()
        self._pipeline.enable_sequential_cpu_offload()

        # Generate image embeddings
        prior_output = self._prior_pipeline(
            self.prompt, negative_prompt=self.negative_prompt, generator=generator
        )
        image_emb, negative_image_emb = prior_output.to_tuple()  # type: ignore

        # Prepare the control image (hint)
        hint = await context.image_to_pil(self.hint)
        hint = hint.resize((self.width, self.height))

        output = self._pipeline(
            hint=make_hint(hint),
            image_embeds=image_emb,
            negative_image_embeds=negative_image_emb,
            height=self.height,
            width=self.width,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            generator=generator,
            output_type="pil",
            callback=progress_callback(self.id, self.num_inference_steps, context),  # type: ignore
            callback_steps=1,
        )

        return await context.image_from_pil(output.images[0])  # type: ignore


class Kandinsky3(BaseNode):
    """
    Generates images using the Kandinsky-3 model from text prompts.
    image, generation, AI, text-to-image

    Use cases:
    - Create detailed images from text descriptions
    - Generate unique illustrations for creative projects
    - Produce visual content for digital media and art
    - Explore AI-generated imagery for concept development
    """

    prompt: str = Field(
        default="A photograph of the inside of a subway train. There are raccoons sitting on the seats. One of them is reading a newspaper. The window shows the city in the background.",
        description="A text prompt describing the desired image.",
    )
    num_inference_steps: int = Field(
        default=25, description="The number of denoising steps.", ge=1, le=100
    )
    width: int = Field(
        default=512, description="The width of the generated image.", ge=64, le=2048
    )
    height: int = Field(
        default=512, description="The height of the generated image.", ge=64, le=2048
    )
    seed: int = Field(
        default=0,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )

    _pipeline: AutoPipelineForText2Image | None = None

    async def initialize(self, context: ProcessingContext):
        self._pipeline = AutoPipelineForText2Image.from_pretrained(
            "kandinsky-community/kandinsky-3",
            variant="fp16",
            torch_dtype=torch.float16,
        )

    async def move_to_device(self, device: str):
        # Commented out as in the original class
        # if self._pipeline is not None:
        #     self._pipeline.to(device)
        pass

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipeline is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        self._pipeline.enable_sequential_cpu_offload()

        output = self._pipeline(
            prompt=self.prompt,
            num_inference_steps=self.num_inference_steps,
            generator=generator,
            width=self.width,
            height=self.height,
            callback=progress_callback(self.id, self.num_inference_steps, context),
            callback_steps=1,
        )  # type: ignore

        image = output.images[0]

        return await context.image_from_pil(image)


class Kandinsky3Img2Img(BaseNode):
    """
    Transforms existing images using the Kandinsky-3 model based on text prompts.
    image, generation, AI, image-to-image

    Use cases:
    - Modify existing images based on text descriptions
    - Apply specific styles or concepts to photographs or artwork
    - Create variations of existing visual content
    - Blend AI-generated elements with existing images
    """

    prompt: str = Field(
        default="A photograph of the inside of a subway train. There are raccoons sitting on the seats. One of them is reading a newspaper. The window shows the city in the background.",
        description="A text prompt describing the desired image transformation.",
    )
    num_inference_steps: int = Field(
        default=25, description="The number of denoising steps.", ge=1, le=100
    )
    strength: float = Field(
        default=0.5,
        description="The strength of the transformation. Use a value between 0.0 and 1.0.",
        ge=0.0,
        le=1.0,
    )
    image: ImageRef = Field(
        default=ImageRef(),
        title="Input Image",
        description="The input image to transform",
    )
    seed: int = Field(
        default=0,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )

    _pipeline: AutoPipelineForImage2Image | None = None

    async def initialize(self, context: ProcessingContext):
        self._pipeline = AutoPipelineForImage2Image.from_pretrained(
            "kandinsky-community/kandinsky-3",
            variant="fp16",
            torch_dtype=torch.float16,
        )

    async def move_to_device(self, device: str):
        pass

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipeline is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        self._pipeline.enable_sequential_cpu_offload()

        input_image = await context.image_to_pil(self.image)
        output = self._pipeline(
            prompt=self.prompt,
            num_inference_steps=self.num_inference_steps,
            generator=generator,
            image=input_image,
            width=input_image.width,
            height=input_image.height,
            callback=progress_callback(self.id, self.num_inference_steps, context),
            callback_steps=1,
        )  # type: ignore

        image = output.images[0]

        return await context.image_from_pil(image)


class StableCascade(BaseNode):
    """
    Generates images using the Stable Cascade model, which involves a two-stage process with a prior and a decoder.
    image, generation, AI, text-to-image

    Use cases:
    - Create high-quality images from text descriptions
    - Generate detailed illustrations for creative projects
    - Produce visual content for digital media and art
    """

    prompt: str = Field(
        default="an image of a shiba inu, donning a spacesuit and helmet",
        description="A text prompt describing the desired image.",
    )
    negative_prompt: str = Field(
        default="", description="A text prompt describing what to avoid in the image."
    )
    width: int = Field(
        default=1024, description="The width of the generated image.", ge=256, le=2048
    )
    height: int = Field(
        default=1024, description="The height of the generated image.", ge=256, le=2048
    )
    prior_num_inference_steps: int = Field(
        default=20,
        description="The number of denoising steps for the prior.",
        ge=1,
        le=100,
    )
    decoder_num_inference_steps: int = Field(
        default=10,
        description="The number of denoising steps for the decoder.",
        ge=1,
        le=100,
    )
    prior_guidance_scale: float = Field(
        default=4.0, description="Guidance scale for the prior.", ge=0.0, le=20.0
    )
    decoder_guidance_scale: float = Field(
        default=0.0, description="Guidance scale for the decoder.", ge=0.0, le=20.0
    )
    seed: int = Field(
        default=-1,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )

    _prior_pipeline: StableCascadePriorPipeline | None = None
    _decoder_pipeline: StableCascadeDecoderPipeline | None = None

    async def initialize(self, context: ProcessingContext):
        self._prior_pipeline = StableCascadePriorPipeline.from_pretrained(
            "stabilityai/stable-cascade-prior",
            variant="bf16",
            torch_dtype=torch.bfloat16,
        )  # type: ignore
        self._decoder_pipeline = StableCascadeDecoderPipeline.from_pretrained(
            "stabilityai/stable-cascade", variant="bf16", torch_dtype=torch.float16
        )  # type: ignore

    async def move_to_device(self, device: str):
        # Commented out as we're using CPU offload
        pass

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._prior_pipeline is None or self._decoder_pipeline is None:
            raise ValueError("Pipelines not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        # Enable CPU offload for memory efficiency
        self._prior_pipeline.enable_model_cpu_offload()
        self._decoder_pipeline.enable_model_cpu_offload()

        # Generate image embeddings with the prior
        prior_output = self._prior_pipeline(
            prompt=self.prompt,
            height=self.height,
            width=self.width,
            negative_prompt=self.negative_prompt,
            guidance_scale=self.prior_guidance_scale,
            num_images_per_prompt=1,
            num_inference_steps=self.prior_num_inference_steps,
            generator=generator,
        )

        # Generate the final image with the decoder
        decoder_output = self._decoder_pipeline(
            image_embeddings=prior_output.image_embeddings.to(torch.float16),  # type: ignore
            prompt=self.prompt,
            negative_prompt=self.negative_prompt,
            guidance_scale=self.decoder_guidance_scale,
            output_type="pil",
            num_inference_steps=self.decoder_num_inference_steps,
            generator=generator,
        ).images[  # type: ignore
            0
        ]

        return await context.image_from_pil(decoder_output)


class StableDiffusionModelId(str, Enum):
    SD_V1_5 = "runwayml/stable-diffusion-v1-5"
    REALISTIC_VISION = "SG161222/Realistic_Vision_V6.0_B1_noVAE"
    DREAMLIKE_V1 = "dreamlike-art/dreamlike-diffusion-1.0"
    INPAINTING = "runwayml/stable-diffusion-inpainting"


class IPAdapter_SD15_Model(str, Enum):
    NONE = ""
    IP_ADAPTER = "ip-adapter_sd15.safetensors"
    IP_ADAPTER_LIGHT = "ip-adapter_sd15_light.safetensors"
    IP_ADAPTER_PLUS = "ip-adapter-plus_sd15.bin"
    IP_ADAPTER_PLUS_FACE = "ip-adapter-plus-face_sd15.safetensors"
    IP_ADAPTER_FULL_FACE = "ip-adapter-full-face_sd15.safetensors"


class StableDiffusionScheduler(str, Enum):
    DDIMScheduler = "DDIMScheduler"
    PNDMScheduler = "PNDMScheduler"
    LMSDiscreteScheduler = "LMSDiscreteScheduler"
    EulerDiscreteScheduler = "EulerDiscreteScheduler"
    EulerAncestralDiscreteScheduler = "EulerAncestralDiscreteScheduler"
    DPMSolverMultistepScheduler = "DPMSolverMultistepScheduler"
    HeunDiscreteScheduler = "HeunDiscreteScheduler"


class StableDiffusionBaseNode(BaseNode):
    prompt: str = Field(default="", description="The prompt for image generation.")
    negative_prompt: str = Field(
        default="",
        description="The negative prompt to guide what should not appear in the generated image.",
    )
    seed: int = Field(
        default=-1,
        ge=-1,
        le=2**32 - 1,
        description="Seed for the random number generator. Use -1 for a random seed.",
    )
    num_inference_steps: int = Field(
        default=25, ge=1, le=100, description="Number of denoising steps."
    )
    guidance_scale: float = Field(
        default=7.5, ge=1.0, le=20.0, description="Guidance scale for generation."
    )
    scheduler: StableDiffusionScheduler = Field(
        default=StableDiffusionScheduler.HeunDiscreteScheduler,
        description="The scheduler to use for the diffusion process.",
    )
    ip_adapter_model: IPAdapter_SD15_Model = Field(
        default=IPAdapter_SD15_Model.NONE,
        description="The IP adapter model to use for image processing",
    )
    ip_adapter_image: ImageRef = Field(
        default=ImageRef(),
        description="When provided the image will be fed into the IP adapter",
    )
    ip_adapter_scale: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Strength of the IP adapter image",
    )

    _pipeline: Any = None

    async def initialize(self, context: ProcessingContext):
        raise NotImplementedError("Subclasses must implement this method")

    def _set_scheduler(self, scheduler_type: StableDiffusionScheduler):
        scheduler_class = get_scheduler_class(scheduler_type)
        self._pipeline.scheduler = scheduler_class.from_config(
            self._pipeline.scheduler.config
        )

    async def move_to_device(self, device: str):
        if self._pipeline is not None:
            self._pipeline.to(device)

    def _setup_generator(self):
        generator = torch.Generator(device="cuda")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)
        return generator

    async def _setup_ip_adapter(self, context: ProcessingContext):
        self._pipeline.set_ip_adapter_scale(self.ip_adapter_scale)
        if self.ip_adapter_model != IPAdapter_SD15_Model.NONE:
            assert not self.ip_adapter_image.is_empty()
            return await context.image_to_pil(self.ip_adapter_image)
        return None

    def progress_callback(self, context: ProcessingContext):
        def callback(step: int, timestep: int, latents: torch.FloatTensor) -> None:
            context.post_message(
                NodeProgress(
                    node_id=self.id,
                    progress=step,
                    total=self.num_inference_steps,
                )
            )

        return callback

    async def process(self, context: ProcessingContext) -> ImageRef:
        raise NotImplementedError("Subclasses must implement this method")


class StableDiffusion(StableDiffusionBaseNode):
    """
    Generates images from text prompts using Stable Diffusion.
    image, generation, AI, text-to-image

    Use cases:
    - Creating custom illustrations for various projects
    - Generating concept art for creative endeavors
    - Producing unique visual content for marketing materials
    - Exploring AI-generated art for personal or professional use
    """

    model: StableDiffusionModelId = Field(
        default=StableDiffusionModelId.SD_V1_5,
        description="The Stable Diffusion model to use for generation.",
    )

    width: int = Field(
        default=512, ge=256, le=1024, description="Width of the generated image."
    )
    height: int = Field(
        default=512, ge=256, le=1024, description="Height of the generated image"
    )

    @classmethod
    def get_title(cls):
        return "Stable Diffusion"

    async def initialize(self, context: ProcessingContext):
        if self._pipe is None:
            self._pipe = StableDiffusionPipeline.from_pretrained(
                self.model.value, torch_dtype=torch.float16, safety_checker=None
            )
            self._set_scheduler(self.scheduler)
            if self.ip_adapter_model != IPAdapter_SD15_Model.NONE:
                self._pipe.load_ip_adapter(
                    "h94/IP-Adapter",
                    subfolder="models",
                    weight_name=self.ip_adapter_model,
                )

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipe is None:
            raise ValueError("Pipeline not initialized")

        generator = self._setup_generator()
        ip_adapter_image = await self._setup_ip_adapter(context)

        image = self._pipe(
            prompt=self.prompt,
            negative_prompt=self.negative_prompt,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            width=self.width,
            height=self.height,
            generator=generator,
            ip_adapter_image=ip_adapter_image,
            callback=self.progress_callback(context),
            callback_steps=1,
        ).images[0]

        return await context.image_from_pil(image)


class StableDiffusionControlNetModel(str, Enum):
    CANNY = "lllyasviel/sd-controlnet-canny"
    DEPTH = "lllyasviel/sd-controlnet-depth"
    POSE = "lllyasviel/sd-controlnet-openpose"


class StableDiffusionControlNetNode(StableDiffusionBaseNode):
    """
    Generates images using Stable Diffusion with ControlNet guidance.
    image, generation, AI, text-to-image, controlnet

    Use cases:
    - Generate images with precise control over composition and structure
    - Create variations of existing images while maintaining specific features
    - Artistic image generation with guided outputs
    """

    model: StableDiffusionModelId = Field(
        default=StableDiffusionModelId.SD_V1_5,
        description="The Stable Diffusion model to use for generation.",
    )

    controlnet: StableDiffusionControlNetModel = Field(
        default=StableDiffusionControlNetModel.CANNY,
        description="The ControlNet model to use for guidance.",
    )
    control_image: ImageRef = Field(
        default=ImageRef(),
        description="The control image to guide the generation process.",
    )
    controlnet_conditioning_scale: float = Field(
        default=1.0,
        description="The scale for ControlNet conditioning.",
        ge=0.0,
        le=2.0,
    )

    _pipeline: StableDiffusionControlNetPipeline | None = None

    @classmethod
    def get_title(cls):
        return "Stable Diffusion ControlNet"

    async def initialize(self, context: ProcessingContext):
        controlnet = ControlNetModel.from_pretrained(
            self.controlnet.value, torch_dtype=torch.float16
        )
        self._pipeline = StableDiffusionControlNetPipeline.from_pretrained(
            self.model.value, controlnet=controlnet, torch_dtype=torch.float16
        )  # type: ignore
        self._pipeline.enable_model_cpu_offload()  # type: ignore

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipeline is None:
            raise ValueError("Pipeline not initialized")

        control_image = await context.image_to_pil(self.control_image)
        ip_adapter_image = await self._setup_ip_adapter(context)
        generator = self._setup_generator()

        image = self._pipeline(
            prompt=self.prompt,
            negative_prompt=self.negative_prompt,
            image=control_image,
            ip_adapter_image=ip_adapter_image,
            width=control_image.width,
            height=control_image.height,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            controlnet_conditioning_scale=self.controlnet_conditioning_scale,
            generator=generator,
            callback=self.progress_callback(context),
            callback_steps=1,
        ).images[  # type: ignore
            0
        ]  # type: ignore

        return await context.image_from_pil(image)


class StableDiffusionImg2ImgNode(StableDiffusionBaseNode):
    """
    Transforms existing images based on text prompts using Stable Diffusion.
    image, generation, AI, image-to-image

    Use cases:
    - Modifying existing images to fit a specific style or theme
    - Enhancing or altering photographs
    - Creating variations of existing artwork
    - Applying text-guided edits to images
    """

    model: StableDiffusionModelId = Field(
        default=StableDiffusionModelId.SD_V1_5,
        description="The Stable Diffusion model to use for generation.",
    )

    init_image: ImageRef = Field(
        default=ImageRef(),
        description="The initial image for Image-to-Image generation.",
    )
    strength: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Strength for Image-to-Image generation. Higher values allow for more deviation from the original image.",
    )

    @classmethod
    def get_title(cls):
        return "Stable Diffusion (Img2Img)"

    async def initialize(self, context: ProcessingContext):
        if self._pipe is None:
            self._pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                self.model.value, torch_dtype=torch.float16, safety_checker=None
            )
            self._set_scheduler(self.scheduler)

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipe is None:
            raise ValueError("Pipeline not initialized")

        generator = self._setup_generator()
        init_image = await context.image_to_pil(self.init_image)
        ip_adapter_image = await self._setup_ip_adapter(context)

        image = self._pipe(
            prompt=self.prompt,
            image=init_image,
            ip_adapter_image=ip_adapter_image,
            negative_prompt=self.negative_prompt,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            width=init_image.width,
            height=init_image.height,
            strength=self.strength,
            generator=generator,
            callback=self.progress_callback(context),
            callback_steps=1,
        ).images[0]

        return await context.image_from_pil(image)


class StableDiffusionControlNetInpaintNode(StableDiffusionBaseNode):
    """
    Performs inpainting on images using Stable Diffusion with ControlNet guidance.
    image, inpainting, AI, controlnet

    Use cases:
    - Remove unwanted objects from images with precise control
    - Fill in missing parts of images guided by control images
    - Modify specific areas of images while preserving the rest and maintaining structure
    """

    model: StableDiffusionModelId = Field(
        default=StableDiffusionModelId.SD_V1_5,
        description="The Stable Diffusion model to use for generation.",
    )

    class StableDiffusionControlNetModel(str, Enum):
        INPAINT = "lllyasviel/control_v11p_sd15_inpaint"

    controlnet: StableDiffusionControlNetModel = Field(
        default=StableDiffusionControlNetModel.INPAINT,
        description="The ControlNet model to use for guidance.",
    )
    init_image: ImageRef = Field(
        default=ImageRef(),
        description="The initial image to be inpainted.",
    )
    mask_image: ImageRef = Field(
        default=ImageRef(),
        description="The mask image indicating areas to be inpainted.",
    )
    control_image: ImageRef = Field(
        default=ImageRef(),
        description="The control image to guide the inpainting process.",
    )
    controlnet_conditioning_scale: float = Field(
        default=0.5,
        description="The scale for ControlNet conditioning.",
        ge=0.0,
        le=2.0,
    )

    _pipeline: StableDiffusionControlNetInpaintPipeline | None = None

    @classmethod
    def get_title(cls):
        return "Stable Diffusion ControlNet Inpaint"

    async def initialize(self, context: ProcessingContext):
        controlnet = ControlNetModel.from_pretrained(
            self.controlnet.value, torch_dtype=torch.float16
        )
        self._pipeline = StableDiffusionControlNetInpaintPipeline.from_pretrained(
            self.model.value, controlnet=controlnet, torch_dtype=torch.float16
        )  # type: ignore
        self._pipeline.enable_model_cpu_offload()  # type: ignore

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipeline is None:
            raise ValueError("Pipeline not initialized")

        init_image = await context.image_to_pil(self.init_image)
        mask_image = await context.image_to_pil(self.mask_image)
        control_image = await context.image_to_pil(self.control_image)
        ip_adapter_image = await self._setup_ip_adapter(context)
        generator = self._setup_generator()

        image = self._pipeline(
            prompt=self.prompt,
            negative_prompt=self.negative_prompt,
            image=init_image,
            mask_image=mask_image,
            control_image=control_image,
            ip_adapter_image=ip_adapter_image,
            width=init_image.width,
            height=init_image.height,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            controlnet_conditioning_scale=self.controlnet_conditioning_scale,
            generator=generator,
            callback=self.progress_callback(context),
            callback_steps=1,
        ).images[  # type: ignore
            0
        ]

        return await context.image_from_pil(image)


class StableDiffusionInpaintNode(StableDiffusionBaseNode):
    """
    Performs inpainting on images using Stable Diffusion.
    image, inpainting, AI

    Use cases:
    - Remove unwanted objects from images
    - Fill in missing parts of images
    - Modify specific areas of images while preserving the rest
    """

    init_image: ImageRef = Field(
        default=ImageRef(),
        description="The initial image to be inpainted.",
    )
    mask_image: ImageRef = Field(
        default=ImageRef(),
        description="The mask image indicating areas to be inpainted.",
    )
    strength: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Strength for inpainting. Higher values allow for more deviation from the original image.",
    )

    @classmethod
    def get_title(cls):
        return "Stable Diffusion (Inpaint)"

    async def initialize(self, context: ProcessingContext):
        if self._pipe is None:
            self._pipe = StableDiffusionInpaintPipeline.from_pretrained(
                "runwayml/stable-diffusion-inpainting",
                torch_dtype=torch.float16,
                safety_checker=None,
            )
            self._set_scheduler(self.scheduler)

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipe is None:
            raise ValueError("Pipeline not initialized")

        generator = self._setup_generator()
        init_image = await context.image_to_pil(self.init_image)
        mask_image = await context.image_to_pil(self.mask_image)
        ip_adapter_image = await self._setup_ip_adapter(context)

        image = self._pipe(
            prompt=self.prompt,
            image=init_image,
            mask_image=mask_image,
            negative_prompt=self.negative_prompt,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            width=init_image.width,
            height=init_image.height,
            strength=self.strength,
            generator=generator,
            ip_adapter_image=ip_adapter_image,
            callback=self.progress_callback(context),
            callback_steps=1,
        ).images[0]

        return await context.image_from_pil(image)


class StableDiffusionControlNetImg2ImgNode(StableDiffusionBaseNode):
    """
    Transforms existing images using Stable Diffusion with ControlNet guidance.
    image, generation, AI, image-to-image, controlnet

    Use cases:
    - Modify existing images with precise control over composition and structure
    - Apply specific styles or concepts to photographs or artwork with guided transformations
    - Create variations of existing visual content while maintaining certain features
    - Enhance image editing capabilities with AI-guided transformations
    """

    model: StableDiffusionModelId = Field(
        default=StableDiffusionModelId.SD_V1_5,
        description="The Stable Diffusion model to use for generation.",
    )

    controlnet: StableDiffusionControlNetModel = Field(
        default=StableDiffusionControlNetModel.CANNY,
        description="The ControlNet model to use for guidance.",
    )
    image: ImageRef = Field(
        default=ImageRef(),
        description="The input image to be transformed.",
    )
    control_image: ImageRef = Field(
        default=ImageRef(),
        description="The control image to guide the transformation.",
    )

    _pipeline: StableDiffusionControlNetImg2ImgPipeline | None = None

    @classmethod
    def get_title(cls):
        return "Stable Diffusion ControlNet (Img2Img)"

    async def initialize(self, context: ProcessingContext):
        controlnet = ControlNetModel.from_pretrained(
            self.controlnet.value, torch_dtype=torch.float16
        )
        self._pipeline = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
            self.model.value, controlnet=controlnet, torch_dtype=torch.float16
        )  # type: ignore
        self._pipeline.enable_model_cpu_offload()  # type: ignore
        self._set_scheduler(self.scheduler)

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipeline is None:
            raise ValueError("Pipeline not initialized")

        input_image = await context.image_to_pil(self.image)
        control_image = await context.image_to_pil(self.control_image)
        ip_adapter_image = await self._setup_ip_adapter(context)

        generator = torch.Generator(device="cuda").manual_seed(self.seed)

        image = self._pipeline(
            prompt=self.prompt,
            image=input_image,
            control_image=control_image,
            ip_adapter_image=ip_adapter_image,
            width=input_image.width,
            height=input_image.height,
            num_inference_steps=self.num_inference_steps,
            generator=generator,
            callback=self.progress_callback(context),
            callback_steps=1,
        ).images[  # type: ignore
            0
        ]

        return await context.image_from_pil(image)


class StableDiffusionXLModelId(str, Enum):
    SDXL_1_0 = "stabilityai/stable-diffusion-xl-base-1.0"
    JUGGERNAUT_XL = "RunDiffusion/Juggernaut-XL-v9"
    REALVISXL = "SG161222/RealVisXL_V4.0"


class IPAdapter_SDXL_Model(str, Enum):
    NONE = ""
    IP_ADAPTER = "ip-adapter_sdxl.safetensors"
    IP_ADAPTER_PLUS = "ip-adapter-plus_sdxl_vit-h.safetensors"


class StableDiffusionXL(BaseNode):
    """
    Generates images from text prompts using Stable Diffusion XL.
    image, generation, AI, text-to-image

    Use cases:
    - Creating custom illustrations for marketing materials
    - Generating concept art for game and film development
    - Producing unique stock imagery for websites and publications
    - Visualizing interior design concepts for clients
    """

    model: StableDiffusionXLModelId = Field(
        default=StableDiffusionXLModelId.SDXL_1_0,
        description="The Stable Diffusion XL model to use for generation.",
    )

    prompt: str = Field(default="", description="The prompt for image generation.")
    seed: int = Field(
        default=-1,
        ge=-1,
        le=1000000,
        description="Seed for the random number generator.",
    )
    num_inference_steps: int = Field(
        default=25, ge=1, le=100, description="Number of inference steps."
    )
    guidance_scale: float = Field(
        default=7.0, ge=0.0, le=20.0, description="Guidance scale for generation."
    )
    width: int = Field(
        default=1024, ge=64, le=2048, description="Width of the generated image."
    )
    height: int = Field(
        default=1024, ge=64, le=2048, description="Height of the generated image"
    )
    scheduler: StableDiffusionScheduler = Field(
        default=StableDiffusionScheduler.DDIMScheduler,
        description="The scheduler to use for the diffusion process.",
    )
    ip_adapter_model: IPAdapter_SDXL_Model = Field(
        default=IPAdapter_SDXL_Model.NONE,
        description="The IP adapter model to use for image processing",
    )
    ip_adapter_image: ImageRef = Field(
        default=ImageRef(),
        description="When provided the image will be fed into the IP adapter",
    )
    ip_adapter_scale: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Strength of the IP adapter image",
    )

    _pipe: Any = None

    @classmethod
    def get_title(cls):
        return "Stable Diffusion XL (Text2Img)"

    def _set_scheduler(self, scheduler_type: StableDiffusionScheduler):
        scheduler_class = get_scheduler_class(scheduler_type)
        self._pipe.scheduler = scheduler_class.from_config(self._pipe.scheduler.config)

    async def initialize(self, context: ProcessingContext):
        if self._pipe is None:
            self._pipe = StableDiffusionXLPipeline.from_pretrained(
                self.model.value,
                torch_dtype=torch.float16,
                variant="fp16",
            )
            self._set_scheduler(self.scheduler)
            if self.ip_adapter_model != IPAdapter_SD15_Model.NONE:
                self._pipe.load_ip_adapter(
                    "h94/IP-Adapter",
                    subfolder="sdxl_models",
                    weight_name=self.ip_adapter_model,
                )

    async def move_to_device(self, device: str):
        if self._pipe is not None:
            self._pipe.to(device)

    async def process(self, context) -> ImageRef:
        if self._pipe is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        if self.ip_adapter_model != IPAdapter_SD15_Model.NONE:
            assert not self.ip_adapter_image.is_empty()
            ip_adapter_image = await context.image_to_pil(self.ip_adapter_image)
        else:
            ip_adapter_image = None

        image = self._pipe(
            prompt=self.prompt,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            width=self.width,
            height=self.height,
            ip_adapter_image=ip_adapter_image,
            callback=progress_callback(self.id, self.num_inference_steps, context),
            callback_steps=1,
            generator=generator,
        ).images[0]

        return await context.image_from_pil(image)


class SDXLInpainting(BaseNode):
    """
    Performs inpainting on images using Stable Diffusion XL.
    image, inpainting, AI, image-editing

    Use cases:
    - Removing unwanted objects from images
    - Adding new elements to existing images
    - Repairing damaged or incomplete images
    - Creating creative image edits and modifications
    """

    prompt: str = Field(
        default="",
        description="The prompt describing what to paint in the masked area.",
    )
    image: ImageRef = Field(
        default=ImageRef(),
        description="The input image to be inpainted.",
    )
    mask_image: ImageRef = Field(
        default=ImageRef(),
        description="The mask image indicating the area to be inpainted.",
    )
    negative_prompt: str = Field(
        default="",
        description="The negative prompt to guide what should not appear in the inpainted area.",
    )
    num_inference_steps: int = Field(
        default=30,
        ge=1,
        le=100,
        description="Number of denoising steps. Values between 15 and 30 work well.",
    )
    guidance_scale: float = Field(
        default=8.0,
        ge=1.0,
        le=20.0,
        description="Guidance scale for generation.",
    )
    strength: float = Field(
        default=0.99,
        ge=0.0,
        le=1.0,
        description="Strength of the inpainting. Values below 1.0 work best.",
    )
    seed: int = Field(
        default=-1,
        ge=-1,
        le=2**32 - 1,
        description="Seed for the random number generator. Use -1 for a random seed.",
    )

    _pipe: Any = None

    @classmethod
    def get_title(cls):
        return "SDXL Inpainting"

    async def initialize(self, context: ProcessingContext):
        if self._pipe is None:
            self._pipe = AutoPipelineForInpainting.from_pretrained(
                "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
                torch_dtype=torch.float16,
                variant="fp16",
            )

    async def move_to_device(self, device: str):
        if self._pipe is not None:
            self._pipe.to(device)

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipe is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cuda")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        # Load and prepare the input and mask images
        input_image = await context.image_to_pil(self.image)
        mask_image = await context.image_to_pil(self.mask_image)

        def callback(step: int, timestep: int, latents: torch.FloatTensor) -> None:
            context.post_message(
                NodeProgress(
                    node_id=self.id,
                    progress=step,
                    total=self.num_inference_steps,
                )
            )

        output = self._pipe(
            prompt=self.prompt,
            image=input_image,
            mask_image=mask_image,
            negative_prompt=self.negative_prompt,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            strength=self.strength,
            generator=generator,
            width=input_image.width,
            height=input_image.height,
            callback=callback,
            callback_steps=1,
        )

        # Convert the output image to ImageRef
        return await context.image_from_pil(output.images[0])


class StableDiffusionXLImg2Img(BaseNode):
    """
    Transforms existing images based on text prompts using Stable Diffusion XL.
    image, generation, AI, image-to-image

    Use cases:
    - Modifying existing images to fit a specific style or theme
    - Enhancing or altering stock photos for unique marketing materials
    - Transforming rough sketches into detailed illustrations
    - Creating variations of existing artwork or designs
    """

    model: StableDiffusionXLModelId = Field(
        default=StableDiffusionXLModelId.SDXL_1_0,
        description="The Stable Diffusion XL model to use for generation.",
    )
    prompt: str = Field(default="", description="The prompt for image generation.")
    init_image: ImageRef = Field(
        default=ImageRef(),
        description="The initial image for Image-to-Image generation.",
    )
    seed: int = Field(
        default=-1,
        ge=-1,
        le=1000000,
        description="Seed for the random number generator.",
    )
    num_inference_steps: int = Field(
        default=25, ge=1, le=100, description="Number of inference steps."
    )
    guidance_scale: float = Field(
        default=7.0, ge=0.0, le=20.0, description="Guidance scale for generation."
    )
    width: int = Field(
        default=1024, ge=64, le=2048, description="Width of the generated image."
    )
    height: int = Field(
        default=1024, ge=64, le=2048, description="Height of the generated image"
    )
    scheduler: StableDiffusionScheduler = Field(
        default=StableDiffusionScheduler.DDIMScheduler,
        description="The scheduler to use for the diffusion process.",
    )
    strength: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Strength for Image-to-Image generation.",
    )

    _pipe: Any = None

    @classmethod
    def get_title(cls):
        return "Stable Diffusion XL (Img2Img)"

    async def initialize(self, context: ProcessingContext):
        if self._pipe is None:
            self._pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                self.model.value,
                torch_dtype=torch.float16,
                variant="fp16",
            )
            self._set_scheduler(self.scheduler)

    def _set_scheduler(self, scheduler_type: StableDiffusionScheduler):
        scheduler_class = globals()[scheduler_type.value]
        self._pipe.scheduler = scheduler_class.from_config(self._pipe.scheduler.config)

    async def move_to_device(self, device: str):
        if self._pipe is not None:
            self._pipe.to(device)

    async def process(self, context) -> ImageRef:
        if self._pipe is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        init_image = await context.image_to_pil(self.init_image)
        init_image = init_image.resize((self.width, self.height))

        image = self._pipe(
            prompt=self.prompt,
            image=init_image,
            num_inference_steps=self.num_inference_steps,
            strength=self.strength,
            guidance_scale=self.guidance_scale,
            callback=progress_callback(self.id, self.num_inference_steps, context),
            callback_steps=1,
            generator=generator,
        ).images[0]

        return await context.image_from_pil(image)


class SDXLTurboModelId(str, Enum):
    SDXL_TURBO = "stabilityai/sdxl-turbo"
    DREAMSHAPER_XL_V2_TURBO = "Lykon/dreamshaper-xl-v2-turbo"


class SDXLTurbo(BaseNode):
    """
    Generates images from text prompts using SDXL Turbo.
    image, generation, AI, text-to-image, fast

    Use cases:
    - Rapid prototyping of visual concepts
    - Real-time image generation for interactive applications
    - Quick visualization of ideas for brainstorming sessions
    - Creating multiple variations of an image concept quickly
    """

    model: SDXLTurboModelId = Field(
        default=SDXLTurboModelId.SDXL_TURBO,
        description="The SDXL Turbo model to use for generation.",
    )
    prompt: str = Field(default="", description="The prompt for image generation.")
    seed: int = Field(
        default=-1,
        ge=-1,
        le=1000000,
        description="Seed for the random number generator.",
    )
    num_inference_steps: int = Field(
        default=1, ge=1, le=50, description="Number of inference steps."
    )
    guidance_scale: float = Field(
        default=0.0, ge=0.0, le=20.0, description="Guidance scale for generation."
    )
    width: int = Field(
        default=512, ge=64, le=2048, description="Width of the generated image."
    )
    height: int = Field(
        default=512, ge=64, le=2048, description="Height of the generated image"
    )

    _pipe: Any = None

    @classmethod
    def get_title(cls):
        return "SDXL Turbo (Text2Img)"

    async def initialize(self, context: ProcessingContext):
        if self._pipe is None:
            self._pipe = AutoPipelineForText2Image.from_pretrained(
                self.model.value, torch_dtype=torch.float16, variant="fp16"
            )

    async def move_to_device(self, device: str):
        if self._pipe is not None:
            self._pipe.to(device)

    async def process(self, context) -> ImageRef:
        if self._pipe is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        image = self._pipe(
            prompt=self.prompt,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            width=self.width,
            height=self.height,
            callback=progress_callback(self.id, self.num_inference_steps, context),
            callback_steps=1,
            generator=generator,
        ).images[0]

        return await context.image_from_pil(image)


class SDXLTurboImg2Img(BaseNode):
    """
    Transforms existing images based on text prompts using SDXL Turbo.
    image, generation, AI, image-to-image

    Use cases:
    - Modifying existing images to fit a specific style or theme
    - Enhancing or altering stock photos for unique marketing materials
    - Transforming rough sketches into detailed illustrations
    - Creating variations of existing artwork or designs
    """

    model: SDXLTurboModelId = Field(
        default=SDXLTurboModelId.SDXL_TURBO,
        description="The SDXL Turbo model to use for generation.",
    )
    prompt: str = Field(default="", description="The prompt for image generation.")
    init_image: ImageRef = Field(
        default=ImageRef(),
        description="The initial image for Image-to-Image generation.",
    )
    seed: int = Field(
        default=-1,
        ge=-1,
        le=1000000,
        description="Seed for the random number generator.",
    )
    num_inference_steps: int = Field(
        default=4, ge=1, le=50, description="Number of inference steps."
    )
    guidance_scale: float = Field(
        default=7.0, ge=0.0, le=20.0, description="Guidance scale for generation."
    )
    width: int = Field(
        default=1024, ge=64, le=2048, description="Width of the generated image."
    )
    height: int = Field(
        default=1024, ge=64, le=2048, description="Height of the generated image"
    )
    strength: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Strength for Image-to-Image generation.",
    )

    _pipe: Any = None

    @classmethod
    def get_title(cls):
        return "SD XL Turbo (Img2Img)"

    async def initialize(self, context: ProcessingContext):
        if self._pipe is None:
            self._pipe = AutoPipelineForImage2Image.from_pretrained(
                self.model.value,
                torch_dtype=torch.float16,
                variant="fp16",
            )

    async def move_to_device(self, device: str):
        if self._pipe is not None:
            self._pipe.to(device)

    async def process(self, context) -> ImageRef:
        if self._pipe is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = torch.Generator(device="cpu")
        if self.seed != -1:
            generator = generator.manual_seed(self.seed)

        init_image = await context.image_to_pil(self.init_image)
        init_image = init_image.resize((self.width, self.height))

        image = self._pipe(
            prompt=self.prompt,
            image=init_image,
            num_inference_steps=self.num_inference_steps,
            strength=self.strength,
            guidance_scale=self.guidance_scale,
            callback=progress_callback(self.id, self.num_inference_steps, context),
            callback_steps=1,
            generator=generator,
        ).images[0]

        return await context.image_from_pil(image)


class StableDiffusion3ControlNetNode(BaseNode):
    """
    Generates images using Stable Diffusion 3 with ControlNet.
    image, generation, AI, text-to-image, controlnet

    Use cases:
    - Generate images with precise control over composition and structure
    - Create variations of existing images while maintaining specific features
    - Artistic image generation with guided outputs
    """

    class StableDiffusion3ControlNetModelId(str, Enum):
        SD3_CONTROLNET_CANNY = "InstantX/SD3-Controlnet-Canny"
        SD3_CONTROLNET_TILE = "InstantX/SD3-Controlnet-Tile"
        SD3_CONTROLNET_POSE = "InstantX/SD3-Controlnet-Pose"

    prompt: str = Field(
        default="A girl holding a sign that says InstantX",
        description="A text prompt describing the desired image.",
    )
    control_model: StableDiffusion3ControlNetModelId = Field(
        default=StableDiffusion3ControlNetModelId.SD3_CONTROLNET_CANNY,
        description="The ControlNet model to use for image generation.",
    )
    control_image: ImageRef = Field(
        default=ImageRef(),
        description="The control image to guide the generation process.",
    )
    controlnet_conditioning_scale: float = Field(
        default=0.7,
        description="The scale of the ControlNet conditioning.",
        ge=0.0,
        le=1.0,
    )
    num_inference_steps: int = Field(
        default=30,
        description="The number of denoising steps.",
        ge=1,
        le=100,
    )
    seed: int = Field(
        default=-1,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )

    _pipeline: StableDiffusion3ControlNetPipeline | None = None

    async def initialize(self, context: ProcessingContext):
        controlnet = SD3ControlNetModel.from_pretrained(
            self.control_model.value, torch_dtype=torch.float16
        )
        self._pipeline = StableDiffusion3ControlNetPipeline.from_pretrained(
            "stabilityai/stable-diffusion-3-medium-diffusers",
            controlnet=controlnet,
            torch_dtype=torch.float16,
        )  # type: ignore

    async def move_to_device(self, device: str):
        pass

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipeline is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = None
        if self.seed != -1:
            generator = torch.Generator(device=self._pipeline.device).manual_seed(
                self.seed
            )

        # Load the control image
        control_image = await context.image_to_pil(self.control_image)

        def callback(pipe: Any, step: int, timestep: int, args: dict):
            context.post_message(
                NodeProgress(
                    node_id=self.id,
                    progress=step,
                    total=self.num_inference_steps,
                )
            )
            return {}

        # Generate the image
        self._pipeline.enable_sequntial_cpu_offload()

        output = self._pipeline(
            prompt=self.prompt,
            control_image=control_image,
            width=control_image.width,
            height=control_image.height,
            controlnet_conditioning_scale=self.controlnet_conditioning_scale,
            num_inference_steps=self.num_inference_steps,
            generator=generator,
            callback_on_step_end=callback,  # type: ignore
        )

        # Convert the output image to ImageRef
        return await context.image_from_pil(output.images[0])  # type: ignore


class StableDiffusionXLControlNetNode(BaseNode):
    """
    Generates images using Stable Diffusion XL with ControlNet.
    image, generation, AI, text-to-image, controlnet

    Use cases:
    - Generate high-quality images with precise control over structures and features
    - Create variations of existing images while maintaining specific characteristics
    - Artistic image generation with guided outputs based on various control types
    """

    class StableDiffusionXLControlNetModel(str, Enum):
        CANNY = "diffusers/controlnet-canny-sdxl-1.0"
        DEPTH = "diffusers/controlnet-depth-sdxl-1.0"
        POSE = "diffusers/controlnet-openpose-sdxl-1.0"
        NORMAL = "diffusers/controlnet-normal-sdxl-1.0"

    prompt: str = Field(
        default="aerial view, a futuristic research complex in a bright foggy jungle, hard lighting",
        description="A text prompt describing the desired image.",
    )
    negative_prompt: str = Field(
        default="low quality, bad quality, sketches",
        description="A text prompt describing what to avoid in the image.",
    )
    control_image: ImageRef = Field(
        default=ImageRef(),
        description="The control image to guide the generation process (already processed).",
    )
    control_model: StableDiffusionXLControlNetModel = Field(
        default=StableDiffusionXLControlNetModel.CANNY,
        description="The type of ControlNet model to use.",
    )
    controlnet_conditioning_scale: float = Field(
        default=0.5,
        description="The scale of the ControlNet conditioning.",
        ge=0.0,
        le=2.0,
    )
    num_inference_steps: int = Field(
        default=30,
        description="The number of denoising steps.",
        ge=1,
        le=100,
    )
    seed: int = Field(
        default=-1,
        description="Seed for the random number generator. Use -1 for a random seed.",
        ge=-1,
    )

    _pipeline: StableDiffusionXLControlNetPipeline | None = None

    async def initialize(self, context: ProcessingContext):
        controlnet = ControlNetModel.from_pretrained(
            self.control_model.value, torch_dtype=torch.float16
        )
        vae = AutoencoderKL.from_pretrained(
            "madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16
        )
        self._pipeline = StableDiffusionXLControlNetPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            controlnet=controlnet,
            vae=vae,
            torch_dtype=torch.float16,
        )  # type: ignore
        self._pipeline.enable_model_cpu_offload()  # type: ignore

    async def move_to_device(self, device: str):
        # Not needed as we're using CPU offload
        pass

    async def process(self, context: ProcessingContext) -> ImageRef:
        if self._pipeline is None:
            raise ValueError("Pipeline not initialized")

        # Set up the generator for reproducibility
        generator = None
        if self.seed != -1:
            generator = torch.Generator(device=self._pipeline.device).manual_seed(
                self.seed
            )

        def callback(step: int, timestep: int, args: dict):
            context.post_message(
                NodeProgress(
                    node_id=self.id,
                    progress=step,
                    total=self.num_inference_steps,
                )
            )
            return {}

        control_image = await context.image_to_pil(self.control_image)

        # Generate the image
        output = self._pipeline(
            prompt=self.prompt,
            negative_prompt=self.negative_prompt,
            image=control_image,
            controlnet_conditioning_scale=self.controlnet_conditioning_scale,
            num_inference_steps=self.num_inference_steps,
            generator=generator,
            callback=callback,
            callback_steps=1,
        )

        # Convert the output image to ImageRef
        return await context.image_from_pil(output.images[0])  # type: ignore
