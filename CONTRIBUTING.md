# Contributing to KB Conduit

Thanks for considering contributing! This is a simple, focused tool - let's keep it that way.

---

## Philosophy

**KB Conduit is intentionally minimal:**
- Simple YAML files (not databases)
- Shell scripts (not frameworks)
- Token-efficient (not feature-bloated)
- Solves real problem (not theoretical)

**Before adding complexity**, ask:
- Does this solve an actual user problem?
- Is there a simpler solution?
- Can this be an optional extension?

---

## How to Contribute

### Reporting Bugs

**Open an issue** with:
- What you expected
- What actually happened
- Steps to reproduce
- Your environment (OS, shell, Claude Code version)

### Suggesting Features

**Open an issue** describing:
- The problem you're solving
- Why current functionality doesn't address it
- Proposed solution (simple as possible)

**Consider**:
- Can this be solved with current features?
- Is this a common need or edge case?
- Does it add significant complexity?

### Contributing Code

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes** (keep them focused)
4. **Test thoroughly** (at minimum, test on your own workspaces)
5. **Commit**: `git commit -m "Description"`
6. **Push**: `git push origin feature/your-feature`
7. **Open a pull request**

---

## Code Guidelines

### Shell Scripts

- **POSIX-compatible** where possible (bash OK for complex logic)
- **Fail fast**: Check for errors, exit cleanly
- **User feedback**: Echo what's happening
- **Comments**: Explain why, not what

**Example**:
```bash
#!/bin/bash
# Load workspace context from .kb-context/context.yaml

# Check if context exists (not every project needs it)
if [ ! -f ".kb-context/context.yaml" ]; then
  exit 0  # Silent success
fi

# Parse workspace (fail if malformed)
WORKSPACE=$(grep "^workspace:" .kb-context/context.yaml | sed 's/^workspace: *//')
if [ -z "$WORKSPACE" ]; then
  echo "⚠️  Error: workspace not defined"
  exit 1
fi

echo "📍 KB Context: $WORKSPACE"
```

### YAML Format

- **Simple structures** (lists and strings, avoid nesting)
- **Self-documenting** (clear key names)
- **Comments** for guidance

### Documentation

- **README.md**: User-facing, how to use
- **CONTRIBUTING.md**: Developer-facing, how to contribute
- **Inline comments**: Why this code exists

---

## Testing

**Minimum testing** before submitting PR:

1. **Install from scratch**: `./install.sh`
2. **Create test workspace**: Use template
3. **Load context**: Verify it works
4. **Check logs**: Verify session.log written correctly
5. **Test edge cases**: Missing files, malformed YAML, etc.

**Bonus**:
- Test on different shells (bash, zsh)
- Test on different OS (macOS, Linux)

---

## Pull Request Process

1. **One feature per PR** (easier to review)
2. **Clear description** of what and why
3. **Test results** (what you tested, what works)
4. **Documentation updated** (if adding/changing features)

**Review criteria**:
- Does it solve a real problem?
- Is it the simplest solution?
- Does it break existing functionality?
- Is it well-tested?

---

## Areas for Contribution

### High Value, Low Complexity

- **More template examples** (different workspace types)
- **Better error messages** (helpful, actionable)
- **Documentation improvements** (clearer explanations, more examples)
- **Example CLAUDE.md integrations** (how to use in different project types)

### Medium Complexity

- **Context search tool** (`kb-search.sh` to find contexts)
- **Validation script** (check context.yaml format)
- **Integration examples** (with other tools/frameworks)

### Future Extensions (High Complexity)

- **Hook integration** (auto-load on `cd`)
- **Cross-workspace references**
- **Debriefing agent implementation**
- **Concierge agent for workspace coordination**

**Note**: High complexity features should be optional extensions, not core.

---

## What NOT to Contribute

**Please don't**:
- Add complex dependency management
- Implement formal versioning without demonstrating need
- Add databases/frameworks for data that fits in YAML
- Over-engineer solutions to hypothetical problems

**Remember**: This tool was shipped in one day by cutting complexity. Let's keep it that way.

---

## Questions?

**Open an issue** or reach out to [@devvyn](https://github.com/devvyn)

---

**Thank you for contributing to KB Conduit!** 🚀
