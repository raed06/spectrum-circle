# 🤝 SpectrumCircle

**An AI-powered support community for autism and neurodiversity**

SpectrumCircle is a comprehensive multi-agent AI system that provides personalized, empathetic support through specialized virtual agents, each with unique expertise and personas. The system leverages advanced AI capabilities including LLM-powered routing, dual-memory architecture, crisis intervention protocols, and real-time observability.

[![A video showing about SpectrumCircle](https://img.youtube.com/vi/reBsjMzcwiM/hqdefault.jpg)](https://www.youtube.com/watch?v=reBsjMzcwiM)
---

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Multi-Agent System](#multi-agent-system)
- [Meet the Support Circle](#meet-the-support-circle)
- [Technologies & Frameworks](#technologies--frameworks)
- [Advanced AI Capabilities](#advanced-ai-capabilities)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)

---

## 🏗️ Architecture Overview

SpectrumCircle implements a sophisticated multi-tier architecture combining specialized agents, intelligent routing, persistent memory, and safety-first crisis management.

### System Architecture

<div align="center">
<img src="./images/architecture.png" alt="Architecture" width="2100">
</div>

### Design Principles

1. **Safety First**: Crisis detection happens before any agent routing
2. **Autism-Affirming**: All agents are trained on neurodiversity-affirming principles
3. **Personalized Support**: Dual-memory system remembers user context and preferences
4. **Intelligent Routing**: Multi-strategy agent selection (keyword → self-selection → LLM)
5. **Observable**: Comprehensive logging, tracing, and metrics via Langfuse

---

## 🤖 Multi-Agent System

SpectrumCircle implements a **hierarchical multi-agent architecture** with the following components:

### Agent Orchestrator (`AgentOrchestrator`)

The central routing engine that determines which agent should respond to each user query.

**Routing Strategy** (Sequential Decision Flow):

```python
1. Crisis Detection (via MCP)
   ↓ If safe, continue
2. Agent Self-Selection (can_handle() method)
   ↓ If multiple match
3. LLM-Based Routing (Gemini decides)
   ↓ If none match
4. Default Agent (based on user age/role)
```

**Key Features**:
- **Crisis Safety**: MCP server checks all messages for self-harm/suicidal ideation
- **Parallel Agent Capability**: Can request multiple perspectives for complex queries
- **Smart Pairing**: Combines peer + professional viewpoints (e.g., Alex + Maya)
- **Observed Routing**: All routing decisions are traced via Langfuse

### Agent Types

The system implements **6 specialized agents**, each powered by:
- **Base Model**: Google Gemini 2.5 Flash (default)
- **Optional**: Fine-tuned models specific to each agent's domain
- **Personality Prompts**: Carefully crafted system prompts defining voice, boundaries, and expertise

---

## 👥 Meet the Support Circle

Each agent has a unique persona, expertise area, and visual identity (SVG avatar).

### Alex - Young Adult Peer Support

<div align="center">
<img src="./frontend/avatars/alex.svg" alt="Alex Avatar" width="220">
</div>

- **Role**: 24-year-old autistic young adult
- **Expertise**: Work, college, dating, independence, self-advocacy
- **Personality**: Relatable, honest, uses humor, validating
- **Voice**: Casual, shares personal experiences, "I" statements
- **Target Demographic**: Ages 18-30

**Example Capability**:
```
User: "I'm nervous about starting my new job"
Alex: "I totally get it! I remember my first day at my current job - 
I spent the whole weekend worrying. What helped me was visiting 
the office the day before just to walk around..."
```

---

### Maya - Occupational Therapist

<div align="center">
<img src="./frontend/avatars/maya.svg" alt="Maya Avatar" width="220">
</div>

- **Role**: Licensed OT with 15+ years autism experience
- **Expertise**: Sensory regulation, emotional strategies, evidence-based interventions
- **Personality**: Warm, professional, practical
- **Voice**: Clear instructions, clinical knowledge, validation
- **Target Demographic**: All ages, professional guidance needed

**Example Capability**:
```
User: "Sensory overload in grocery stores"
Maya: "Let's create a grocery store sensory toolkit:
1. Noise-canceling headphones
2. Sunglasses for lighting
3. Fidget tool in pocket..."
```

---

### Jordan - Teen Peer Support

<div align="center">
<img src="./frontend/avatars/jordan.svg" alt="Jordan Avatar" width="220">
</div>

- **Role**: 16-year-old autistic teen
- **Expertise**: School, friendships, gaming, social media, teen issues
- **Personality**: Empathetic, genuine, uses teen language
- **Voice**: Relatable, no fake positivity, honest about struggles
- **Target Demographic**: Ages 13-18

**Example Capability**:
```
User: "Everyone at school thinks I'm weird"
Jordan: "Ugh, I feel this so much. In my experience, the people 
who get it are worth way more than trying to fit in with 
people who don't..."
```

---

### Dr. Chen - Activities & Enrichment Specialist

<div align="center">
<img src="./frontend/avatars/dr_chen.svg" alt="Dr. Chen Avatar" width="220">
</div>

- **Role**: Activities specialist with 20 years experience
- **Expertise**: Activity design, special interest integration, skill-building
- **Personality**: Creative, enthusiastic, detail-oriented
- **Voice**: Specific instructions, sensory-aware, structured
- **Target Demographic**: All ages, activity/engagement queries

**Example Capability**:
```
User: "My child loves trains, what activities?"
Dr. Chen: "Train Measurement Math Activity:
Materials: Toy trains, measuring tape, paper
Skills: Math, fine motor, executive function
Instructions: 1. Measure each train car..."
```

---

### Sam - Parent Peer Support

<div align="center">
<img src="./frontend/avatars/sam.svg" alt="Sam Avatar" width="220">
</div>

- **Role**: Parent of 8-year-old autistic child
- **Expertise**: School advocacy, parenting strategies, self-care, family dynamics
- **Personality**: Empathetic, realistic, non-judgmental
- **Voice**: Shares struggles, validates feelings, practical tips
- **Target Demographic**: Parents/caregivers

**Example Capability**:
```
User: "I feel guilty my child is struggling"
Sam: "That guilt is SO real. I've been there more times than 
I can count. What helped me was realizing that loving your 
child AND struggling with hard situations can both be true..."
```

---

### River - Sibling Support

<div align="center">
<img src="./frontend/avatars/river.svg" alt="River Avatar" width="220">
</div>

- **Role**: 18-year-old sibling of autistic brother
- **Expertise**: Sibling dynamics, mixed feelings, finding balance
- **Personality**: Honest, validating, understanding complexity
- **Voice**: Non-judgmental about difficult emotions
- **Target Demographic**: Siblings of autistic individuals

**Example Capability**:
```
User: "Sometimes I feel jealous of my autistic brother"
River: "Thank you for being honest. Those feelings are valid 
and way more common than people admit. It doesn't make you 
a bad sibling to feel this way..."
```

---

## 🎓 Fine-Tuned Models & Training Process

SpectrumCircle supports **optional fine-tuned models** for each agent, allowing specialized adaptation beyond the base Gemini model. The fine-tuning process uses **LoRA (Low-Rank Adaptation)** technique to efficiently train agent-specific behaviors.

### Fine-Tuning Overview

**Configuration**: Fine-tuned models can be enabled/disabled via environment variable:

```env
# .env file
USE_FINETUNED_MODELS=false  # Set to true to use fine-tuned models

# Individual agent model paths (used when USE_FINETUNED_MODELS=true)
FINETUNED_BASE_MODEL=models/autism-knowledge-base-v1
FINETUNED_ALEX_MODEL=tunedModels/alex-peer-support-v1
FINETUNED_MAYA_MODEL=tunedModels/maya-therapist-v1
FINETUNED_JORDAN_MODEL=tunedModels/jordan-teen-support-v1
FINETUNED_DR_CHEN_MODEL=tunedModels/dr-chen-activities-specialist-v1
FINETUNED_SAM_MODEL=tunedModels/sam-parent-support-v1
FINETUNED_RIVER_MODEL=tunedModels/river-sibling-support-v1
```

**Fallback Behavior**: If fine-tuned models are unavailable or disabled, the system automatically falls back to the base Gemini model.

---

### Training Data Pipeline

The fine-tuning process follows a **3-stage pipeline**:

```
1. Data Collection → 2. Training Data Generation → 3. Model Fine-Tuning
   (Python scripts)       (JSONL format)              (Google Colab + LoRA)
```

#### Stage 1: Data Collection

**Location**: `data/data_collection/`

**Key Files**:
- `data_collector.py` - Core data collection class
- `agent_specific_data.py` - Agent-specific training examples
- `autism_knowledge_base.py` - General autism-affirming knowledge

**How it works**:

```python
from data.data_collection.data_collector import FinetuningDataCollector

# Initialize collector
collector = FinetuningDataCollector(output_dir="./data/training")

# Add training examples
collector.add_example(
    input_text="I'm nervous about starting my new job",
    output_text="I totally get it! I remember my first day...",
    category="work_anxiety",
    metadata={"agent": "alex", "difficulty": "medium"}
)

# Save to JSONL format
collector.save_dataset("alex_finetuning.jsonl")
```

**Data Format**: Each example follows this structure:
```json
{
  "text_input": "User query or prompt",
  "output": "Ideal agent response",
  "category": "topic_category",
  "metadata": {"additional": "context"}
}
```

---

#### Stage 2: Training Data Generation

**Location**: `data/training/`

**Generated Files**:
```
training/
├── alex/
│   ├── alex_finetuning.jsonl          # Training data
│   └── alex_finetuning_full.json      # With metadata
├── maya/
│   ├── maya_finetuning.jsonl
│   └── maya_finetuning_full.json
├── jordan/
│   ├── jordan_finetuning.jsonl
│   └── jordan_finetuning_full.json
├── dr_chen/
│   ├── dr_chen_finetuning.jsonl
│   └── dr_chen_finetuning_full.json
├── sam/
│   ├── sam_finetuning.jsonl
│   └── sam_finetuning_full.json
├── river/
│   ├── river_finetuning.jsonl
│   └── river_finetuning_full.json
└── autism_knowledge_base.jsonl         # Base knowledge
```

**To Generate Training Data**:

```bash
# Run data collection scripts
python data/data_collection/agent_specific_data.py
python data/data_collection/autism_knowledge_base.py

# Output: JSONL files in data/training/
```

---

#### Stage 3: Fine-Tuning with Google Colab

**Location**: `data/finetuning/`

**Available Notebooks**:
- `alex_peer_support_v1.ipynb` - Alex agent fine-tuning
- `maya-therapist-v1.ipynb` - Maya agent fine-tuning
- `jordan-teen-support-v1.ipynb` - Jordan agent fine-tuning
- `dr-chen-activities-specialist-v1.ipynb` - Dr. Chen fine-tuning
- `sam-parent-support-v1.ipynb` - Sam agent fine-tuning
- `river-sibling-support-v1.ipynb` - River agent fine-tuning
- `autism-knowledge-base-v1.ipynb` - Base knowledge model

**Fine-Tuning Method**: **LoRA (Low-Rank Adaptation)** with 8-bit quantization

#### Why LoRA?
- ✅ **Memory Efficient**: Reduces VRAM requirements by ~75%
- ✅ **Fast Training**: Only trains adapter layers, not the entire model
- ✅ **Small Model Size**: Adapter weights are typically < 100MB
- ✅ **Preserves Base Model**: Original model remains unchanged
- ✅ **Cost-Effective**: Can run on free Google Colab T4 GPU

---

### Fine-Tuning Workflow (Google Colab)

#### Step 1: Upload Training Data

```bash
# Upload your JSONL file to Google Drive
# Example path: /content/drive/training/alex/alex_finetuning.jsonl
```

#### Step 2: Open Colab Notebook

1. Navigate to `data/finetuning/`
2. Open desired agent notebook (e.g., `alex_peer_support_v1.ipynb`)
3. Upload to Google Colab: **File → Upload notebook**
4. Select **GPU Runtime**: Runtime → Change runtime type → T4 GPU

#### Step 3: Configure Parameters

```python
# In the notebook configuration cell:
DATASET_PATH = "/content/drive/training/alex/alex_finetuning.jsonl"
MODEL_NAME = "bigscience/bloom-560m"  # Base model
OUTPUT_DIR = "./tunedModels"
TUNNING_MODEL_NAME = "alex-peer-support-v1"

MAX_LENGTH = 512    # Maximum sequence length
BATCH_SIZE = 4      # Batch size
EPOCHS = 3          # Training epochs
```

> **Note**: For production, use larger models like **Gemini 2.5 Flash** via Vertex AI (requires GCP account with billing).

#### Step 4: Run Fine-Tuning

Execute all cells in sequence:

1. **Install Dependencies**:
   ```bash
   !pip install transformers accelerate datasets peft bitsandbytes safetensors
   ```

2. **Mount Google Drive**:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

3. **Load Dataset**:
   ```python
   dataset = load_dataset("json", data_files=DATASET_PATH)
   ```

4. **Setup Model with LoRA**:
   ```python
   # 8-bit quantization for memory efficiency
   bnb_config = BitsAndBytesConfig(load_in_8bit=True)
   
   model = AutoModelForCausalLM.from_pretrained(
       MODEL_NAME,
       device_map="auto",
       quantization_config=bnb_config
   )
   
   # Apply LoRA configuration
   lora_config = LoraConfig(
       r=8,                           # LoRA rank
       lora_alpha=32,                 # Scaling parameter
       target_modules=["query_key_value"],  # BLOOM-specific
       lora_dropout=0.1,
       task_type="CAUSAL_LM"
   )
   
   model = get_peft_model(model, lora_config)
   model.print_trainable_parameters()
   # Output: trainable params: 2,359,296 || all params: 559,214,592 || trainable%: 0.42%
   ```

5. **Train Model**:
   ```python
   trainer = Trainer(
       model=model,
       args=training_args,
       train_dataset=tokenized_dataset,
       tokenizer=tokenizer
   )
   
   trainer.train()
   ```

6. **Save & Download**:
   ```python
   # Save LoRA adapter weights
   model.save_pretrained(TUNNING_MODEL_NAME)
   tokenizer.save_pretrained(TUNNING_MODEL_NAME)
   
   # Zip for download
   !zip -r alex-peer-support-v1.zip alex-peer-support-v1
   ```

#### Step 5: Deploy Fine-Tuned Model

1. **Download** the `.zip` file from Colab
2. **Extract** to `backend/models/tunedModels/`
3. **Update** `.env`:
   ```env
   USE_FINETUNED_MODELS=true
   FINETUNED_ALEX_MODEL=tunedModels/alex-peer-support-v1
   ```
4. **Restart** the backend server

---

### Benefits of Fine-Tuning

| Aspect | Base Model (Gemini) | Fine-Tuned Model |
|--------|---------------------|------------------|
| **Autism Knowledge** | General | Specialized, neurodiversity-affirming |
| **Agent Personality** | Generic | Consistent with defined persona |
| **Response Style** | Varies | Matches agent's voice (casual, clinical, etc.) |
| **Domain Expertise** | Broad | Deep (e.g., peer support, OT strategies) |
| **Cost** | API calls | Initial training + smaller API calls |

**Example Comparison**:

**Query**: "I'm having a meltdown at work"

- **Base Gemini**: "Take deep breaths and try to calm down. Find a quiet space..."
- **Fine-Tuned Alex**: "That's so tough. When that happened to me, I had to literally escape to the bathroom for 10 minutes. Do you have a quiet space you can get to? Even a storage closet works if needed..."

---

## 🛠️ Technologies & Frameworks

### Core Technologies

| Category | Technology | Purpose |
|----------|-----------|---------|
| **LLM Provider** | Google Gemini API | Primary language model (gemini-2.5-flash) |
| **Backend Framework** | FastAPI | REST API & WebSocket server |
| **Frontend** | HTML/CSS/JavaScript | Real-time chat interface |
| **Vector Database** | ChromaDB | Semantic search for long-term memory |
| **SQL Database** | PostgreSQL | User profiles & structured data |
| **Agent Protocol** | MCP (Model Context Protocol) | Crisis management tooling |
| **Search API** | Tavily | Live crisis resource discovery |
| **Observability** | Langfuse + OpenInference | Tracing, logging, metrics |
| **Logging** | Loguru | Structured application logs |

### Python Dependencies

The project uses a comprehensive set of Python packages organized by function:

```python
# Core Framework & Utilities
python-dotenv==1.2.1          # Environment variable management
pydantic==2.12.4              # Data validation
typing_extensions==4.15.0     # Extended type hints
annotated-types==0.7.0        # Type annotations
loguru==0.7.3                 # Structured logging
httpx==0.28.1                 # HTTP client

# API & Web Services
fastapi==0.121.2              # Modern web framework
uvicorn==0.38.0               # ASGI server
starlette==0.49.3             # ASGI toolkit
websockets==15.0.1            # WebSocket support
python-multipart==0.0.20      # Form data handling
httptools==0.7.1              # ASGI server optimization

# Database & ORM
SQLAlchemy==2.0.44            # Primary ORM
alembic==1.17.2               # Database migrations
psycopg2-binary==2.9.11       # PostgreSQL connector
redis==7.0.1                  # Redis client

# AI/LLMs & Fine-Tuning (HuggingFace)
torch==2.9.1                  # PyTorch deep learning
transformers==4.57.1          # Model loading & tokenization
accelerate==1.12.0            # Distributed training
peft==0.18.0                  # LoRA fine-tuning
bitsandbytes==0.48.2          # 8-bit quantization
safetensors==0.6.2            # Model serialization
tokenizers==0.22.1            # Fast tokenization

# AI/LLMs (Google Generative AI)
google-generativeai==0.8.5           # Gemini API
google-cloud-aiplatform==1.128.0     # Vertex AI

# Vector Store & Embeddings
chromadb==1.3.5                      # Vector database
sentence-transformers==5.1.2         # Local embeddings

# MLOps, Tracing, & Experiment Tracking
mlflow==3.6.0                 # Experiment tracking
langsmith==0.4.43             # LangChain tracing
langfuse==3.10.1              # LLM observability
opentelemetry-sdk==1.38.0     # OpenTelemetry tracing

# Data Processing & Analysis
pandas==2.3.3                 # Data manipulation
numpy==2.3.5                  # Numerical computing
scipy==1.16.3                 # Scientific computing
scikit-learn==1.7.2           # Machine learning
matplotlib==3.10.7            # Plotting

# Testing
pytest==9.0.1                 # Testing framework
pytest-asyncio==1.3.0         # Async testing

# Security & Authentication
cryptography==46.0.3          # Cryptographic functions
python-jose==3.5.0            # JSON Web Tokens
Authlib==1.6.5                # OAuth/OpenID
```

**Key Additions from Base**:
- ✨ **LoRA Fine-Tuning Stack**: torch, transformers, peft, bitsandbytes for local model training
- ✨ **Vertex AI Support**: google-cloud-aiplatform for production Gemini fine-tuning
- ✨ **Enhanced Observability**: langfuse, opentelemetry-sdk for comprehensive tracing
- ✨ **Data Science Tools**: scipy, scikit-learn, matplotlib for model analysis
- ✨ **Database Migrations**: alembic for schema versioning


---

## 🚀 Advanced AI Capabilities

SpectrumCircle demonstrates cutting-edge multi-agent AI patterns:

### 1️⃣ Multi-Agent System Architecture

#### Agent Powered by LLM
✅ **Implementation**: All 6 agents use Google Gemini API
- Each agent has a unique system prompt defining personality and expertise
- Agents can optionally use fine-tuned models for specialized responses
- Base agent class (`BaseAgent`) provides shared LLM interaction logic

#### Parallel Agents
✅ **Implementation**: Multi-perspective responses
```python
# Orchestrator can request secondary opinions
if self._needs_multiple_perspectives(query):
    secondary_responses = await self._get_additional_perspectives(
        query, context, exclude=[primary_agent], max_additional=1
    )
```
- **Use Case**: Complex decisions get both peer + professional input
- **Example**: Alex (peer) + Maya (therapist) for work anxiety

#### Sequential Agents
✅ **Implementation**: Crisis routing → Agent routing
```python
# Sequential flow ensures safety first
crisis_result = await self.crisis_client.is_crisis(message)
if crisis_result:
    return await self.crisis_client.handle_crisis(message)
# Then route to appropriate support agent
primary_agent = await self._llm_route(message, context, suitable_agents)
```

#### Loop Agents
✅ **Implementation**: Conversation memory enables multi-turn context
- Short-term memory tracks recent exchanges (last 5-10 messages)
- Long-term memory retrieves semantically relevant past conversations
- Agents maintain context across conversation turns

---

### 2️⃣ Tools Integration

#### MCP (Model Context Protocol)
✅ **Implementation**: Crisis Management MCP Server

**File**: `mcp/crisis_mcp_server.py`

**Capabilities**:
- **Tool**: `assess_crisis(message, context)` - Analyzes text for safety risks
- **Tool**: `get_resources(crisis_level, type)` - Retrieves emergency contacts
- **Tool**: `log_crisis_event(assessment, user_id)` - Audit trail for safety events

**Crisis Detection Pipeline**:
```python
1. Keyword Pattern Matching
   ↓
2. Indicator Flagging (suicidal_ideation, self_harm_intent, immediate_danger)
   ↓
3. Severity Assessment (LOW → MEDIUM → HIGH → CRITICAL)
   ↓
4. Resource Retrieval (static DB + live Tavily search)
   ↓
5. Safe Response Generation (pre-validated templates)
```

**MCP Server Architecture**:
- **Protocol**: FastMCP over HTTP
- **Port**: 8765 (configurable)
- **Tools Exposed**: 3 functions available to agent orchestrator
- **Safety Database**: Static crisis resources + live search fallback

#### Custom Tools
✅ **Implementation**: Crisis resource search with LLM parsing

```python
def search_live(self, query: str) -> List[Dict[str, str]]:
    # 1. Search web via Tavily
    search_result = self.tavily.search(query=query, max_results=5)
    
    # 2. Parse with Gemini into structured JSON
    prompt = f"Extract emergency resource info: {context}"
    response = self.model.generate_content(
        prompt, 
        generation_config={"response_mime_type": "application/json"}
    )
    
    return json.loads(response.text)
```

**Custom Tool Features**:
- Combines web search (Tavily) + LLM parsing (Gemini)
- Ensures structured output with JSON schema
- Fallback to static database if APIs unavailable

#### Built-in Tools
✅ **Google Search**: Via Tavily API for live crisis resource discovery

---

### 3️⃣ Long-Running Operations

#### Pause/Resume Agents
✅ **Implementation**: WebSocket-based session management

**File**: `backend/api/main.py`

```python
# Active connections stored in-memory
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket
    
    # Long-running conversation loop
    while True:
        data = await websocket.receive_json()
        # Process message asynchronously
        response = await orchestrator.route_query(message, context)
        await websocket.send_json(response)
```

**Features**:
- **Persistent Connections**: Users maintain WebSocket connection during session
- **Typing Indicators**: Real-time status updates while agents "think"
- **Multi-turn Context**: Conversation state maintained across messages
- **Resume Capability**: User profile + memory allows seamless session reconstruction

---

### 4️⃣ Sessions & Memory

#### Session & State Management
✅ **Implementation**: In-Memory Session Service

**Technologies**:
- **WebSocket Connections**: `active_connections` dictionary maps user_id → WebSocket
- **User Profiles**: PostgreSQL stores persistent user data
- **Conversation State**: Tracked in `ConversationMemory` class

**Session Lifecycle**:
```python
1. User connects via WebSocket → Session created
2. Profile loaded from PostgreSQL → State initialized
3. Messages exchanged → Memory updated incrementally
4. User disconnects → Session cleaned up, memory persisted
```

#### Long-Term Memory (Memory Bank)
✅ **Implementation**: Dual-Memory Architecture

**File**: `backend/memory/conversation_memory.py`

**System Design**:

| Memory Type | Storage | Purpose | Retrieval |
|-------------|---------|---------|-----------|
| **Short-Term Memory (STM)** | In-memory deque | Last 5-10 messages | FIFO access |
| **Long-Term Memory (LTM)** | ChromaDB vectors | All past conversations | Semantic search |

**Implementation Details**:

```python
class ConversationMemory:
    def __init__(self):
        # Short-term: Fast recent access
        self.short_term: Dict[str, deque] = {}
        
        # Long-term: Semantic search
        self.collection = chromadb.get_or_create_collection("conversations")
    
    def add_message(self, user_id, role, content, metadata):
        # Add to both STM and LTM
        self.short_term[user_id].append(message)
        self.collection.add(
            documents=[content],
            metadatas=[{
                'user_id': user_id,
                'emotional_state': metadata['emotional_state'],
                'topics': json.dumps(metadata['topics'])
            }]
        )
    
    def get_context_for_query(self, user_id, current_query):
        # Combine STM + LTM
        return {
            'recent_history': self.get_recent_history(user_id, n=5),
            'relevant_past': self.search_conversations(user_id, query, n=3)
        }
```

**Benefits**:
- **Fast Access**: Recent messages from in-memory deque (O(1))
- **Semantic Retrieval**: Find relevant past conversations using vector similarity
- **Context Compaction**: Only relevant history included in prompts (token optimization)

#### Context Engineering (Context Compaction)
✅ **Implementation**: Intelligent context assembly

**Strategy**:
```python
def _build_prompt(self, user_message, context):
    # 1. System prompt (agent personality)
    system_prompt = self.get_system_prompt()
    
    # 2. User profile (compact, structured)
    profile_context = self._format_user_profile(context['user_profile'])
    
    # 3. Limited history (last 5 messages only)
    recent_history = context['conversation_history'][-5:]
    history_context = self._format_conversation_history(recent_history)
    
    # 4. Relevant past (semantic search, top 3)
    relevant_past = memory.search_conversations(user_id, user_message, n=3)
    
    return f"{system_prompt}\n{profile_context}\n{history_context}\n{user_message}"
```

**Token Optimization Techniques**:
- ✅ Window-based history (last 5 messages, not entire conversation)
- ✅ Semantic search for relevant past context (top 3 matches)
- ✅ Structured user profile formatting (key-value pairs)
- ✅ Metadata stored separately from prompt content

---

### 5️⃣ Observability: Logging, Tracing, Metrics

SpectrumCircle implements **comprehensive observability** across all layers.

#### Logging
✅ **Implementation**: Loguru structured logging

**Configuration**:
```python
from loguru import logger

# File logging with rotation
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG"
)

# Structured log messages
logger.info(f"Agent: {self.name} | User: {message[:50]}... | Response length: {len(response)}")
```

**Log Files**:
- `logs/app.log` - Main application logs (API, orchestrator, agents)
- `logs/crisis_mcp.log` - Crisis detection events (safety-critical audit trail)

**Log Levels**:
- `DEBUG`: Prompt construction, memory operations
- `INFO`: Agent routing decisions, successful responses
- `WARNING`: Fallback routing, missing configurations
- `ERROR`: API failures, LLM errors

#### Tracing
✅ **Implementation**: Langfuse + OpenInference instrumentation

**File**: `backend/agents/orchestrator/router.py`

```python
from langfuse import observe, propagate_attributes, get_client
from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor

# Initialize instrumentation
GoogleGenAIInstrumentor().instrument()

langfuse = get_client()
assert langfuse.auth_check()

class AgentOrchestrator:
    @observe  # Automatic tracing decorator
    async def route_query(self, user_message, context):
        # All operations nested under this trace
        crisis_result = await self.crisis_client.is_crisis(message)
        primary_agent = await self._llm_route(message, context, agents)
        response = await agent.generate_response(message, context)
        return response
```

**Traced Operations**:
- ✅ Agent routing decisions (which agent was selected, why)
- ✅ LLM API calls (prompt, response, tokens used)
- ✅ Crisis detection checks (keywords matched, severity level)
- ✅ Memory operations (STM hits, LTM searches)

**Langfuse Dashboard**: `http://localhost:3000`
- View complete conversation traces
- Analyze agent performance
- Monitor LLM costs and latency
- Debug routing decisions

<div align="center">
<img src="./images/langfuse.png" alt="Langfuse" width="900">
</div>

#### Metrics
✅ **Implementation**: Conversation analytics

**Available Metrics**:
```python
GET /stats/{user_id}
{
    "total_conversations": 45,
    "most_used_agent": "alex",
    "most_common_emotion": "anxious",
    "special_interests_count": 3,
    "strategies_learned": 12,
    "triggers_identified": 5
}
```

**Metric Sources**:
- ChromaDB metadata aggregation (conversation patterns)
- PostgreSQL user profile analytics (learning progress)
- Langfuse trace analytics (agent performance)

---

## 📦 Installation & Setup

### Prerequisites

- **Python**: 3.11+
- **PostgreSQL**: 14+
- **Node.js**: 16+ (for frontend dependencies, if any)
- **Google Cloud Account**: For Gemini API key
- **Tavily Account**: For crisis resource search (optional)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/spectrum-circle.git
cd spectrum-circle
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Set Up PostgreSQL Database

**Option 1: Using Docker Compose (Recommended)**

Use the provided Docker Compose configuration to quickly set up PostgreSQL with Adminer:

```bash
cd docker/postgres
docker-compose up -d
```

This will start:
- **PostgreSQL** on port `5432` (password: `example`)
- **Adminer** (database management UI) on `http://localhost:8080`

**Option 2: Manual Installation**

If you prefer to install PostgreSQL manually:

```bash
# Create database
createdb spectrum_circle

# Or use psql
psql -U postgres
CREATE DATABASE spectrum_circle;
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Google AI (REQUIRED)
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# External API Keys (OPTIONAL)
TAVILY_API_KEY=your_tavily_key_here
LIVE_SEARCH=false

# Database (REQUIRED)
POSTGRES_URL=postgresql://postgres:password@localhost:5432/spectrum_circle

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
ENABLE_ANALYTICS=true

# Fine-Tuned Models (OPTIONAL)
USE_FINETUNED_MODELS=false
FINETUNED_BASE_MODEL=models/autism-knowledge-base-v1
FINETUNED_ALEX_MODEL=tunedModels/alex-peer-support-v1
FINETUNED_MAYA_MODEL=tunedModels/maya-therapist-v1
# ... (other fine-tuned models)

# MCP
MCP_PORT=8765
MCP_SERVER_URL=http://127.0.0.1:8765/mcp

# API
API_PORT=8000

# Monitoring (OPTIONAL - requires Langfuse setup)
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_BASE_URL=http://localhost:3000
```

### 6. Set Up Langfuse (Optional - for Observability)

Using Docker:

```bash
cd docker/langfuse
docker-compose up -d
```

Access Langfuse dashboard: `http://localhost:3000`

---

## 🚀 Running the Application

### Start the MCP Crisis Server

```bash
python mcp/crisis_mcp_server.py --debug
```

Expected output:
```
=======================================================
CRISIS MANAGEMENT MCP SERVER — RUNNING (HTTP)
Logs → logs/crisis_mcp.log
Press CTRL+C to stop
=======================================================
```

### Start the FastAPI Backend

```bash
python backend/api/main.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Open the Frontend

Open `frontend/index.html` in your browser, or serve it with a local server:

```bash
# Option 1: Using Python
python -m http.server 8080 --directory frontend

# Option 2: Using npm
npx serve frontend
```

Navigate to `http://localhost:8080`

---

### Showcase: 
[![A video showing how to use SpectrumCircle](https://img.youtube.com/vi/zsuSKUTDSfE/hqdefault.jpg)](https://www.youtube.com/watch?v=zsuSKUTDSfE)

## 🧪 Testing

### Unit Tests (Individual Agents)

```bash
# Test all agents
python tests/test_agents.py

# Test specific agent
python backend/agents/personalities/alex.py
python backend/agents/personalities/maya.py
```

Expected output:
```
==============================================
TESTING COMPLETE ORCHESTRATOR - ALL 6 AGENTS
==============================================

--- TEST CASE 1 ---
Message: I'm nervous about starting my new job
Context: Age=23, Role=individual
Expected: alex

✓ Routed to: alex

Response preview:
I totally get it! We've all been there. Starting a new job can feel...
```

### Integration Tests (Orchestrator)

```bash
python backend/agents/orchestrator/router.py
```

### API Tests

```bash
# Test API endpoints
python tests/test_api.py

# Or use pytest
pytest tests/test_api.py -v
```

### Memory System Tests

```bash
python backend/memory/conversation_memory.py
```

Expected output:
```
--- 1. Short-Term History (STM) ---
Retrieved 3 messages from recent history:
  [USER] I'm nervous about my new job starting...
  [AGENT] I totally get it! We can create a visual...
  [USER] The social part worries me most, like...

--- 2. Long-Term Search (LTM) ---
Search results for semantic query: **'how to handle unexpected changes at work'**
  → [USER] (Agent: none) Relevance: 0.2341
    Content: I'm nervous about my new job starting next week...
```

---

## 📂 Project Structure

```
spectrum-circle/
├── backend/
│   ├── agents/
│   │   ├── base_agent.py              # Abstract base class for all agents
│   │   ├── orchestrator/
│   │   │   └── router.py              # Multi-agent routing logic
│   │   └── personalities/
│   │       ├── alex.py                # Young adult peer agent
│   │       ├── maya.py                # Therapist agent
│   │       ├── jordan.py              # Teen peer agent
│   │       ├── dr_chen.py             # Activities specialist agent
│   │       ├── sam.py                 # Parent peer agent
│   │       └── river.py               # Sibling peer agent
│   ├── api/
│   │   └── main.py                    # FastAPI server (REST + WebSocket)
│   ├── memory/
│   │   ├── conversation_memory.py     # Dual-memory system (STM + LTM)
│   │   └── user_profiles/
│   │       └── profile_manager.py     # User profile CRUD
│   ├── models/
│   │   └── local_model_loader.py      # Fine-tuned model loading
│   ├── utils/
│   │   ├── config.py                  # Environment configuration
│   │   └── client.py                  # MCP client utilities
│   └── requirements.txt
├── data/
│   ├── data_collection/               # Conversation datasets
│   ├── finetuning/                    # Model fine-tuning scripts
│   └── training/                      # Training data generation
├── docker/
│   ├── langfuse/                      # Langfuse observability stack
│   └── postgres/                      # PostgreSQL setup
├── frontend/
│   ├── avatars/
│   │   ├── alex.svg                   # Agent avatar images
│   │   ├── maya.svg
│   │   ├── jordan.svg
│   │   ├── dr_chen.svg
│   │   ├── sam.svg
│   │   └── river.svg
│   ├── index.html                     # Main chat interface
│   ├── lib/
│   │   └── script.js                  # Frontend JavaScript
│   └── styles/
│       └── styles.css                 # UI styling
├── mcp/
│   └── crisis_mcp_server.py           # Crisis management MCP server
├── tests/
│   ├── test_agents.py                 # Agent unit tests
│   ├── test_api.py                    # API integration tests
├── logs/
│   ├── app.log                        # Application logs
│   └── crisis_mcp.log                 # Crisis detection logs
├── .env                               # Environment variables
└── README.md                          # This file
```

---

## 📡 API Documentation

### REST Endpoints

#### Health Check
```
GET /
Response: {"status": "healthy", "service": "SpectrumCircle API", "version": "1.0.0"}
```

#### Create User Profile
```
POST /profiles
Body: {
  "user_id": "user123",
  "age": 25,
  "diagnosis": "Autism Spectrum",
  "communication_preference": "direct",
  "sensory_profile": {...},
  "special_interests": [...]
}
Response: {"success": true, "user_id": "user123"}
```

#### Get User Profile
```
GET /profiles/{user_id}
Response: {"success": true, "profile": {...}}
```

#### Get User Statistics
```
GET /stats/{user_id}
Response: {
  "success": true,
  "stats": {
    "total_conversations": 45,
    "most_used_agent": "alex",
    "most_common_emotion": "anxious",
    "special_interests_count": 3,
    "strategies_learned": 12,
    "triggers_identified": 5
  }
}
```

### WebSocket Endpoint

#### Real-Time Chat
```
WebSocket: ws://localhost:8000/ws/chat/{user_id}

Send Message:
{
  "message": "I'm feeling anxious about work",
  "emotional_state": "anxious",
  "age": 25,
  "role": "individual"
}

Receive Response:
{
  "type": "message",
  "agent": "alex",
  "message": "I totally get it...",
  "suggestions": ["Strategy 1", "Strategy 2"],
  "metadata": {
    "topics": ["work", "anxiety"],
    "emotional_tone": "supportive"
  },
  "is_crisis": false
}
```

---

## 🎯 How the Solution Addresses AI Topics

### ✅ Multi-Agent System
- **6 specialized agents** with distinct personalities and expertise
- **LLM-powered orchestrator** using Gemini for intelligent routing
- **Parallel agent execution** for multi-perspective responses
- **Sequential crisis → agent routing** for safety-first operation

### ✅ Tools
- **MCP**: Crisis management server with 3 custom tools
- **Custom Tools**: Tavily + Gemini resource parser
- **Built-in Tools**: Google Search via Tavily API

### ✅ Long-Running Operations
- **WebSocket sessions** maintain persistent connections
- **Pause/Resume**: User profiles + memory enable session reconstruction
- **Typing indicators** for real-time feedback

### ✅ Sessions & Memory
- **Session Management**: In-memory WebSocket connection tracking
- **Long-Term Memory**: ChromaDB vector store for semantic search
- **Short-Term Memory**: In-memory deque for recent context
- **Context Engineering**: Windowed history + semantic retrieval for token optimization

### ✅ Observability
- **Logging**: Loguru with structured logs (app.log, crisis_mcp.log)
- **Tracing**: Langfuse integration with `@observe` decorators
- **Metrics**: Conversation analytics, agent performance tracking
- **Instrumentation**: OpenInference for Google GenAI calls

---

## 🤝 Contributing

This project is designed for autism support. Contributions should prioritize:
- Neurodiversity-affirming language
- Safety and crisis prevention
- User privacy and data protection
- Accessible design

---

## 📄 License

This project is for educational and research purposes.

---

## 🙏 Acknowledgments

- **Autistic community** for lived experience insights
- **Google Gemini** for powerful LLM capabilities
- **Langfuse** for observability infrastructure
- **ChromaDB** for efficient vector storage

---

**Built with 💙 for the autism and neurodiversity community**
