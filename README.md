# rippling-flux-sdk

Defines the interfaces and data-models used by Rippling Flux Apps.

The **distribution name** for this project is `rippling-flux-sdk`, which is how it is listed in PyPI. Once added as a
dependency though, use the name `flux_sdk` as the **import name**.

The imports for this package should be included in the scaffolding for a Flux App, in general Flux app developers will
not need to write that code. By being distributed as a package, it will allow your IDE to inspect the defined types for
additional context.