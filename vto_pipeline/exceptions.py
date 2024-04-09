class CategoryNotFoundError(Exception):
    message: str = "An entity of the requested category could not be found in the group."


class EntityGroupingError(Exception):
    message: str = "Unable to find valid groups. There was an error in the list of entities provided."


class EntityGroupMappingError(Exception):
    message: str = "Can't perform mapping on an invalid group."


class NoMatchError(Exception):
    def __init__(self, task_id: str, query: str) -> None:
        self.task_id = task_id
        self.query = query

    @property
    def message(self) -> str:
        return f"No match found for query: '{self.query}' (task: {self.task_id})"


class NoProductsRecognizedError(Exception):
    message: str = "No products were recognized, order proposal empty."


class ChatGPTResponseProcessingError(Exception):
    def __init__(self, response: str) -> None:
        self.response = response

    @property
    def message(self) -> str:
        return f"Unable to process chatGPT response into a list of dicts: '{self.response}'"


class OrderGenerationError(Exception):
    def __init__(self, task_id: str, error: Exception):
        self.task_id = task_id
        self.error = error

    @property
    def message(self) -> str:
        return f"An error occured during order generation for task {self.task_id}: {self.error}"
