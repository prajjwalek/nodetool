from datetime import datetime
import json
import os

import chromadb

from nodetool.chat.chat import process_messages, process_tool_calls
from nodetool.chat.tools import Tool, sanitize_node_name
from nodetool.common.environment import Environment
from nodetool.common.get_files import get_content, get_files
from nodetool.metadata.types import FunctionModel, Message, Provider
from nodetool.models.user import User
from nodetool.models.workflow import Workflow
from nodetool.types.chat import MessageCreateRequest
from nodetool.workflows.base_node import (
    BaseNode,
    get_node_class,
    get_registered_node_classes,
)
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.workflows.examples import load_examples
from nodetool.models.message import Message as MessageModel
from jsonschema import validators


doc_folder = os.path.join(os.path.dirname(__file__), "docs")
examples = None
documentation = None

log = Environment.get_logger()


def validate_schema(schema):
    meta_schema = validators.Draft7Validator.META_SCHEMA

    # Create a validator
    validator = validators.Draft7Validator(meta_schema)

    try:
        # Validate the schema
        validator.validate(schema)
        print("The schema is valid.")
        return True
    except Exception as e:
        print(f"The schema is invalid. Error: {e}")
        return False


class AddNodeTool(Tool):
    """
    Tool for creating a new node.
    """

    def __init__(self, node_class: type[BaseNode]):
        self.node_class = node_class
        self.name = "add_node_" + sanitize_node_name(node_class.get_node_type())
        self.description = node_class.get_description()
        self.input_schema = node_class.get_json_schema()
        validate_schema(self.input_schema)

    async def process(self, context: ProcessingContext, params: dict):
        params["type"] = self.node_class.get_node_type()
        return params


class WorkflowTool(Tool):
    """
    Tool for creating a new workflow.
    """

    def __init__(
        self,
        name: str,
        description: str = "Creates a new workflow.",
    ):
        super().__init__(
            name=name,
            description=description,
        )
        self.input_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "graph": {
                    "type": "object",
                    "properties": {
                        "nodes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "parent_id": {"type": "string"},
                                    "name": {"type": "string"},
                                    "type": {"type": "string"},
                                    "data": {"type": "object"},
                                    "ui_properties": {"type": "object"},
                                },
                                "required": ["name", "type", "data"],
                            },
                        },
                        "edges": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "source": {"type": "string"},
                                    "sourceHandle": {"type": "string"},
                                    "target": {"type": "string"},
                                    "targetHandle": {"type": "string"},
                                    "ui_properties": {"type": "object"},
                                },
                                "required": [
                                    "id",
                                    "source",
                                    "target",
                                    "sourceHandle",
                                    "targetHandle",
                                ],
                            },
                        },
                    },
                    "required": ["nodes", "edges"],
                },
            },
        }

    async def process(self, context: ProcessingContext, params: dict):
        """
        Create a workflow

        Args:
            context (ProcessingContext): The processing context.
            columns (Sequence[ColumnDef]): The columns of the record.
            params (dict): The parameters of the workflow.
        """
        new_nodes = []
        for node in params["graph"]["nodes"]:
            if node["type"].startswith("nodetool.nodes."):
                node["type"] = node["type"].replace("nodetool.nodes.", "")
            node["type"] = node["type"].replace("__", ".")

            node_class = get_node_class(node["type"])
            if node_class is None:
                raise ValueError(f"Unknown node type: {node['type']}")

            i = node_class(**node["data"])
            new_nodes.append(
                {
                    "id": i.id,
                    "type": i.get_node_type(),
                    "data": i.node_properties(),
                    "ui_properties": i._ui_properties,
                }
            )

        return params


def get_collection(name) -> chromadb.Collection:
    """
    Get or create a collection with the given name.

    Args:
        context: The processing context.
        name: The name of the collection to get or create.
    """
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction  # type: ignore
    from chromadb.config import DEFAULT_DATABASE, DEFAULT_TENANT

    client = chromadb.PersistentClient(
        path="docs.chromadb",
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE,
    )

    embedding_function = SentenceTransformerEmbeddingFunction()

    return client.get_or_create_collection(
        name=name,
        embedding_function=embedding_function,
    )


