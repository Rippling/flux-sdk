# rippling-flux-sdk

Defines the interfaces and data-models used by Rippling Flux Apps.

The **distribution name** for this project is `rippling-flux-sdk`, which is how it is listed in PyPI. Once added as a
dependency though, use the name `flux_sdk` as the **import name**.

The imports for this package should be included in the scaffolding for a Flux App, in general Flux app developers will
not need to write that code. By being distributed as a package, it will allow your IDE to inspect the defined types for
additional context.


## Getting Started

Code is linted with ruff.  It's recommended to run `./install_hooks.sh` to run linting on commit.
Linting can also be run manually with `./run_ruff.sh`.  In many cases it's possible to auto-fix
linting errors with `./run_ruff.sh --fix`.
