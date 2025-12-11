# ANTIVIRUS Modules

## Overview

ANTIVIRUS is organized into focused modules, each with a specific responsibility. This document provides detailed information about each module.

---

## Core Modules

### `antivirus.core.scanner`

**Purpose**: File and directory scanning orchestration.

**Key Classes**:
- `FileScanner`: Scans individual files
- `DirectoryScanner`: Recursively scans directories
- `ProcessScanner`: Scans running processes

**Usage**:
```python
from antivirus.core.scanner import FileScanner

scanner = FileScanner()
result = scanner.scan("/path/to/file")

if result.is_threat:
    print(f"Threat detected: {result.threat_name}")
```

**Configuration**:
- `max_file_size`: Maximum file size to scan (default: 100MB)
- `skip_extensions`: Extensions to skip (e.g., ['.iso', '.img'])
- `follow_symlinks`: Whether to follow symbolic links

---

### `antivirus.core.detector`

**Purpose**: Threat detection using multiple methods.

**Key Classes**:
- `HashDetector`: Signature-based detection using file hashes
- `PatternDetector`: Pattern matching for malicious content
- `HeuristicDetector`: Behavioral analysis (future)

**Detection Methods**:

1. **Hash Matching**:
   ```python
   detector = HashDetector()
   threat = detector.check_hash("a1b2c3d4...")
   ```

2. **Pattern Matching**:
   ```python
   detector = PatternDetector()
   threats = detector.scan_content(file_content)
   ```

**Adding Custom Detectors**:
```python
from antivirus.core.detector import BaseDetector

class CustomDetector(BaseDetector):
    def detect(self, data):
        # Your detection logic
        if self.is_malicious(data):
            return Threat(
                name="CustomThreat",
                severity="HIGH",
                description="Custom detection"
            )
        return None
```

---

### `antivirus.core.analyzer`

**Purpose**: Risk analysis and threat assessment.

**Key Classes**:
- `ThreatAnalyzer`: Analyzes and scores threats
- `RiskScorer`: Calculates risk scores (0-100)

**Risk Factors**:
- File extension
- Hash match confidence
- Pattern match count
- Behavioral indicators (future)

**Usage**:
```python
from antivirus.core.analyzer import ThreatAnalyzer

analyzer = ThreatAnalyzer()
score = analyzer.calculate_risk(scan_result)
# score: 0-100, where 100 is most dangerous
```

---

## Agent Modules

### `antivirus.agents.file`

**Purpose**: File system monitoring and scanning.

**Capabilities**:
- File metadata collection
- Permission analysis
- Hash calculation (MD5, SHA1, SHA256)
- Content analysis

**Example**:
```python
from antivirus.agents.file import FileAgent

agent = FileAgent()
metadata = agent.get_metadata("/path/to/file")
print(f"Size: {metadata.size}, Hash: {metadata.sha256}")
```

---

### `antivirus.agents.process`

**Purpose**: Process monitoring and analysis.

**Capabilities**:
- Process enumeration
- Process tree analysis
- Connection monitoring
- Resource usage tracking

**Example**:
```python
from antivirus.agents.process import ProcessAgent

agent = ProcessAgent()
processes = agent.get_running_processes()
for proc in processes:
    if agent.is_suspicious(proc):
        print(f"Suspicious: {proc.name} (PID: {proc.pid})")
```

---

### `antivirus.agents.network` (Future - Phase 5)

**Purpose**: Network traffic monitoring.

**Planned Capabilities**:
- Connection tracking
- Traffic analysis
- C2 detection
- Port scanning detection

---

### `antivirus.agents.memory` (Future - Phase 3)

**Purpose**: Memory analysis and injection detection.

**Planned Capabilities**:
- Memory scanning
- Code injection detection
- Rootkit detection

---

## Database Modules

### `antivirus.database.signatures`

**Purpose**: Manage malware signature database.

**Structure**:
```json
{
  "version": "1.0",
  "signatures": [
    {
      "id": "SIG001",
      "name": "Threat Name",
      "type": "malware_type",
      "hashes": {
        "md5": "...",
        "sha1": "...",
        "sha256": "..."
      },
      "severity": "CRITICAL|HIGH|MEDIUM|LOW"
    }
  ]
}
```

**API**:
```python
from antivirus.database import SignatureDB

db = SignatureDB()
threat = db.lookup_hash("a1b2c3d4...")
db.add_signature(new_signature)
db.update()  # Fetch latest signatures
```

---

### `antivirus.database.patterns`

**Purpose**: Store and match malicious patterns.

**Pattern Types**:
- Regular expressions
- Byte patterns
- Script patterns

**Example Pattern**:
```json
{
  "id": "PAT001",
  "name": "eval-injection",
  "type": "code_pattern",
  "regex": "eval\\s*\\([^)]*\\)",
  "severity": "HIGH",
  "description": "Dangerous eval() usage"
}
```

---

## Utility Modules

### `antivirus.utils.logger`

**Purpose**: Semantic logging with context.