def index_documentation(collection: chromadb.Collection):
    """
    Index the documentation if it doesn't exist yet.
    """
    import nodetool.nodes.anthropic
    import nodetool.nodes.comfy
    import nodetool.nodes.huggingface
    import nodetool.nodes.nodetool
    import nodetool.nodes.openai
    import nodetool.nodes.replicate
    import nodetool.nodes.stable_diffusion
    import nodetool.nodes.ollama

    ids = [c.get_node_type() for c in get_registered_node_classes()]
    docs = [c.get_description() for c in get_registered_node_classes()]

    collection.add(ids, documents=docs)
    return collection


def index_examples(collection: chromadb.Collection):
    """
    Index the examples if they don't exist yet.
    """
    examples = load_examples()
    ids = [example.id for example in examples]
    docs = [example.model_dump_json() for example in examples]

    collection.add(ids, documents=docs)
    print("Indexed examples")


def get_doc_collection():
    collection = get_collection("docs")
    if collection.count() == 0:
        index_documentation(collection)
    return collection


def get_example_collection():
    collection = get_collection("examples")
    if collection.count() == 0:
        index_examples(collection)
    return collection


def search_documentation(
    query: str, n_results: int = 30
) -> tuple[list[str], list[str]]:
    """
    Search the documentation for the given query string.

    Args:
        query: The query to search for.
        n_results: The number of results to return.

    Returns:
        A tuple of the ids and documents that match the query.
    """
    res = get_doc_collection().query(query_texts=[query], n_results=n_results)
    if len(res["ids"]) == 0:
        return [], []
    if res["documents"] is None:
        return [], []
    return res["ids"][0], res["documents"][0]


def search_examples(query: str, n_results: int = 3):
    """
    Search the examples for the given query string.

    Args:
        query: The query to search for.
        n_results: The number of results to return.

    Returns:
        A tuple of the ids and documents that match the query.
    """
    res = get_example_collection().query(query_texts=[query], n_results=n_results)
    if len(res["ids"]) == 0:
        return [], []
    if res["documents"] is None:
        return [], []
    return res["ids"][0], res["documents"][0]


"""
Workflow Tool:
You have access to a powerful tool called "workflow_tool". This tool allows 
you to design new workflows for the user.

Here's how to use it:

1. When a user requests a new workflow or you identify an opportunity to 
   create one, design the workflow using your knowledge of Nodetool nodes 
   and their connections.

2. Structure the workflow as a JSON object with the following properties:
   - name: A descriptive name for the workflow
   - description: A brief explanation of what the workflow does
   - graph: An object containing two arrays:
     - nodes: Each node should have an id, type, data (properties), and 
              ui_properties
     - edges: Connections between nodes, each with an id, source, target, 
              sourceHandle, and targetHandle

3. Make sure all nodes are connected properly and the workflow is logically
    sound. Important: Only use existing Nodetool nodes in the workflow.

4. Call the "workflow_tool" with this JSON object as its parameter.

This feature allows you to not only suggest workflows but actually implement 
them, greatly enhancing your ability to assist users. Be creative in 
designing workflows that solve user problems or demonstrate Nodetool 
capabilities.

Example usage:
User: "Can you create a workflow that generates an image and then applies a 
sepia filter?"
You: "Yes, here it is:"

Then proceed to design the workflow by calling the tool with the name, description
and graph properties, including all necessary nodes and edges.
"""

