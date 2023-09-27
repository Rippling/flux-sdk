# Developer Notes

## Publishing New Releases

Each merge to the `main` branch will create a new release using the format `<major>.<minor>.<build number>`.

The `<major>` and `<minor>` need to be updated in the PR which introduces the change:

| Resource                    |  Add  | Update | Remove |
|-----------------------------|:-----:|:------:|:------:|
| kit                         | minor |   -    | major  |
| capability                  | minor |   -    | major  |
| interface (optional)        | minor | major  | major  |
| interface (required)        | major | major  | major  |
| data model                  | minor | major  | major  |
| data model field (optional) | minor | major  | major  |
| data model field (required) | major | major  | major  |

The `<build number>` is an always-increasing number from the "publish" GitHub Actions workflow.