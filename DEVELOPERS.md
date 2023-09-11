# Developer Notes

## Publishing New Releases

First, determine which semver level to bump. Use this table if you are unsure:

| Resource                    | Documentation |  Add  | Update | Remove |
|-----------------------------|:-------------:|:-----:|:------:|:------:|
| kit                         |     patch     | minor |   -    | major  |
| capability                  |     patch     | minor |   -    | major  |
| interface (optional)        |     patch     | minor | major  | major  |
| interface (required)        |     patch     | major | major  | major  |
| data model                  |     patch     | minor | major  | major  |
| data model field (optional) |     patch     | minor | major  | major  |
| data model field (required) |     patch     | major | major  | major  |

Once chosen, use:

```shell
poetry version <patch|minor|major>
```

Which will update `pyproject.toml` and print the new version:

> Bumping version from 0.1.0 to 0.1.1

Next, use [git-release] (available via [git-extras]) and pass along the updated version:

```shell
git release <version> -c
```

This will update the changelog and open your `$EDITOR` to review and make any manual changes. Once saved, the tag will
be created and pushed to Github, where the release will automatically be published to PyPI via Github Actions.

### One-Liner

To simplify the steps above, once you've chosen your semver level:

```shell
git release `poetry version <level> -s` -c
```

**NOTE:** the use of `poetry version ... -s` to only output the new version.

For example, to publish a new minor version:

```shell
git release `poetry version minor -s` -c
```


[git-extras]: https://github.com/tj/git-extras
[git-release]: https://github.com/tj/git-extras/blob/master/Commands.md#git-release