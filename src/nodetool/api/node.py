#!/usr/bin/env python

from fastapi import APIRouter
from nodetool.types.job import (
    JobUpdate,
)
from nodetool.types.prediction import Prediction
from nodetool.metadata.node_metadata import NodeMetadata
from nodetool.metadata.types import (
    AssetRef,
    HuggingFaceModel,
    NodeRef,
    WorkflowRef,
    AudioRef,
    DataframeRef,
    FolderRef,
    ImageRef,
    ModelRef,
    Tensor,
    TextRef,
    VideoRef,
    HFImageTextToText,
    HFVisualQuestionAnswering,
    HFDocumentQuestionAnswering,
    HFVideoTextToText,
    HFComputerVision,
    HFDepthEstimation,
    HFImageClassification,
    HFObjectDetection,
    HFImageSegmentation,
    HFTextToImage,
    HFStableDiffusion,
    HFStableDiffusionXL,
    HFImageToText,
    HFImageToImage,
    HFImageToVideo,
    HFUnconditionalImageGeneration,
    HFVideoClassification,
    HFTextToVideo,
    HFZeroShotImageClassification,
    HFMaskGeneration,
    HFZeroShotObjectDetection,
    HFTextTo3D,
    HFImageTo3D,
    HFImageFeatureExtraction,
    HFNaturalLanguageProcessing,
    HFTextClassification,
    HFTokenClassification,
    HFTableQuestionAnswering,
    HFQuestionAnswering,
    HFZeroShotClassification,
    HFTranslation,
    HFSummarization,
    HFFeatureExtraction,
    HFTextGeneration,
    HFText2TextGeneration,
    HFFillMask,
    HFSentenceSimilarity,
    HFTextToSpeech,
    HFTextToAudio,
    HFAutomaticSpeechRecognition,
    HFAudioToAudio,
    HFAudioClassification,
    HFZeroShotAudioClassification,
    HFVoiceActivityDetection,
)
from nodetool.workflows.base_node import get_registered_node_classes
from nodetool.common.environment import Environment
from nodetool.workflows.types import NodeProgress, NodeUpdate

log = Environment.get_logger()
router = APIRouter(prefix="/api/nodes", tags=["nodes"])


# This is a dummy type that contains all property types and Websocket types.
UnionType = (
    AssetRef
    | AudioRef
    | DataframeRef
    | FolderRef
    | ImageRef
    | Tensor
    | VideoRef
    | ModelRef
    | TextRef
    | WorkflowRef
    | NodeRef
    | Prediction
    | JobUpdate
    | NodeUpdate
    | NodeProgress
    | HuggingFaceModel
    | HFImageTextToText
    | HFVisualQuestionAnswering
    | HFDocumentQuestionAnswering
    | HFVideoTextToText
    | HFComputerVision
    | HFDepthEstimation
    | HFImageClassification
    | HFObjectDetection
    | HFImageSegmentation
    | HFTextToImage
    | HFStableDiffusion
    | HFStableDiffusionXL
    | HFImageToText
    | HFImageToImage
    | HFImageToVideo
    | HFUnconditionalImageGeneration
    | HFVideoClassification
    | HFTextToVideo
    | HFZeroShotImageClassification
    | HFMaskGeneration
    | HFZeroShotObjectDetection
    | HFTextTo3D
    | HFImageTo3D
    | HFImageFeatureExtraction
    | HFNaturalLanguageProcessing
    | HFTextClassification
    | HFTokenClassification
    | HFTableQuestionAnswering
    | HFQuestionAnswering
    | HFZeroShotClassification
    | HFTranslation
    | HFSummarization
    | HFFeatureExtraction
    | HFTextGeneration
    | HFText2TextGeneration
    | HFFillMask
    | HFSentenceSimilarity
    | HFTextToSpeech
    | HFTextToAudio
    | HFAutomaticSpeechRecognition
    | HFAudioToAudio
    | HFAudioClassification
    | HFZeroShotAudioClassification
    | HFVoiceActivityDetection
    | dict
)


@router.get("/dummy")
async def dummy() -> UnionType:
    """
    Returns a dummy node.
    """
    return {"hello": "world"}


@router.get("/metadata")
async def metadata() -> list[NodeMetadata]:
    """
    Returns a list of all node metadata.
    """
    worker_client = Environment.get_worker_api_client()
    if worker_client:
        res = await worker_client.get("/metadata")
        return res.json()
    else:
        return [node_class.metadata() for node_class in get_registered_node_classes()]
