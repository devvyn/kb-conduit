"""
Marimo Agent Stacking Example
Demonstrates how reactive cells create call surface stacking

This is a simplified example showing how THREE marimo notebooks
would interact as layered agents. In practice, each would be a
separate .py file.
"""

import marimo

# =============================================================================
# CONCEPTUAL LAYER 1: Context Loader Agent
# File: agents/context_loader.py
# =============================================================================

"""
import marimo as mo
import yaml
import os

app = mo.App()

@app.cell
def load_kb_context():
    '''Base layer: Load context from kb-conduit YAML'''
    context_path = os.path.expanduser('~/.kb-conduit/contexts/example.yaml')

    with open(context_path) as f:
        raw_context = yaml.safe_load(f)

    return raw_context


@app.cell
def validate_context(raw_context):
    '''Validation layer: Ensure schema compliance'''
    required_keys = ['workspace', 'contexts', 'people', 'policies']

    for key in required_keys:
        if key not in raw_context:
            raise ValueError(f"Missing required key: {key}")

    validated = {
        'workspace': raw_context['workspace'],
        'contexts': raw_context.get('contexts', []),
        'people': raw_context.get('people', []),
        'policies': raw_context.get('policies', []),
        'clues': raw_context.get('clues', []),
        'metadata': {
            'validated_at': datetime.now(),
            'valid': True
        }
    }

    return validated


@app.cell
def compute_metrics(validated):
    '''Analytics layer: Compute context metrics'''
    metrics = {
        'num_contexts': len(validated['contexts']),
        'num_people': len(validated['people']),
        'num_policies': len(validated['policies']),
        'num_clues': len(validated['clues']),
        'completeness_score': calculate_completeness(validated)
    }

    return metrics


@app.cell
def expose_context_api(validated, metrics):
    '''
    API Surface: This cell exposes data to higher layers

    In a real deployment, this could be:
    - Written to a file that Layer 2 watches
    - Served via HTTP endpoint (marimo server mode)
    - Published to a message queue
    - Stored in shared memory
    '''
    context_api = {
        'context': validated,
        'metrics': metrics,
        'status': 'ready',
        'last_updated': datetime.now()
    }

    # Higher layers can access this via HTTP:
    # GET http://localhost:2718/context

    return context_api


# UI Elements for human inspection
@app.cell
def display_ui(validated, metrics):
    '''Interactive UI for monitoring Layer 1'''
    import marimo as mo

    mo.md(f'''
    ## Context Loader (Layer 1)

    **Workspace**: {validated['workspace']}

    **Metrics**:
    - Contexts: {metrics['num_contexts']}
    - People: {metrics['num_people']}
    - Policies: {metrics['num_policies']}
    - Completeness: {metrics['completeness_score']:.1%}
    ''')

    return mo


if __name__ == '__main__':
    app.run()
"""

# =============================================================================
# CONCEPTUAL LAYER 2: Debriefing Agent
# File: agents/debriefer.py
# =============================================================================

