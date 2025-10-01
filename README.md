# KB Conduit

**Context management for Claude Code across multiple workspaces**

Stop copy/pasting context between work and personal projects. Define workspace context once, agent loads it automatically.

---

## The Problem

Working on multiple projects means explaining context repeatedly:
- "I'm at work now, here's my supervisor..."
- "I'm home now, different policies apply..."
- Copy/paste between workspaces
- Token waste on redundant explanations
- Context confusion when switching

## The Solution

**Define context once per workspace:**

```yaml
# .kb-context/context.yaml
workspace: "AAFC-SRDC Saskatoon"
contexts:
  - herbarium_specimen_digitization
  - darwin_core_extraction
people:
  - me: "Devvyn Murphy"
  - supervisor: "Jane Doe"
policies:
  - "Public employee policies"
clues:
  - "herbarium"
  - "specimen"
```

**Load automatically at session start:**

```bash
cd ~/work-project
~/.kb-conduit/load-context.sh

# 📍 KB Context: AAFC-SRDC Saskatoon
# ✓ Context loaded successfully
```

**Agent knows where you are:**
- Mention "herbarium" → agent references work context
- Mention "personal project" → agent references home context
- No copy/paste, no re-explaining

---

## Quick Start

### 1. Install

```bash
# Clone repository
git clone https://github.com/devvyn/kb-conduit.git
cd kb-conduit

# Run installer
./install.sh
```

### 2. Create workspace context

```bash
# Copy template
mkdir -p ~/my-project/.kb-context
cp ~/.kb-conduit/templates/context.yaml ~/my-project/.kb-context/

# Edit context.yaml with your workspace info
```

### 3. Load context

```bash
cd ~/my-project
~/.kb-conduit/load-context.sh
```

Done. Agent has context.

---

## How It Works

### Context Files

Each workspace has a `.kb-context/context.yaml`:

```yaml
workspace: "Workspace Name"

contexts:
  - area_of_focus_1
  - area_of_focus_2

people:
  - me: "Your Name"
  - collaborator: "Their Role"

policies:
  - "Relevant policy or guideline"

clues:
  # Keywords that trigger this context
  - "keyword1"
  - "keyword2"
```

### Session Loading

At session start, run:

```bash
~/.kb-conduit/load-context.sh
```

This:
- Reads `.kb-context/context.yaml`
- Exports context to environment
- Logs session for agent handoff
- Displays workspace info

### Agent Awareness

Update your project's `CLAUDE.md`:

```markdown
## KB Context Awareness

At session start, I load `.kb-context/context.yaml`.

When you mention clue keywords, I reference workspace context:
- "keyword1" → loads relevant context
- Token-efficient (details loaded on demand)
```

### Session Logs

All context loads logged to `~/.kb-conduit/logs/session.log`:

```yaml
---
timestamp: 2025-10-01T08:42:17Z
workspace: "AAFC-SRDC Saskatoon"
context_file: ".kb-context/context.yaml"
pwd: "/Users/devvynmurphy/Documents/GitHub/aafc-herbarium-dwc-extraction-2025"
session_id: code-17172
```

Purpose: Debriefing/concierge agents can read session history and understand workspace context across sessions.

---

## Example Workspaces

### Work Project

```yaml
workspace: "AAFC-SRDC Saskatoon"

contexts:
  - herbarium_specimen_digitization
  - darwin_core_extraction
  - ocr_optimization

people:
  - me: "Devvyn Murphy"
  - supervisor: "Research Lead"
  - organization: "AAFC-SRDC"

policies:
  - "Public employee policies"
  - "Data sensitivity: Public scientific data"

clues:
  - "herbarium"
  - "specimen"
  - "Darwin Core"
  - "AAFC"
```

### Personal Project

```yaml
workspace: "Meta-Project (Personal)"

contexts:
  - multi_agent_collaboration
  - bridge_system_coordination
  - security_architecture

people:
  - me: "Devvyn Murphy"
  - household: "Spouse coordination"

policies:
  - "Personal sovereignty"
  - "Open source (MIT licensed)"

clues:
  - "bridge"
  - "meta-project"
  - "coordination"
```

---

## Token Efficiency

**Problem**: Loading all context upfront wastes tokens

**Solution**: Clue-based retrieval

**Implementation**:
- Context not pre-loaded
- Agent retrieves details when clues mentioned
- Cached for session duration

**Result**: Minimal token usage, maximum context awareness

---

## Benefits

| Without KB Conduit | With KB Conduit |
|-------------------|-----------------|
| Copy/paste context | Drop clues → agent knows |
| Explain people each session | Defined once in context.yaml |
| Token waste on redundancy | Token-efficient loading |
| Manual context switching | Automatic workspace detection |
| No agent handoff | Session logs for continuity |

---

## Installation

### Automatic

