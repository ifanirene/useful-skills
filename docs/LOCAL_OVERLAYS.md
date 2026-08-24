# Local overlays

The public Skill registry contains reusable behavior only. Machine-specific paths, aliases,
credentials, private data, and runtime artifacts belong under the ignored `.local/` directory
or outside this checkout.

Use one subdirectory per Skill:

```text
.local/
└── <skill-name>/
    ├── env             # optional environment assignments; never auto-source
    ├── aliases.json    # private names and routes
    ├── runtime/        # private inputs and generated artifacts
    └── README.md       # private operator notes
```

Public Skills may document this contract and placeholder variable names. They must not record
real values. Agents should read only the overlay fields needed for the current task and must
not print credentials or private paths in logs, reports, or public files.

The entire `.local/` tree is gitignored and excluded from public-content validation. This is a
local projection, not part of the canonical registry or a portable configuration mechanism.
