# Agent Stacking Architecture with Marimo Notebooks

## Overview

This document describes an **Infrastructure-as-Code** approach to layering marimo notebooks as **AI agent strata**, where each layer provides services to higher layers through reactive cell interfaces.

## Core Concepts

### 1. Agent as Substrate

Each marimo notebook acts as a **computational substrate** that:
- Exposes reactive cells as API surfaces
- Consumes inputs from lower layers
- Provides outputs to higher layers
- Maintains internal state through marimo's reactivity

### 2. Layered Architecture

```
┌────────────────────────────────────────────────────┐
│ Layer 3: Orchestration                            │
│ ┌────────────────────┐                            │
│ │ Concierge Agent    │ Multi-workspace coordination│
│ └────────────────────┘                            │
└────────────────────────────────────────────────────┘
           ▲
           │ insights, recommendations, patterns
           │
┌────────────────────────────────────────────────────┐
│ Layer 2: Analysis                                 │
│ ┌──────────────────┐  ┌──────────────────┐       │
│ │ Debriefing Agent │  │ Pattern Detector │       │
│ └──────────────────┘  └──────────────────┘       │
└────────────────────────────────────────────────────┘
           ▲
           │ validated contexts, session logs
           │
┌────────────────────────────────────────────────────┐
│ Layer 1: Context Management                       │
│ ┌────────────────┐  ┌────────────────┐           │
│ │ Context Loader │  │ Validator      │           │
│ └────────────────┘  └────────────────┘           │
└────────────────────────────────────────────────────┘
           ▲
           │ workspace context, session logs
           │
┌────────────────────────────────────────────────────┐
│ Layer 0: Base Infrastructure                      │
│ ┌────────────────────────────────┐                │
│ │ KB Conduit (Shell + YAML)      │                │
│ └────────────────────────────────┘                │
└────────────────────────────────────────────────────┘
```

### 3. Call Surface Stacking

**Traditional API Stack:**
```
HTTP REST → Service Layer → Database
```

**Marimo Agent Stack:**
```
Reactive Cell → Reactive Cell → Reactive Cell → Data Source
    (Layer 3)      (Layer 2)       (Layer 1)      (Layer 0)
```

**Key Difference:** Changes propagate **automatically** through marimo's reactivity graph, creating a **living computational stack**.

## Infrastructure-as-Code Schema

### Design Principles

1. **Declarative Configuration**: Define *what* the stack should be, not *how* to build it
2. **Layer Isolation**: Each layer only knows about layers below it
3. **Data Flow Contracts**: Explicit interfaces between layers
4. **Runtime Agnostic**: Can deploy to local, Docker, K8s, etc.

### Schema Components

#### Agent Definition

```yaml
agent:
  name: "debriefing_agent"           # Unique identifier
  type: "marimo_notebook"             # Execution model
  layer: 2                            # Position in stack

  implementation:
    path: "agents/debriefer.py"       # Where the code lives

  dependencies:                       # What this agent needs
    - agent_name: "kb_base"
      inputs:
        session_log: "history"        # Dependency output → my input

  interface:                          # Contract with other agents
    inputs:
      - name: "history"
        type: "session_log"
        source: "agent:kb_base.session_log"

    outputs:
      - name: "insights"
        type: "insights"
        exposed_as: "reactive_cell:insights"
```

#### Stack Definition

```yaml
stack:
  name: "kb-conduit-full-stack"

  agents:
    - [agent definitions...]          # List of all agents

  data_flow:                          # Explicit data flow graph
    - from: "kb_base"
      to: "debriefing_agent"
      data: "session_log"
      transform: "parse_yaml_log"

  policies:
    auto_restart: true                # Operational policies
    cascade_stop: true
    parallel_init: true
```

## How Marimo Enables This

### 1. Reactive Cells as API Surfaces

```python
# agents/context_loader.py (Layer 1)
import marimo as mo

# This cell is an "API endpoint" for higher layers
@mo.cell
def load_context():
    context = load_yaml_context()
    return context  # Exposed as "agent:context_loader.context"

# Higher layer can depend on this cell
# Any change to the YAML triggers re-execution
```