```bash
git clone https://github.com/devvyn/kb-conduit.git
cd kb-conduit
./install.sh
```

This creates:
```
~/.kb-conduit/
├── README.md
├── load-context.sh
├── templates/
│   └── context.yaml
└── logs/
    └── session.log
```

### Manual

1. Copy files to `~/.kb-conduit/`
2. Make `load-context.sh` executable: `chmod +x ~/.kb-conduit/load-context.sh`
3. Create `.kb-context/context.yaml` in your projects
4. Update project `CLAUDE.md` files with KB Context awareness

---

## Usage

### Creating New Workspace Context

```bash
# 1. Copy template
mkdir -p ~/my-project/.kb-context
cp ~/.kb-conduit/templates/context.yaml ~/my-project/.kb-context/

# 2. Edit context
vim ~/my-project/.kb-context/context.yaml

# 3. Load at session start
cd ~/my-project
~/.kb-conduit/load-context.sh
```

### Updating Context

Edit `.kb-context/context.yaml` in your project:
- Add/remove context areas
- Update people/policies
- Add new clue keywords

Changes take effect next session.

### Viewing Session History

```bash
# See all workspace switches
cat ~/.kb-conduit/logs/session.log

# See recent sessions
tail ~/.kb-conduit/logs/session.log
```

---

## Integration with Claude Code

### CLAUDE.md Template

Add to your project's `CLAUDE.md`:

```markdown
## KB Context Awareness

**At session start**, I load workspace context from `.kb-context/context.yaml`.

### Workspace Context

Run `~/.kb-conduit/load-context.sh` to see current workspace.

### Clue-Based Retrieval

When you mention clue keywords, I reference workspace context:
- [List your workspace-specific clues]

### Token Efficiency

- Context not pre-loaded
- Details loaded when clues mentioned
- Cached for session

### Session Logging

Actions logged to `~/.kb-conduit/logs/session.log` for agent handoff.
```

### Session Startup Checklist

Update your session startup to include:

```markdown
## Session Startup Checklist

1. ✅ **Load KB Context**: `~/.kb-conduit/load-context.sh`
2. ✅ [Your other startup steps]
```

---

## Architecture

### Design Principles

1. **Simple over complex**: YAML files, not databases
2. **Token efficient**: Clue-based loading, not pre-loading
3. **Agent handoff**: Session logs for continuity
4. **Real context**: Solve actual problem, not theoretical

### File Structure

```
~/.kb-conduit/
├── README.md              # Documentation
├── load-context.sh        # Context loader
├── templates/
│   └── context.yaml       # Template for new workspaces
└── logs/
    └── session.log        # Session history

PROJECT/.kb-context/
└── context.yaml           # Workspace-specific context
```

### Context Format

**Minimal required**:
```yaml
workspace: "Name"
contexts: []
people: []
policies: []
clues: []
```

**Full example**: See `templates/context.yaml`

---

## Future Extensions

**Possible additions** (not implemented yet):
- Hook integration (auto-load on `cd`)
- Context search tool
- Cross-workspace references
- Version management
- Community context library

**Current philosophy**: Start simple. Ship. Iterate based on real use.

---

## Contributing

Contributions welcome! This is a minimal viable implementation.

**Ideas for contribution**:
- Additional template examples
- Integration with other AI coding tools
- Debriefing/concierge agent implementations
- Context search utilities
- Documentation improvements

See `CONTRIBUTING.md` for guidelines.

---

## License

MIT License - See `LICENSE` file

---

## Credits

**Built by**: Devvyn Murphy ([@devvyn](https://github.com/devvyn))

**Built in**: One day (2025-10-01)

**Philosophy**: Simple solutions to real problems. Ship fast, iterate based on use.

---

## Related Projects

- [Multi-Agent Collaboration Framework](https://github.com/devvyn/devvyn-meta-project) - Coordination infrastructure this builds on
- [Claude Code](https://claude.ai/code) - The AI coding assistant this integrates with

---

## FAQ

**Q: Does this work with other AI coding tools?**
A: Currently designed for Claude Code. Concept could adapt to other tools with context awareness.

**Q: How do I share contexts between workspaces?**
A: Currently each workspace has independent context. Cross-workspace references are a future extension.

**Q: What if I don't have a `.kb-context/` directory?**
A: Script silently skips (not every project needs context). No error.

**Q: Can agents read each other's session logs?**
A: Yes - that's the point. Session logs in YAML format for easy parsing by debriefing/concierge agents.

**Q: Is this over-engineered?**
A: No. This is the minimal viable implementation. Research phase considered formal proofs, versioning, complex dependency resolution - all cut in favor of simple solution that works.

---

**Start using KB Conduit**: `git clone https://github.com/devvyn/kb-conduit.git && cd kb-conduit && ./install.sh`