"""
import marimo as mo
import yaml
import requests
from datetime import datetime, timedelta

app = mo.App()

@app.cell
def fetch_layer1_context():
    '''
    Call Surface Stack: Pull data from Layer 1

    This cell depends on Layer 1's exposed API.
    When Layer 1's context changes, this triggers re-execution.
    '''
    # Option 1: HTTP fetch from Layer 1's marimo server
    response = requests.get('http://localhost:2718/context')
    layer1_data = response.json()

    # Option 2: File-based (simpler, no HTTP)
    # with open('/tmp/context_api.json') as f:
    #     layer1_data = json.load(f)

    return layer1_data


@app.cell
def load_session_logs():
    '''Load kb-conduit session logs'''
    log_path = os.path.expanduser('~/.kb-conduit/logs/session.log')

    sessions = []
    with open(log_path) as f:
        for entry in yaml.safe_load_all(f):
            sessions.append(entry)

    return sessions


@app.cell
def analyze_sessions(sessions, layer1_data):
    '''
    Core analysis: Extract insights from session history

    This cell receives:
    - sessions: from our own load_session_logs cell
    - layer1_data: from Layer 1 via fetch_layer1_context

    This is the "stacking" - combining data from lower layer
    with our own data sources.
    '''
    current_workspace = layer1_data['context']['workspace']

    # Filter sessions for current workspace
    workspace_sessions = [
        s for s in sessions
        if s.get('workspace') == current_workspace
    ]

    # Time-based analysis
    recent_cutoff = datetime.now() - timedelta(days=7)
    recent_sessions = [
        s for s in workspace_sessions
        if datetime.fromisoformat(s['timestamp']) > recent_cutoff
    ]

    # Extract insights
    insights = {
        'total_sessions': len(workspace_sessions),
        'recent_sessions': len(recent_sessions),
        'avg_sessions_per_day': len(recent_sessions) / 7,
        'most_common_pwd': find_most_common(workspace_sessions, 'pwd'),
        'context_drift': detect_context_drift(workspace_sessions, layer1_data),
        'recommended_clues': suggest_new_clues(workspace_sessions),
    }

    return insights


@app.cell
def generate_recommendations(insights, layer1_data):
    '''
    Generate recommendations for context updates

    This is Layer 2's "added value" - intelligence on top of Layer 1
    '''
    recommendations = []

    # Recommend new clues based on session patterns
    current_clues = set(layer1_data['context']['clues'])
    suggested_clues = set(insights['recommended_clues'])
    new_clues = suggested_clues - current_clues

    if new_clues:
        recommendations.append({
            'type': 'add_clues',
            'clues': list(new_clues),
            'rationale': 'Appeared in 3+ recent sessions'
        })

    # Recommend context updates based on drift
    if insights['context_drift'] > 0.3:
        recommendations.append({
            'type': 'review_contexts',
            'rationale': f'High drift detected ({insights["context_drift"]:.1%})'
        })

    return recommendations


@app.cell
def expose_debrief_api(insights, recommendations):
    '''
    API Surface: Expose Layer 2 intelligence to Layer 3

    This is Layer 2's "call surface" for higher layers
    '''
    debrief_api = {
        'insights': insights,
        'recommendations': recommendations,
        'status': 'ready',
        'last_analysis': datetime.now()
    }

    # Higher layers access via:
    # GET http://localhost:2720/insights

    return debrief_api


@app.cell
def display_ui(insights, recommendations):
    '''Interactive UI for monitoring Layer 2'''
    import marimo as mo

    mo.md(f'''
    ## Debriefing Agent (Layer 2)

    **Session Analysis**:
    - Total sessions: {insights['total_sessions']}
    - Recent (7d): {insights['recent_sessions']}
    - Daily average: {insights['avg_sessions_per_day']:.1f}

    **Recommendations**: {len(recommendations)}
    ''')

    # Interactive element: approve recommendations
    approve = mo.ui.checkbox(label="Approve recommendations")

    return mo, approve


if __name__ == '__main__':
    app.run()
"""

# =============================================================================
# CONCEPTUAL LAYER 3: Concierge Agent
# File: agents/concierge.py
# =============================================================================

"""
import marimo as mo
import requests
import os
import glob

app = mo.App()

@app.cell
def discover_workspaces():
    '''Find all available kb-conduit workspaces'''
    context_dir = os.path.expanduser('~/.kb-conduit/contexts')
    context_files = glob.glob(f'{context_dir}/*.yaml')

    workspaces = []
    for path in context_files:
        with open(path) as f:
            ctx = yaml.safe_load(f)
            workspaces.append({
                'name': ctx['workspace'],
                'path': path,
                'file': os.path.basename(path)
            })

    return workspaces


@app.cell
def fetch_layer1_context():
    '''Call Surface Stack: Pull from Layer 1'''
    response = requests.get('http://localhost:2718/context')
    return response.json()


@app.cell
def fetch_layer2_insights():
    '''Call Surface Stack: Pull from Layer 2'''
    response = requests.get('http://localhost:2720/insights')
    return response.json()


@app.cell
def orchestrate(workspaces, layer1_context, layer2_insights):
    '''
    Multi-workspace orchestration

    This cell combines:
    - workspaces: Our own discovery
    - layer1_context: Layer 1's context API
    - layer2_insights: Layer 2's insights API

    This is THREE-LAYER STACKING:
    Layer 3 (this cell) → Layer 2 (insights) → Layer 1 (context) → Layer 0 (YAML)
    '''
    current_workspace = layer1_context['context']['workspace']
    recommendations = layer2_insights['recommendations']

    # Build orchestration plan
    plan = {
        'current_workspace': current_workspace,
        'available_workspaces': len(workspaces),
        'pending_actions': [],
        'cross_workspace_insights': {},
    }

    # Process Layer 2 recommendations
    for rec in recommendations:
        if rec['type'] == 'add_clues':
            plan['pending_actions'].append({
                'workspace': current_workspace,
                'action': 'add_clues',
                'clues': rec['clues'],
                'auto_apply': False,  # Require human approval
                'source': 'debriefing_agent'
            })

    # Cross-workspace analysis (Layer 3's unique value)
    # Check if similar contexts exist in other workspaces
    for ws in workspaces:
        if ws['name'] != current_workspace:
            # Could fetch insights for each workspace
            # and find patterns across workspaces
            pass

    return plan


@app.cell
def execute_actions(plan):
    '''
    Action execution layer

    Actually applies approved recommendations
    '''
    executed = []

    for action in plan['pending_actions']:
        if action.get('approved', False):
            # Execute the action
            if action['action'] == 'add_clues':
                update_context_file(
                    action['workspace'],
                    add_clues=action['clues']
                )
                executed.append(action)

    return executed


@app.cell
def expose_concierge_api(plan, executed):
    '''
    API Surface: Layer 3's orchestration interface

    This is the TOP of the stack - exposed to humans or external systems
    '''
    concierge_api = {
        'orchestration_plan': plan,
        'executed_actions': executed,
        'status': 'ready',
        'last_orchestration': datetime.now()
    }

    return concierge_api


@app.cell
def display_ui(workspaces, plan, executed):
    '''Interactive UI for human oversight'''
    import marimo as mo

    # Multi-workspace selector
    workspace_selector = mo.ui.dropdown(
        options=[w['name'] for w in workspaces],
        label="Select workspace"
    )

    mo.md(f'''
    ## Concierge Agent (Layer 3)

    **Multi-Workspace Orchestration**

    Available workspaces: {len(workspaces)}

    **Pending Actions**: {len(plan['pending_actions'])}
    **Executed Actions**: {len(executed)}
    ''')

    # Action approval interface
    action_list = mo.ui.table(
        data=plan['pending_actions'],
        selection='multi'
    )

    approve_button = mo.ui.button(
        label="Approve Selected Actions",
        on_click=lambda: approve_actions(action_list.value)
    )

    return mo, workspace_selector, action_list, approve_button


if __name__ == '__main__':
    app.run()
"""