**Features**:
- Structured logging
- Multiple output formats (console, file, JSON)
- Severity levels
- Context tracking

**Usage**:
```python
from antivirus.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Scanning started", path="/home/user")
logger.warning("Suspicious file found", 
               file="script.sh", 
               reason="eval pattern")
```

**Log Format**:
```
[2024-01-01 10:30:45] [INFO] [scanner] Scanning started: path=/home/user
[2024-01-01 10:30:46] [WARN] [detector] Suspicious file: script.sh (eval pattern)
```

---

### `antivirus.utils.reporter`

**Purpose**: Generate scan reports in various formats.

**Supported Formats**:
- Console (colored, formatted)
- JSON
- HTML (future)
- PDF (future)

**Usage**:
```python
from antivirus.utils.reporter import Reporter

reporter = Reporter(format="console")
reporter.add_result(scan_result)
reporter.generate()
```

**Console Output**:
```
🛡️ ANTIVIRUS Scan Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[CRITICAL] threat.exe
  Hash: a1b2c3d4...
  Type: Ransomware
  Action: Quarantine immediately

[HIGH] malicious.sh
  Pattern: eval injection
  Line: 42
  Action: Review and remove

Summary:
  Scanned: 1,234 files
  Threats: 2 (1 CRITICAL, 1 HIGH)
  Clean: 1,232
  Duration: 5.2s
```

---

### `antivirus.utils.hasher`

**Purpose**: File hashing utilities.

**Supported Algorithms**:
- MD5
- SHA1
- SHA256
- SHA512

**Usage**:
```python
from antivirus.utils.hasher import hash_file

hashes = hash_file("/path/to/file", algorithms=["md5", "sha256"])
print(hashes["sha256"])
```

---

## CLI Module

### `antivirus.cli.main`

**Purpose**: Command-line interface entry point.

**Commands**:

```bash
# Scan a path
antivirus scan <path> [--recursive] [--follow-links]

# Scan processes
antivirus scan-processes [--all]

# Scan downloads
antivirus scan-downloads

# Update signatures
antivirus update

# Show version
antivirus version

# Configure
antivirus config [--set key=value]
```

**Command Implementation**:
```python
import click

@click.command()
@click.argument('path')
@click.option('--recursive', '-r', is_flag=True)
def scan(path, recursive):
    """Scan a file or directory for threats."""
    scanner = FileScanner()
    results = scanner.scan(path, recursive=recursive)
    reporter = Reporter()
    reporter.display(results)
```

---

## Configuration Module

### `antivirus.config`

**Purpose**: Application configuration management.

**Config File**: `~/.antivirus/config.json`

**Default Configuration**:
```json
{
  "scanning": {
    "max_file_size": 104857600,
    "skip_extensions": [".iso", ".img"],
    "follow_symlinks": false,
    "threads": 4
  },
  "database": {
    "auto_update": true,
    "update_interval": 86400
  },
  "reporting": {
    "format": "console",
    "verbosity": "normal",
    "color": true
  }
}
```

**API**:
```python
from antivirus.config import Config

config = Config()
max_size = config.get("scanning.max_file_size")
config.set("scanning.threads", 8)
config.save()
```

---

## Module Dependencies

```
antivirus/
├── cli/              (depends on: core, utils)
├── core/             (depends on: agents, database, utils)
│   ├── scanner       (depends on: agents, database)
│   ├── detector      (depends on: database)
│   └── analyzer      (depends on: detector)
├── agents/           (depends on: utils)
│   ├── file
│   ├── process
│   ├── network
│   └── memory
├── database/         (depends on: utils)
│   ├── signatures
│   └── patterns
├── utils/            (no dependencies)
│   ├── logger
│   ├── reporter
│   ├── hasher
│   └── config
└── config/           (no dependencies)
```

---

## Testing Modules

Each module has corresponding tests in `tests/`:

```
tests/
├── unit/
│   ├── test_scanner.py
│   ├── test_detector.py
│   ├── test_file_agent.py
│   └── ...
├── integration/
│   ├── test_full_scan.py
│   ├── test_process_scan.py
│   └── ...
└── fixtures/
    ├── malware_samples/
    ├── clean_files/
    └── test_signatures.json
```

---

## Performance Characteristics

| Module | CPU Usage | Memory Usage | I/O Intensive |
|--------|-----------|--------------|---------------|
| FileScanner | Medium | Low | High |
| ProcessScanner | Low | Low | Low |
| HashDetector | High | Low | High |
| PatternDetector | High | Medium | Medium |
| ThreatAnalyzer | Medium | Low | Low |

---

## Module Roadmap

### Phase 1 (Current)
- ✅ Core scanning modules
- ✅ File agent
- ✅ Process agent (basic)
- ✅ Hash detector
- ✅ Pattern detector

### Phase 2-3
- ⏳ Real-time monitoring
- ⏳ Network agent
- ⏳ Memory agent
- ⏳ ML-based detector

### Phase 4+
- ⏳ Sandbox module
- ⏳ Quarantine module
- ⏳ Recovery module
- ⏳ Firewall module
