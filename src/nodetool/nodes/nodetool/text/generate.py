from enum import Enum
from pydantic import Field, validator
from nodetool.metadata.types import LlamaFile
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.workflows.base_node import BaseNode


class GPT2Node(BaseNode):
    """
    GPT-2 is a transformer-based language model. This node uses the GPT-2 model to generate text based on a prompt.

    # Applications
    - Generating text based on a prompt.
    - Generating text for chatbots.
    - Generating text for creative writing.
    """

    prompt: str = Field(default="", description="Prompt to send to the model.")
    max_tokens: int = Field(
        default=128,
        ge=1,
        le=1024,
        description="Maximum number of tokens to generate. A word is generally 2-3 tokens (minimum: 1)",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="The temperature to use for the model.",
    )
    top_k: int = Field(
        default=50,
        ge=1,
        le=100,
        description="The number of highest probability tokens to keep for top-k sampling.",
    )
    top_p: float = Field(
        default=0.95,
        ge=0.0,
        le=1.0,
        description="The cumulative probability cutoff for nucleus/top-p sampling.",
    )

    async def process(self, context: ProcessingContext) -> str:
        from transformers import pipeline

        pipe = pipeline(task="text-generation", model="gpt2")
        res = pipe(
            self.prompt,
            max_new_tokens=self.max_tokens,
            do_sample=True,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            return_full_text=False,
        )
        return res[0]["generated_text"]  # type: ignore


class LlamaModel(str, Enum):
    PHI_2 = "Phi-2"
    GEMMA_2B = "Gemma-2B"
    Qwen_0_5 = "Qwen1.5-0.5B-Chat"
    Qwen_1_8 = "Qwen1.5-1.8B-Chat"
    Qwen_4_0 = "Qwen1.5-4.0B-Chat"
    Qwen_7_0 = "Qwen1.5-7.0B-Chat"
    Mistral_7B_Instruct = "Mistral_7B_Instruct"
    Mistral_8x_7B_Instruct = "Mistral_8x_7B_Instruct"
    CapybaraHermes_2_5_Mistral_7B = "CapybaraHermes-2.5-Mistral-7B"
    Dolphin_2_5_Mixtral_8x7B = "dolphin-2.5-mixtral-8x7b"
    Zephyr_7B = "Zephyr-7B"


llama_models = {
    LlamaModel.PHI_2: {
        "repo_id": "TheBloke/phi-2-GGUF",
        "filename": "*Q4_K_S.gguf",
    },
    LlamaModel.GEMMA_2B: {
        "repo_id": "lmstudio-ai/gemma-2b-it-GGUF",
        "filename": "*q8_0.gguf",
    },
    LlamaModel.Qwen_0_5: {
        "repo_id": "Qwen/Qwen1.5-0.5B-Chat-GGUF",
        "filename": "*q8_0.gguf",
    },
    LlamaModel.Qwen_1_8: {
        "repo_id": "Qwen/Qwen1.5-1.8B-Chat-GGUF",
        "filename": "*q8_0.gguf",
    },
    LlamaModel.Qwen_4_0: {
        "repo_id": "Qwen/Qwen1.5-4.0B-Chat-GGUF",
        "filename": "*q8_0.gguf",
    },
    LlamaModel.Qwen_7_0: {
        "repo_id": "Qwen/Qwen1.5-7.0B-Chat-GGUF",
        "filename": "*q4_0.gguf",
    },
    LlamaModel.Mistral_7B_Instruct: {
        "repo_id": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        "filename": "*Q4_0.gguf",
    },
    LlamaModel.Mistral_8x_7B_Instruct: {
        "repo_id": "TheBloke/Mistral-8x-7B-Instruct-v0.1-GGUF",
        "filename": "*Q2_K.gguf",
    },
    LlamaModel.CapybaraHermes_2_5_Mistral_7B: {
        "repo_id": "TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF",
        "filename": "*Q4_0.gguf",
    },
    LlamaModel.Dolphin_2_5_Mixtral_8x7B: {
        "repo_id": "TheBloke/Dolphin-2.5-Mixtral-8x7B-GGUF",
        "filename": "*Q2_K.gguf",
    },
    LlamaModel.Zephyr_7B: {
        "repo_id": "TheBloke/zephyr-7B-beta-GGUF",
        "filename": "*Q4_0.gguf",
    },
}

cached_models = {}


class LlamaCppNode(BaseNode):
    """
    Run Llama models.
    """

    model: LlamaFile = Field(default=LlamaFile(), description="The Llama model to use.")
    prompt: str = Field(default="", description="Prompt to send to the model.")
    system_prompt: str = Field(
        default="You are an assistant.",
        description="System prompt to send to the model.",
    )
    max_tokens: int = Field(
        default=128,
        ge=1,
        le=1024,
        description="Maximum number of tokens to generate. A word is generally 2-3 tokens (minimum: 1)",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="The temperature to use for the model.",
    )
    n_gpu_layers: int = Field(
        default=0,
        ge=-1,
        le=100,
        description="Number of layers to offload to GPU (-ngl). If -1, all layers are offloaded.",
    )
    top_k: int = Field(
        default=50,
        ge=1,
        le=100,
        description="The number of highest probability tokens to keep for top-k sampling.",
    )
    top_p: float = Field(
        default=0.95,
        ge=0.0,
        le=1.0,
        description="The cumulative probability cutoff for nucleus/top-p sampling.",
    )
    grammar: str = Field(
        default="",
        description="The grammar to use for the model. If empty, no grammar is used.",
    )
    is_json_schema: bool = Field(
        default=False,
        description="Whether the grammar is a JSON schema. If true, the grammar is used as a JSON schema.",
    )

    @validator("model", pre=True)
    def validate_model(cls, v):
        if isinstance(v, str):
            v = LlamaFile(name=v)
        if isinstance(v, dict):
            v = LlamaFile(**v)
        if v.name == "":
            raise ValueError("The model cannot be empty.")
        return v

    async def process(self, context: ProcessingContext) -> str:
        from llama_cpp import LlamaGrammar

        if self.grammar != "":
            if self.is_json_schema:
                grammar = LlamaGrammar.from_json_schema(self.grammar)
            else:
                grammar = LlamaGrammar.from_string(self.grammar)
        else:
            grammar = None

        llm = context.load_model(
            "llama", self.model.name, n_gpu_layers=self.n_gpu_layers
        )

        res = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {"role": "user", "content": self.prompt},
            ],
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            grammar=grammar,
        )
        return str(res["choices"][0]["message"]["content"])  # type: ignore
