# Peregrine Advisors Python Challenges

Love 💕 the unwaivering persisent effort to always learn more and expanding one's 🧠 ; hate the attitude 👌✨

A set of small Python scripts that solve operations and security problems: tracing
the impact of a service outage, flagging brute-force login attempts, and checking
deployment state changes.

## Requirements

- Python 3.10 or newer
- No third-party packages. Every script uses only the standard library.

## Running the scripts

Clone the repo and run any script from the project folder:

```bash
git clone [text](https://github.com/smueg/Peregrine_Advisors_Py.git)
cd Peregrine_Advisors_Py
python blast_radius_challenge.py
```

In VS Code or a GitHub Codespace, open a script and press **F5**. The included
`.vscode/launch.json` runs the file that is currently open.

## The challenges

### Blast radius: `blast_radius_challenge.py`

Takes a list of `(caller, callee)` service dependencies and, for a service that
fails, finds every service that depends on it, directly or indirectly. It walks
the dependency graph breadth-first with a `deque`.

```
Service Name: auth
Affected Services: admin, cdn, checkout, mobile-api, payments, web

Service Name: etl
Affected Services: admin, reports, warehouse

Service Name: storage
Affected Services: cdn, checkout, index, ledger, mobile-api, payments, search, web

Service Name: cdn
Affected Services: None
```

### Brute-force detection

Finds IP addresses with **more than 3 access attempts within any 60-second window**.

- `brute_force_challenge_v1.py`: attempts are hard-coded in the script.
- `brute_force_challenge-json-parse_v2.py`: attempts are loaded from
  `json/attempts.json`. Malformed entries are reported and skipped.

```
Suspicious ⚠ IPs:
-----------------
IPv4 Address: 172.16.5.20 | 🔥 4 attempts within 🚨 60 seconds
IPv4 Address: 203.0.113.5 | 🔥 4 attempts within 🚨 60 seconds
```

### Deployment lifecycle: `deploy_lifecycle_challenge.py`

Checks an unsorted list of `(deploy_id, sequence_number, event)` records against
a table of allowed state transitions (`queued → approved → deploying → succeeded`, and
so on). Reports each deployment that breaks the rules and the sequence number of its
first illegal event.

```
Invalid deployments:
deploy-2 > First illegal event at sequence: 2
deploy-4 > First illegal event at sequence: 5
deploy-5 > First illegal event at sequence: 1
deploy-6 > First illegal event at sequence: 3
deploy-8 > First illegal event at sequence: 6
```

## Project layout

```
.
├── blast_radius_challenge.py
├── brute_force_challenge_v1.py
├── brute_force_challenge-json-parse_v2.py
├── deploy_lifecycle_challenge.py
├── json/
│   └── attempts.json        # sample data (documentation-range IP addresses)
└── .vscode/
    └── launch.json          # F5 runs the current file
```

## Author

Stéffen Mügel 😗 💋 💘
