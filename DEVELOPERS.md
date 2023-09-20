# Developer Notes

## Publishing New Releases

First, create a new release branch, using the naming convention "release/<new version>":

```shell
git checkout -b release/0.1.1
```

Next, determine which semver level to bump. Use this table if you are unsure:

| Resource                    | Documentation |  Add  | Update | Remove |
|-----------------------------|:-------------:|:-----:|:------:|:------:|
| kit                         |     patch     | minor |   -    | major  |
| capability                  |     patch     | minor |   -    | major  |
| interface (optional)        |     patch     | minor | major  | major  |
| interface (required)        |     patch     | major | major  | major  |
| data model                  |     patch     | minor | major  | major  |
| data model field (optional) |     patch     | minor | major  | major  |
| data model field (required) |     patch     | major | major  | major  |

Then, execute the following in your release branch.

```shell
poetry version <patch|minor|major>
```

Which will update `pyproject.toml` and print the new version:

> Bumping version from 0.1.0 to 0.1.1

Commit this change and open a Pull Request with your branch. Once approved and merged, create a new release using the
GitHub Releases UI:
- tag: create a new tag using the new version (eg: "0.1.1")
- title: "Release <new version>" (eg: "Release 0.1.1")
- description: click "Generate release notes" to allow GitHub to automate this

Once published, a GitHub Actions workflow will take care of publishing the new release to PyPI.