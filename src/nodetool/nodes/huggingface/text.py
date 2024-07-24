from enum import Enum
from typing import Any
from pydantic import Field
from nodetool.metadata.types import ColumnDef, DataframeRef
from nodetool.nodes.huggingface.huggingface_pipeline import HuggingFacePipelineNode
from nodetool.workflows.processing_context import ProcessingContext

class TextGeneration(HuggingFacePipelineNode):
    """
    Generates text based on a given prompt.
    text, generation, natural language processing

    Use cases:
    - Creative writing assistance
    - Automated content generation
    - Chatbots and conversational AI
    - Code generation and completion
    """

    class TextGenerationModelId(str, Enum):
        GPT2 = "openai-community/gpt2"
        DISTILGPT2 = "distilbert/distilgpt2"
        QWEN2_0_5 = "Qwen/Qwen2-0.5B-Instruct"
        STARCODER = "bigcode/starcoder"

    model: TextGenerationModelId = Field(
        default=TextGenerationModelId.GPT2,
        title="Model ID on Huggingface",
        description="The model ID to use for the text generation",
    )
    inputs: str = Field(
        default="",
        title="Prompt",
        description="The input text prompt for generation",
    )
    max_new_tokens: int = Field(
        default=50,
        title="Max New Tokens",
        description="The maximum number of new tokens to generate",
    )
    temperature: float = Field(
        default=1.0,
        title="Temperature",
        description="Controls randomness in generation. Lower values make it more deterministic.",
        ge=0.0,
        le=2.0,
    )
    top_p: float = Field(
        default=1.0,
        title="Top P",
        description="Controls diversity of generated text. Lower values make it more focused.",
        ge=0.0,
        le=1.0,
    )
    do_sample: bool = Field(
        default=True,
        title="Do Sample",
        description="Whether to use sampling or greedy decoding",
    )

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return 'text-generation'

    def get_params(self):
        return {
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "do_sample": self.do_sample,
        }
        
    async def get_inputs(self, context: ProcessingContext):
        return self.inputs

    async def process_remote_result(self, context: ProcessingContext, result: Any) -> str:
        return result[0]["generated_text"]

    async def process_local_result(self, context: ProcessingContext, result: Any) -> str:
        return result[0]['generated_text']

    async def process(self, context: ProcessingContext) -> str:
        return await super().process(context)


class TextClassifier(HuggingFacePipelineNode):
    class TextClassifierModelId(str, Enum):
        CARDIFFNLP_TWITTER_ROBERTA_BASE_SENTIMENT_LATEST = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        J_HARTMANN_EMOTION_ENGLISH_DISTILROBERTA_BASE = "j-hartmann/emotion-english-distilroberta-base"
        SAMLOWE_ROBERTA_BASE_GO_EMOTIONS = "SamLowe/roberta-base-go_emotions"
        PROSUSAI_FINBERT = "ProsusAI/finbert"
        DISTILBERT_BASE_UNCASED_FINETUNED_SST_2_ENGLISH = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

    model: TextClassifierModelId = Field(
        default=TextClassifierModelId.CARDIFFNLP_TWITTER_ROBERTA_BASE_SENTIMENT_LATEST,
        title="Model ID on Huggingface",
        description="The model ID to use for the classification",
    )
    inputs: str = Field(
        default="",
        title="Inputs",
        description="The input text to the model",
    )

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return 'text-classification'

    async def process_remote_result(self, context: ProcessingContext, result: Any) -> dict[str, float]:
        return result[0]

    async def process_local_result(self, contex: ProcessingContext, result: Any) -> dict[str, float]:
        return {i['label']: i['score'] for i in list(result)}
    
    async def process(self, context: ProcessingContext) -> dict[str, float]:
        return await super().process(context)


class Summarize(HuggingFacePipelineNode):
    class SummarizeModelId(str, Enum):
        FALCONSAI_TEXT_SUMMARIZATION = "Falconsai/text_summarization"
        FALCONSAI_MEDICAL_SUMMARIZATION = "Falconsai/medical_summarization"
        IMVLADIKON_HET5_SUMMARIZATION = "imvladikon/het5_summarization"

    model: SummarizeModelId = Field(
        default=SummarizeModelId.FALCONSAI_TEXT_SUMMARIZATION,
        title="Model ID on Huggingface",
        description="The model ID to use for the summarization",
    )
    inputs: str = Field(
        default="",
        title="Inputs",
        description="The input text to the model",
    )
    max_length: int = Field(
        default=100,
        title="Max Length",
        description="The maximum length of the generated text",
    )
    do_sample: bool = Field(
        default=False,
        title="Do Sample",
        description="Whether to sample from the model",
    )

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return 'summarization'

    def get_params(self):
        return {
            "max_length": self.max_length,
            "do_sample": self.do_sample,
        }

    async def process_remote_result(self, context: ProcessingContext, result: Any) -> str:
        return result[0]["summary_text"]

    async def process_local_result(self, context: ProcessingContext, result: Any) -> str:
        return result[0]['summary_text']

    async def process(self, context: ProcessingContext) -> str:
        return await super().process(context)
    