# =============================================================================
# HOW THE STACKING WORKS
# =============================================================================

"""
Call Surface Propagation:

1. Layer 0 (kb-conduit YAML) changes
   → Triggers Layer 1 re-execution (file watcher or manual reload)

2. Layer 1 cell `load_kb_context()` re-runs
   → Triggers `validate_context()` (marimo reactive dependency)
   → Triggers `compute_metrics()` (dependency on validated)
   → Triggers `expose_context_api()` (dependency on validated + metrics)
   → HTTP API updates at localhost:2718

3. Layer 2 cell `fetch_layer1_context()` polls/streams from Layer 1
   → Detects change in Layer 1's API
   → Triggers `analyze_sessions()` (dependency on layer1_data)
   → Triggers `generate_recommendations()` (dependency on insights)
   → Triggers `expose_debrief_api()` (dependency on insights + recommendations)
   → HTTP API updates at localhost:2720

4. Layer 3 cell `fetch_layer2_insights()` polls/streams from Layer 2
   → Detects change in Layer 2's API
   → Triggers `orchestrate()` (dependency on layer2_insights)
   → Triggers `execute_actions()` (dependency on plan)
   → Triggers `expose_concierge_api()` (dependency on plan + executed)
   → UI updates automatically (marimo reactivity)

This is AGENT CALL SURFACE STACKING via reactive propagation!

---

Data Flow:

YAML File → Layer 1 → Layer 2 → Layer 3 → Human UI
    ↓
  Changes propagate automatically through the reactive graph
  Each layer adds intelligence/processing
  Each layer exposes a "call surface" (API) to the next layer

---

Infrastructure-as-Code:

The stack.yaml defines:
- Which agents exist (marimo notebooks)
- What layers they occupy
- How data flows between them
- Runtime requirements (ports, resources, env vars)

Deployment tool reads stack.yaml and:
- Starts each marimo notebook as a service
- Configures networking between them
- Sets up health checks and restarts
- Generates systemd/docker/k8s configs as needed

---

Why This Is Powerful:

1. Visual debugging: Each layer has a marimo UI
2. Live editing: Edit any layer while stack runs
3. Type safety: Can use Python typing across layers
4. Testability: Test each layer in isolation
5. Reactive: Changes propagate automatically
6. Introspectable: See data at every layer
7. Gradual: Add layers incrementally
"""

# =============================================================================
# EXAMPLE: Running the Stack Locally
# =============================================================================

"""
# Terminal 1: Start Layer 1
$ cd /home/user/kb-conduit
$ marimo run agents/context_loader.py --port 2718
✓ Context Loader running at http://localhost:2718

# Terminal 2: Start Layer 2
$ marimo run agents/debriefer.py --port 2720
✓ Debriefing Agent running at http://localhost:2720
✓ Connected to Layer 1 at http://localhost:2718

# Terminal 3: Start Layer 3 (interactive mode)
$ marimo edit agents/concierge.py --port 2722
✓ Concierge Agent running at http://localhost:2722
✓ Connected to Layer 1 at http://localhost:2718
✓ Connected to Layer 2 at http://localhost:2720

# Now you have a 3-layer stack:
# - Edit any layer's code live
# - See changes propagate through the stack
# - Inspect data at any layer via browser UI
# - Approve/execute actions from Layer 3 UI

# Deploy with one command (if using IaC schema):
$ kb-conduit-stack deploy --config examples/complex-stack.yaml
"""
