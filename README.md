# rippling.flux-sdk

A Python package with modules useful for local Flux app development.

## server

This sub-package contains a `flask` module which exports a [Flask][flask] app that will make your `flux_apps/` code 
available to [Rippling][rippling] servers for live debugging sessions.

The easiest way to use this is via the [Flask CLI][flask-cli], which is likely to have integration with your IDE of
choice. With `rippling.flux-sdk` installed as a dependency, you can use `--app flux_sdk.server.flask`, which uses this
flask app  as the "app target".

```shell
python -m flask --app rippling.flux_sdk.server.flask run
```

[flask]: https://flask.palleprtsprojects.com/en/2.3.x/
[flask-cli]: https://flask.palletsprojects.com/en/2.3.x/cli/
[rippling]: https://www.rippling.com/