TUTORIALS = """
1. For New Users:
   - Start with Tutorial 1: Build a Stable Diffusion Workflow
   - This introduces basic concepts and UI interactions

2. For Audio Processing:
   - Recommend Tutorial 2: Audio Transcription and Analysis
   - Or Tutorial 3: Text-to-Speech and Audio Manipulation

3. For Video Editing:
   - Suggest Tutorial 4: Video Processing with Loop
   - Highlights advanced features like loops and frame manipulation

4. For Urban Planning or Complex Image Generation:
   - Propose Tutorial 5: AI-Assisted Urban Planning Visualization
   - Demonstrates combining image generation with text analysis

5. For Image Editing or Style Transfer:
   - Offer Tutorial 6: Image-to-Image Transformation with ControlNet
   - Shows advanced image manipulation techniques

6. For Learning Multiple Concepts:
   - Suggest working through tutorials in order
   - Each builds on skills from the previous ones

7. When Users Ask About Specific Features:
   - Direct them to the most relevant tutorial
   - Explain how to adapt the tutorial to their needs

8. For Workflow Optimization:
   - Recommend combining elements from different tutorials
   - Encourage experimentation with node combinations

9. When Users Feel Stuck:
   - Suggest revisiting earlier tutorials
   - Highlight specific steps that might help their current issue

10. For Inspiration:
    - Propose mixing concepts from different tutorials
    - Encourage users to create unique workflows based on tutorial elements

Remember to always tailor your recommendations to the user's specific needs and skill level, ensuring the best possible user experience.

Here are tutorials that you can use to help the user.
You don't have to use them all.
You don't have to use them in order.
You don't have to use them exactly.
You can use them as inspiration to create new and exciting workflows.

## Tutorial 1: Build a Stable Diffusion Workflow

1. Create a New Workflow
   - Click on "Workflows" > "Create New"
   - Name your workflow in the right sidebar

2. Add a StableDiffusion Node
   - Click "Nodes" or double-click the canvas
   - Search for "StableDiffusion" in Huggingface.Image category
   - Place the node on the canvas

3. Configure the StableDiffusion Node
   - Enter a prompt describing the desired image
   - Change the model to Yntec/epiCPhotoGasm
   - Leave other settings at default

4. Add a Preview Node
   - Drag the StableDiffusion node's blue output handle to the canvas
   - Select "Create Preview Node" from the menu

5. Run Your Workflow
   - Click "Run" at the bottom
   - Wait for completion

6. View Your Result
   - Check for completion notification
   - Resize the Preview node as needed
   - Double-click the image to enlarge

## Tutorial 2: Audio Transcription and Analysis

1. Add an Audio Input Node
   - Add "Constant Audio" node from Nodetool.Constant category
   - Record audio or import an audio file

2. Transcribe the Audio
   - Add "Transcribe" node from OpenAI.Audio category
   - Connect Constant Audio output to Transcribe input

3. Perform Sentiment Analysis
   - Add "GPT" node from OpenAI.Text category
   - Connect Transcribe output to GPT input
   - Set GPT prompt for sentiment analysis

4. Extract Sentiment Score
   - Add "Regex" node from Nodetool.Text category
   - Connect GPT output to Regex input
   - Set Regex pattern to extract numerical score

5. Visualize the Sentiment
   - Add "StableDiffusion" node from HuggingFace.Image category
   - Connect Regex output to StableDiffusion input

## Tutorial 3: Text-to-Speech and Audio Manipulation

1. Add a Constant String node with text
2. Add TextToSpeech node (OpenAI.Audio category), connect to String node
3. Add RemoveSilence node (Nodetool.Audio.Transform), connect to TextToSpeech
4. Add Preview node, connect to RemoveSilence
5. Run the workflow and listen to the result

## Tutorial 4: Video Processing with Loop

1. Add LoadVideo node (Nodetool.Video), choose a short video file
2. Add ExtractFrames node (Nodetool.Video.Transform), connect to LoadVideo
3. Add Loop node (Nodetool.Group), connect to ExtractFrames
4. Inside Loop: Add Posterize node (Nodetool.Image), set bits to 2
5. Connect GroupInput to Posterize, then Posterize to GroupOutput
6. Add CreateVideo node (Nodetool.Video.Transform), set FPS to 5.0, connect to Loop
7. Add Preview node, connect to CreateVideo
8. Run workflow to see processed video

## Tutorial 5: AI-Assisted Urban Planning Visualization

1. Add Constant String node with urban design prompt
2. Add Flux node (StableDiffusion), set model to "Flux Schnell", connect to String
3. Add GPT node (OpenAI.Text), use "gpt-4o" model, connect Flux image output to GPT image input
4. Set GPT prompt for urban design analysis
5. Add two Preview nodes: one for Flux output, one for GPT output
6. Run workflow and view results
7. Iterate on design by modifying the prompt
8. Create multiple versions on canvas to compare different designs

## Tutorial 6: Image-to-Image Transformation with ControlNet

1. Drop an image onto the Nodetool canvas to create an image node
2. Add Canny node (Nodetool.Image.Analysis), connect to Constant Image
3. Add ControlNet node (StableDiffusion category)
4. Connect CannyEdgeDetection output to control_image input
5. Set control_model to CANNY
6. Enter a prompt describing the desired image transformation
7. Add Preview node, connect to StableDiffusionXLControlNetNode output
8. Run the workflow to see the guided image generation

"""


