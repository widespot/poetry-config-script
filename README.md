# poetry-config-script
> Configure Python Poetry with script on top of pyproject.toml

## Usage
Use any Python script to customize Poetry config
```toml
# pyproject.toml
[tool.poetry]
name = "poetry-config-script"
config_script = "my_package.module:poetry_config"
...
```
```python
# my_package/module.py
def poetry_config(config):
    with open('VERSION', 'r') as file:
        version = file.read()
        
    config['version'] = version
```

and later
```bash
poetry-ws ANY COMMAND
# is equivalent to
poetry ANY COMMAND
```

## Implementation
It's crazy the feature isn't in Poetry yet but the implementation is rather simple.
`poetry.core` will have a `pyproject.toml.PyProjectTOML` class responsible for parsing
the `pyproject.toml` file. And that class does have a `@property` attribute `poetry_config`
to return the configuration.

That last method was simply monkey-patched. The patched version is calling
the source implementation and passes the result to the `config_script` method 
