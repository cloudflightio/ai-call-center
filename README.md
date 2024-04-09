# Voice 2 Order Pipeline

__Please read through this whole file before joining us on the Tech Visit. The setup can take some time so it would be great if you manage to install the environment before we start.__

## Poetry and your IDE interpreter
Since you're reading this, you've already found the right repository to clone into your favorite IDE. Do that as a first step.

It is recommended to set up the project under Linux / WSL, otherwise we can't guarantee a smooth experience when installing dependencies.

The project uses [Poetry](https://python-poetry.org/) for dependency management, we recommend you do the same. See their website for installation instructions. Use the `curl` install, not the `pipx` one. Once Poetry is installed, install dependencies using `poetry install` and make sure your IDE uses poetry's virtual environment when executing code. In VS Code you can set the interpreter in the bottom right once you have a python file opened (see image below). The installation takes quite a while since the Torch library is installed which depends on some huge CUDA libraries. So, do this before the workshop.

![snip.PNG](snip.PNG)

### Installing in Detail
The simplest way to develop is to open the project in a dev-container usin the specified dev-container file. This way all dependencies are properly installed. Otherwise, make sure you use a virtual environment generated by Poetry.

The repository uses `poetry` to manage dependencies and `pre-commit` to ensure code quality. To install the dependencies run `poetry install` and to run any module `poetry run python -m .vto_pipeline.module_name`. You can also use the `poetry shell` command to spawn a shell that uses the poetry venv. Pre-commit can be installed using pip `pip install pre-commit`. Then use `pre-commit install` to make sure you can commit locally when not being in the dev-container.

## Configuration
The keys for our ChatGPT endpoint are stored in a `.env` file (will be pushed later), and the endpoint in the `config.yml` file. The `.env` file is normally in the `.gitignore` so that these secrets are not uploaded to the internet. The `settings.py` file uses pydantic to automatically load these secrets into the pipeline object. The config file also contains settings like the paths to the data objects and LLM models.

## Running the pipeline
This project uses dependency injection to ensure consistency between all the objects in the pipeline. The `main.py` file shows how to create the container that contains all the objects with the correct configuration. The pipeline container object contains all objects needed to run the pipeline to generate orders for text messages.

The orchestrator of the pipeline is `OrderProposalService`. This contains one main method required to run through a task:
```python
order_proposal = order_generator.from_text(text)
```

To run the pipeline from text to order there is a predefined configuration to run it faster: `poetry run pipeline`. This command runs `main.py` for one order example. This only works after the `load_example_order()` succesfully finds data, and once the `entity_recognition.py` has been implemented. You will be doing this in the workshop!

## Running tests
There are two groups of tests: They are marked using pytest as `unit` and `integration`. Run them using `pytest -m unit` or `pytest -m integration`. Unit tests normally use mocked clients and can be executed without any connection to clients. Integration tests test that the clients work as expected. For the workshop we don't provide mocked clients, so most unit tests are actually also integration tests. During the workshop you can run the tests to see if your implementation works as it should. 