### 2. Dependency Graph = Agent Graph

```python
# agents/debriefer.py (Layer 2)
import marimo as mo

# Depends on Layer 1's context
@mo.cell
def analyze(context):  # context comes from Layer 1
    insights = extract_insights(context)
    return insights  # Exposed to Layer 3

# Marimo automatically:
# 1. Detects the dependency on 'context'
# 2. Re-runs this cell when context changes
# 3. Propagates changes to Layer 3
```

### 3. Multi-Notebook Orchestration

While a single marimo notebook creates an internal DAG of cells, **multiple notebooks** can be orchestrated as a **meta-DAG** where:

- Each notebook = node in meta-DAG
- Data flows between notebooks via:
  - Shared file system (YAML, JSON)
  - Environment variables
  - HTTP APIs (marimo's server mode)
  - Message queues (for async patterns)

## Deployment Models

### Local Development

```yaml
deployment:
  target: "local"
  local:
    workspace_path: "/home/user/kb-conduit"
```

**Execution:**
```bash
# Layer 1 agents (run mode, background)
marimo run agents/context_loader.py --port 2718 &
marimo run agents/validator.py --port 2719 &

# Layer 2 agents
marimo run agents/debriefer.py --port 2720 &
marimo run agents/pattern_detector.py --port 2721 &

# Layer 3 agent (edit mode, foreground - human oversight)
marimo edit agents/concierge.py --port 2722
```

### Docker Compose

```yaml
deployment:
  target: "docker"
  docker:
    compose_file: "docker-compose.generated.yaml"
```

**Generated docker-compose.yaml:**
```yaml
services:
  context_loader:
    image: marimo-agent:latest
    command: marimo run /app/agents/context_loader.py --port 2718
    volumes:
      - ~/.kb-conduit:/kb-conduit:ro
    ports:
      - "2718:2718"
    depends_on:
      - kb_base

  debriefing_agent:
    image: marimo-agent:latest
    command: marimo run /app/agents/debriefer.py --port 2720
    depends_on:
      - context_loader
    ports:
      - "2720:2720"

  # ... other agents
```

### Kubernetes

```yaml
deployment:
  target: "kubernetes"
  kubernetes:
    namespace: "kb-conduit-agents"
```

**Generated manifests:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: debriefing-agent
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: marimo
        image: marimo-agent:latest
        command: ["marimo", "run", "/app/agents/debriefer.py"]
        env:
        - name: KB_CONDUIT_ROOT
          value: "/kb-conduit"
        resources:
          requests:
            memory: "1Gi"
            cpu: "1.5"
```

## Data Flow Patterns

### 1. Reactive Pull (Marimo Native)

```python
# Higher layer cell automatically pulls from lower layer
@mo.cell
def analyze(context):  # 'context' is a marimo reference
    # Automatically re-runs when context changes
    return extract_insights(context)
```

### 2. File-Based Push

```python
# Lower layer writes file
@mo.cell
def save_context():
    with open('/tmp/context.json', 'w') as f:
        json.dump(context, f)

# Higher layer watches file
@mo.cell
def watch_context():
    # Use file watcher or polling
    return json.load(open('/tmp/context.json'))
```

### 3. HTTP API

```python
# Lower layer exposes HTTP endpoint (marimo server mode)
@mo.cell
def api_endpoint():
    return context  # Accessible at http://localhost:2718/

# Higher layer fetches via HTTP
@mo.cell
def fetch_context():
    import requests
    return requests.get('http://context_loader:2718/context').json()
```

### 4. Message Queue (Async)

```python
# Lower layer publishes
@mo.cell
def publish_insights():
    redis.publish('insights_channel', json.dumps(insights))

# Higher layer subscribes
@mo.cell
def subscribe_insights():
    message = redis.subscribe('insights_channel')
    return json.loads(message)
```

## Why This Is Powerful

### 1. **Inspectability**

Every layer is a marimo notebook = **visual debugging** of the entire stack.

```
Layer 3 UI: Shows orchestration decisions
   ↓
Layer 2 UI: Shows session analysis and patterns
   ↓
Layer 1 UI: Shows context validation and editing
   ↓
Layer 0: YAML files (human-readable)
```

### 2. **Gradual Complexity**

Start with one agent, add layers as needed:

```
Week 1: Just Layer 0 (kb-conduit shell script)
Week 2: Add Layer 1 (context loader marimo notebook)
Week 3: Add Layer 2 (debriefing agent)
Week 4: Add Layer 3 (concierge orchestration)
```

### 3. **Development Velocity**

Edit any layer's marimo notebook **live** while the stack runs:

```bash
# Edit Layer 2 agent while Layers 0, 1, 3 keep running
marimo edit agents/debriefer.py

# Changes propagate automatically through reactive graph
# No restart needed!
```

### 4. **Type Safety** (with typing)

```python
from typing import TypedDict

class ContextSnapshot(TypedDict):
    workspace: str
    contexts: list[str]
    timestamp: datetime

@mo.cell
def load_context() -> ContextSnapshot:
    return {...}

@mo.cell
def analyze(context: ContextSnapshot):  # Type-checked!
    ...
```

### 5. **Testing in Layers**

```python
# Test Layer 1 in isolation
def test_context_loader():
    mock_yaml = {...}
    result = context_loader.load_context(mock_yaml)
    assert result.workspace == "Test"

# Test Layer 2 with mocked Layer 1
def test_debriefing_agent():
    mock_context = ContextSnapshot(...)
    insights = debriefer.analyze(mock_context)
    assert len(insights) > 0
```

## Comparison to Traditional IaC

### Terraform / Ansible

**What they manage:** Infrastructure (VMs, networks, databases)

**What marimo agent stacking manages:** Computational workflows and AI agents

**Similarity:** Declarative YAML describing desired state

**Difference:** Marimo adds **reactivity** - state changes propagate automatically

### Kubernetes

**What it orchestrates:** Containerized services

**What marimo agent stacking orchestrates:** Marimo notebooks as services

**Similarity:** Layered architecture, health checks, restarts

**Difference:** Marimo notebooks are **introspectable** and **editable** while running

### Docker Compose

**What it composes:** Container services

**What marimo agent stacking composes:** Reactive computational graphs

**Similarity:** Dependency management, networking, resource limits

**Difference:** Marimo enables **live editing** of service logic

## Is This the Right Fit for KB Conduit?

### Pros

1. **Natural Extension**: KB Conduit is already designed for agent handoff
2. **Visual Debugging**: Each layer visible in marimo UI
3. **Incremental Adoption**: Can add one layer at a time
4. **Reactive Architecture**: Changes propagate automatically
5. **Developer Experience**: Edit agents live while running

### Cons

1. **Complexity**: Current KB Conduit is intentionally minimal (shell + YAML)
2. **Dependencies**: Requires Python, marimo, potentially other libraries
3. **Resource Overhead**: Each marimo notebook needs its own process/port
4. **Operational Burden**: More moving parts = more things to monitor
5. **Over-Engineering**: Might be solving problems users don't have yet

### Recommendation

**Use this architecture IF:**
- You want to build **actual AI agents** (not just context loading)
- You need **multi-workspace orchestration**
- You want **visual introspection** of agent behavior
- You're comfortable with **operational complexity**

**Don't use this architecture IF:**
- Current shell script + YAML is sufficient
- You prefer **simple over complex** (KB Conduit's stated philosophy)
- You don't need agent-to-agent communication
- The 10x complexity increase isn't justified by user needs

## Next Steps

If you want to explore this further, we could:

1. **Prototype Layer 1**: Build a single marimo context loader
2. **Define Minimal Schema**: Create a simplified version for just 2 layers
3. **Build Schema Validator**: Tool to validate agent stack YAML files
4. **Generate Deployment Code**: Script to convert YAML → docker-compose or systemd services
5. **Create Example Agents**: Reference implementations of debriefer, concierge

The schema is designed to **reason about** the architecture, even if full implementation isn't warranted.