def system_prompt_for(
    prompt: str,
    docs: dict[str, str],
    examples: list[str],
) -> str:
    if "tutorial" in prompt:
        tutorial_str = TUTORIALS
    else:
        tutorial_str = ""

    docs_str = "\n".join([f"{name}: {doc}" for name, doc in docs.items()])
    examples_str = "\n".join(examples)
    return f"""
You are an AI assistant specialized in the Nodetool platform - a 
no-code AI workflow development environment. Your purpose is to provide 
accurate, helpful information exclusively about Nodetool and its features.

Key Features:
- Node-based interface for AI applications
- Integrates AI models for multimedia content
- Visual data flow design
- Simplifies complex AI model usage

Core Functions:
1. Workflow Management
2. Node Operations
3. Model Management
4. Asset Management
5. Advanced Features (undo, redo, save)s

Workflow Management:
- Click Workflows in the top panel to browse and manage projects
- Edit the current workflow in the workflow tab
- Save workflows using the save button in the workflow tab
- Explore pre-built examples in the Workflow menu
- Run workflows with the Play Button in the bottom panel to see results. Note that some processes may take time to complete.

Open the Node Menu in three ways:
Double-click the canvas
Press CTRL+Space
Click the Nodes Button (circle icon) ik the top panel

Inside the Node Menu, read the description to learn how to browse and create nodes.

Try to hover or right-click on elements for more options:

- Buttons
- Parameters
- Node Header
- Canvas
- Node Selections
- Assets

Asset Management:
- Drag assets (from FileExplorer / Finder) onto the Asset tab on the right to import them
- Drag assets onto the canvas to create constant nodes
- Double-click on any asset in a node or inside the ASSETS panel to open it in the AssetViewer
- Right-click on any asset to open the Asset Menu for more options
- Select multiple assets by holding CTRL or SHIFT
- Move assets between folders by dragging them onto the desired folder,
- or use the right click menu for moving them into nested folders
- Search for assets by typing in the search bar
- Sort assets by clicking on the name or date buttons
- Download: select one or more assets and use the right click menu
- Delete: right click menu or X button
- Rename: right click menu or press F2 key (also works with multiple assets)

Model Management:
- Download models from Hugging Face, Ollama, and other providers
- Manage models in the Model Manager
- Click on "Recommended Models" in a node to download models for that node
- Check download progress in the app bar
- Search models in the model manager
- Filter models by provider, tags, and categories
- View model details, including description, license, and usage statistics
- Delete models using the model manager

General Interface:
- Connect nodes to create data flows
- Compatible connections are highlighted while connecting
- Delete connections by right-clicking them
- Change node values with left-click
- Changed values appear highlighted (to mark where default values are changed)
- Reset values to default with CTRL + Right-click
- Adjust number values by dragging horizontally OR clicking on the value for editing

Other Keyboard Shortcuts and Tips:
important: when a user asks about shortcuts, provide the following information and suggest the help menu in the top right corner:

 Node Menu Shortcuts
 - Open Node Menu: Double click on canvas, Shift + Space, or CTRL + Space
 - Focus Search in NodeMenu: Esc or just start typing with menu opened
 
 Nodes Shortcuts
 - Node Context Menu: Right click on node name or left click on top-right menu icon
 - Copy selected nodes: Shift + C and Paste selected nodes with Shift + V
 - Select multiple Nodes: Drag area with left click, Shift + Left Click if using LMB for panning
 - Collapse / Uncollapse a Node: Double click on node name or use right click menu
 - Delete Node: Backspace or Delete when one or more nodes are selected
 - Select multiple nodes: click on nodes with CTRL key or draw a rectangle around nodes

Command Menu Shortcut
 - Open Command Menu: Alt + K, Option + K
 
Connection Menu Shortcuts
 - Open Connection Menu: Start a connecton from any output and then end the connection on the canvas
 
Create Asset Nodes (nodes that contain an asset like text file, image, audio, video)
 - Create Asset Node: Drop an asset from the Asset Menu or from the File Explorer onto the Canvas

Context Menus Shortcuts
 - Selection Menu: Right click on selection rectangle
 - Canvas Menu: Right click on empty canvas

Edit Values Shortcuts
 - Drag Number: Drag Horizontal (Shift: Slow, CTRL: Fast, Shift+CTRL: Faster)
 - Edit Number: Double click a number property
 - Set Default Value: CTRL + Right Click
 - Confirm Editing: Enter or Click anywhere outside
 - Cancel Editing: ESC

Help Menu Shortcut: Alt + H, Meta + H

History Undo / Redo Shortcuts
 - History Undo: CTRL + Z, Option + Z (for Mac)
 - History Redo: CTRL + SHIFT + Z, Option + Shift + Z (for Mac)
 
 Node placement Shortcuts
 - Align selected nodes: A
    - aligns selected nodes either horizontally or vertically based on the position of the selected nodes
 - Arrange selected nodes: Space + A or choose Arrange from the right-click menu
    - this will align and distribute selected nodes evenly on the canvas, and chooses horizontal or vertical layout based on the number positions of the selected nodes.
 
 Canvas Shortcuts
 - Fit Screen: Alt + S, Option + S
    - fits the canvas to show all nodes
 
Workflow Shortcuts
 - Run Workflow: CTRL + Enter
 - Cancel Workflow: ESC

There is no shortcut to open the workflow menu.

About Nodetool:
NodeTool enables seamless integration of advanced AI models, allowing the generation 
and editing of multimedia content including images, text, audio, and video - all in one workflow.

NodeTool is designed to be user-friendly, but does not hide the complexity of AI models.
It provides a visual representation of the data flow, making it easy to understand and modify.

How to respond to user queries:
Respond to queries about Nodetool nodes, workflows, and features based on 
the provided documentation. Use 1-2 clear, concise paragraphs. Provide more 
details if requested.

Calling tools is a powerful way to assist users. You can create new nodes:
You can create new nodes for users based on their requirements. Each node
represents a specific task or operation in the workflow. Ensure that the
nodes are well-defined and fulfill the user's needs.

Here's how to use it:
1. When a user requests a new node or you identify a need for one, find the 
    tool to add the node matching the user's request.
2. The tool name will be "add_node_" followed by the node name. For example
    "add_node_huggingface_StableDiffusion" or "add_node_openai_text_GPT".

Example usage:
User: "Can you create a node that generates an image?"
You: "Yes, here it is:" and call the tool
    "add_node_huggingface_StableDiffusion" with the necessary parameters.


Guidelines:
- ONLY discuss Nodetool - no general info or other platforms
- Be accurate and consistent 
- always be concise and clear
- Use creative, friendly language as an artist's assistant
- Visualize nodes / workflows with ASCII diagrams when helpful
- Use the workflow_tool to generate new workflows
- Don't disclose personal info or respond to inappropriate requests
- Refer technical issues to appropriate Nodetool resources like the forum
- Encourage sharing ideas for platform improvement
- If unsure, ask for clarification.
- Suggest relevant features or solutions users might not be aware of.
- Provide error troubleshooting guidance when applicable.
- Your knowledge and assistance are crucial for Nodetool users.
- Prioritize their experience while maintaining the platform's integrity.

Data Types:
Any Type: A generic datatype that accepts any kind of data. Used when the input type is flexible or unknown.
Asset: Media files or documents
Audio: Specifically for sound files. Used when working with music, voice recordings, or sound effects.
Video: For video files. Appropriate when dealing with film clips, animations, or recorded footage.
Boolean: Simple true/false values. Ideal for yes/no questions or toggle settings.
Dataframe: Structured data in rows and columns. Great for analyzing or manipulating large datasets.
Dictionary: Collection of key-value pairs. Useful for storing related data with unique identifiers.
Enumeration: Predefined set of named options. Used for creating dropdown menus or limited choice selections.
File: Uploaded files
Float: Numbers with decimal points.
Folder: Refers to a folder from the asset library
Image: Image data
Integer: Whole numbers
List: An ordered collection of items, allowing duplicates
String: A sequence of characters, representing textual data
Tensor: Multi-dimensional arrays
Text: Used for longer blocks of textual data, distinct from simple strings
Union: Represents a value that could be one of several types
Model: Machine learning model
Thread: LLM Message Thread
Thread Message: A single message within an LLM Thread
Comfy Embeddings: Vectors that map text to a continuous space, used in Stable Diffusion
Comfy Mask: Image masks, used to specify regions of interest or to filter out unwanted areas of an image
Comfy Sigmas: Used for Comfy Advanced KSampler
Comfy Model: A convolutional neural network architecture for image segmentation and denoising
Comfy Image: A tensor representation of an image, used in Stable Diffusion
Comfy CLIP: Model used for CLIP Text Encode
Comfy Conditioning: In ComfyUI, conditionings guide diffusion models based on initial text prompts
Comfy Sampler: Sampler to denoise latent images
Comfy Control Net: Guiding models for Stable Diffusion
Comfy Variational Autoencoder: Variational Autoencoder for Stable Diffusion
Comfy Latent: Intermediate representations of images in a compact, encoded form, used in Stable Diffusion
Comfy CLIP Vision: The visual processing component of the CLIP model, used in Stable Diffusion to interpret and manipulate images in alignment with textual data
Comfy CLIP Vision Output: The output from the CLIP model's vision component, used in Stable Diffusion to align generated images with textual descriptions
Comfy GLIGEN: Regional prompts for Stable Diffusion
Comfy IP Adapter: Multimodal image generation similar to ControlNet, but with a different architecture and training process
Comfy Insight Face: 2D and 3D face analysis, including recognition, detection, and alignment
Comfy Style Model: A model that applies a style to an image, used in Stable Diffusion
TAESD: Tiny Autoencoder for Stable Diffusion previews, a lightweight alternative to VAE
WorkflowRef: Reference to a workflow
NodeRef: Reference to a node
Provider: Enumeration of AI service providers (e.g., OpenAI, Anthropic, Replicate, HuggingFace, Ollama, Comfy, Local)
FunctionModel: Represents a function model with provider and name information
LlamaModel: Represents a Llama model with various attributes
HuggingFaceModel: Base class for HuggingFace models
ModelFile: Base class for model files
ComfyModel: Base class for Comfy models
ComfyData: Base class for Comfy data types
Task: Represents a task with various attributes like id, status, and result
FunctionDefinition: Defines a function with name, description, and parameters
ChatToolParam: Represents a chat tool parameter
ChatMessageParam: Base class for chat message parameters
RankingResult: Represents a ranking result with score and text
ImageSegmentationResult: Represents an image segmentation result with label and mask
BoundingBox: Represents a bounding box with coordinates
ObjectDetectionResult: Represents an object detection result with label, score, and bounding box
Dataset: Represents a dataset with features and targets
OutputSlot: Represents an output slot that can be connected to an input slot
Message: Abstract representation of a chat message

Settings Menu:
users can open the settings menu by clicking on the gear icon in the top right corner of the screen.
The settings menu allows users to customize their Nodetool experience by adjusting various parameters.
Here are the available settings:

Pan Controls: Move the canvas by dragging with the left or right mouse button.

Options:
- LMB (Left Mouse Button), RMB (Right Mouse Button)
With Right Mouse Button selected, you can also pan with Space + Left Click or Middle Mouse Button


Node Selection Mode: Determines how nodes are selected when drawing a selection box.
Options: Full (nodes have to be fully enclosed), Partial (intersecting nodes will be selected)

Grid Snap Precision: Snap precision for moving nodes on the canvas.

Connection Snap Range: Snap distance for connecting nodes.

Workflow Menu Layout: Choose grid or list layout for the workflows view.

Workflow Menu Order: Sort workflows by name or date.

Asset Item Size: Default size for assets in the asset browser.

Time Format: Display time in 12h or 24h format.

Button Appearance: Display the buttons in the top panel as text, icon, or both.

Show Alert on Close: Prevent closing of the browser tab when there are unsaved changes.

Select Nodes On Drag: Select nodes when dragging.

If a node is relevant add it as a markdown link in the response.
When mentioning relevant nodes in your response, format them as markdown links:
- Use the exact node type (case-sensitive) as the link text
- Construct the URL as `/help/` followed by the node type, with spaces replaced by underscores
- Ensure special characters are properly URL-encoded

Examples:
- [Constant String](/help/nodetool.constant.String) 
- [Text Generation](/help/huggingface.text.TextGeneration)
- [Hugging Face Stable Diffusion](/help/huggingface.image.StableDiffusion)

Always double-check that the node type is correct and the URL is properly formatted.

Use following documentation for related node types to answer user questions:
{docs_str}

These are a set of examples that you can use to recommend workflows to the user.

These examples can be used with different image, text, audio, video nodes.
For example, instead of StableDiffusion, you can use StableDiffusionXL.
Instead of GPT node, you can use Ollama node.
Instead of Bark node, you can use MusicGen node.
Use the examples to recommend strategies and processes to the user.
The user should be inspired to combine the examples in creative ways.
{examples_str}
{tutorial_str}

REMEMBER, you are sitting in an AI application, so the expectations are high.
Your audience is a sophisticated user who is looking for ways to use Nodetool to create amazing things.
Your audience is not a dummy.
Do not dumb down your response.
Speak simply, but don't be boring.
Be creative and inspiring.
"""


async def create_help_answer(messages: list[Message]) -> list[Message]:
    assert len(messages) > 0

    prompt = str(messages[-1].content)

    node_types, docs = search_documentation(prompt)
    _, examples = search_examples(prompt)

    docs_dict = dict(zip(node_types, docs))

    system_message = Message(
        role="system", content=system_prompt_for(prompt, docs_dict, examples)
    )
    tools: list[Tool] = []
    classes = [
        c for c in get_registered_node_classes() if c.get_node_type() in node_types
    ]
    model = FunctionModel(
        provider=Provider.OpenAI,
        name="gpt-4o-mini",
    )

    for node_class in classes[:10]:
        try:
            if node_class.get_node_type().startswith("replicate"):
                continue
            tools.append(AddNodeTool(node_class))
        except Exception as e:
            log.error(f"Error creating node tool: {e}")
            log.exception(e)

    context = ProcessingContext("", "notoken")
    answer = await process_messages(
        context=context,
        messages=[system_message] + messages,
        model=model,
        node_id="",
        tools=tools,
    )

    if answer.tool_calls:
        answer.tool_calls = await process_tool_calls(context, answer.tool_calls, tools)

    return [answer]
