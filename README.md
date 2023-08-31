# flux-dev-kit

A Python module with packages for local Flux development.

## server

This sub-package contains a `flask.py` module which exports a [Flask][flask] app that will expose your `flux_apps` code
to [Rippling][rippling] servers for live testing.

The easiest way to use this is via the [Flask CLI][flask-cli], which is likely to have integration with your IDE of
choice. With `flux-dev-kit` as a dependency, you can use `--app flux_dev_kit.server.flask`, which uses this flask app
as the "target".



[flask]: https://flask.palletsprojects.com/en/2.3.x/
[flask-cli]: https://flask.palletsprojects.com/en/2.3.x/cli/
[rippling]: https://www.rippling.com/