class QuestionAnswering(HuggingFacePipelineNode):
    """
    Answers questions based on a given context.
    text, question answering, natural language processing

    Use cases:
    - Automated customer support
    - Information retrieval from documents
    - Reading comprehension tasks
    - Enhancing search functionality
    """

    class QuestionAnsweringModelId(str, Enum):
        DISTILBERT_BASE_CASED_DISTILLED_SQUAD = "distilbert-base-cased-distilled-squad"
        BERT_LARGE_UNCASED_WHOLE_WORD_MASKING_FINETUNED_SQUAD = "bert-large-uncased-whole-word-masking-finetuned-squad"
        DEEPSET_ROBERTA_BASE_SQUAD2 = "deepset/roberta-base-squad2"
        DISTILBERT_BASE_UNCASED_DISTILLED_SQUAD = "distilbert-base-uncased-distilled-squad"

    model: QuestionAnsweringModelId = Field(
        default=QuestionAnsweringModelId.DISTILBERT_BASE_CASED_DISTILLED_SQUAD,
        title="Model ID on Huggingface",
        description="The model ID to use for question answering",
    )
    context: str = Field(
        default="",
        title="Context",
        description="The context or passage to answer questions from",
    )
    question: str = Field(
        default="",
        title="Question",
        description="The question to be answered based on the context",
    )

    def get_model_id(self):
        return self.model.value
    
    async def get_inputs(self, context: ProcessingContext):
        return {
            "question": self.question,
            "context": self.context,
        }

    @property
    def pipeline_task(self) -> str:
        return 'question-answering'

    async def process_remote_result(self, context: ProcessingContext, result: Any) -> dict[str, Any]:
        return await self.process_local_result(context, result)

    async def process_local_result(self, context: ProcessingContext, result: Any) -> dict[str, Any]:
        return {
            "answer": result["answer"],
            "score": result["score"],
            "start": result["start"],
            "end": result["end"],
        }

    async def process(self, context: ProcessingContext) -> dict[str, Any]:
        return await super().process(context)
    

class FillMask(HuggingFacePipelineNode):
    """
    Fills in a masked token in a given text.
    text, fill-mask, natural language processing

    Use cases:
    - Text completion
    - Sentence prediction
    - Language understanding tasks
    - Generating text options
    """

    class FillMaskModelId(str, Enum):
        BERT_BASE_UNCASED = "bert-base-uncased"
        ROBERTA_BASE = "roberta-base"
        DISTILBERT_BASE_UNCASED = "distilbert-base-uncased"
        ALBERT_BASE_V2 = "albert-base-v2"

    model: FillMaskModelId = Field(
        default=FillMaskModelId.BERT_BASE_UNCASED,
        title="Model ID on Huggingface",
        description="The model ID to use for fill-mask task",
    )
    inputs: str = Field(
        default="The capital of France is [MASK].",
        title="Inputs",
        description="The input text with [MASK] token to be filled",
    )
    top_k: int = Field(
        default=5,
        title="Top K",
        description="Number of top predictions to return",
    )
    
    async def get_inputs(self, context: ProcessingContext):
        return self.inputs

    def get_model_id(self):
        return self.model.value

    @property
    def pipeline_task(self) -> str:
        return 'fill-mask'

    def get_params(self):
        return {
            "top_k": self.top_k,
        }

    async def process_remote_result(self, context: ProcessingContext, result: Any) -> DataframeRef:
        return await self.process_local_result(context, result)

    async def process_local_result(self, context: ProcessingContext, result: Any) -> DataframeRef:
        data = [[item["token_str"], item["score"]] for item in result]
        columns = [
            ColumnDef(name="token", data_type="string"),
            ColumnDef(name="score", data_type="float"),
        ]
        return DataframeRef(columns=columns, data=data)

    async def process(self, context: ProcessingContext) -> list[dict[str, Any]]:
        return await super().process(context)
    

class TableQuestionAnswering(HuggingFacePipelineNode):
    """
    Answers questions based on tabular data.
    table, question answering, natural language processing

    Use cases:
    - Querying databases using natural language
    - Analyzing spreadsheet data with questions
    - Extracting insights from tabular reports
    - Automated data exploration
    """

    class TableQuestionAnsweringModelId(str, Enum):
        GOOGLE_TAPAS_BASE_FINETUNED_WTQ = "google/tapas-base-finetuned-wtq"
        MICROSOFT_TAPEX_LARGE_FINETUNED_TABFACT = "microsoft/tapex-large-finetuned-tabfact"
        GOOGLE_TAPAS_LARGE_FINETUNED_SQA = "google/tapas-large-finetuned-sqa"

    model: TableQuestionAnsweringModelId = Field(
        default=TableQuestionAnsweringModelId.GOOGLE_TAPAS_BASE_FINETUNED_WTQ,
        title="Model ID on Huggingface",
        description="The model ID to use for table question answering",
    )
    inputs: DataframeRef = Field(
        default=DataframeRef(),
        title="Table",
        description="The input table to query",
    )
    question: str = Field(
        default="",
        title="Question",
        description="The question to be answered based on the table",
    )

    def get_model_id(self):
        return self.model.value
    
    async def get_inputs(self, context: ProcessingContext):
        table = await context.dataframe_to_pandas(self.inputs)
        return {
            "table": table,
            "query": self.question,
        }

    @property
    def pipeline_task(self) -> str:
        return 'table-question-answering'

    async def process_remote_result(self, context: ProcessingContext, result: Any) -> dict[str, Any]:
        return await self.process_local_result(context, result)

    async def process_local_result(self, context: ProcessingContext, result: Any) -> dict[str, Any]:
        return {
            "answer": result["answer"],
            "coordinates": result.get("coordinates"),
            "cells": result.get("cells"),
            "aggregator": result.get("aggregator"),
        }

    async def process(self, context: ProcessingContext) -> dict[str, Any]:
        return await super().process(context)