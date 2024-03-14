from dependency_injector import containers, providers
from .services import PreprocessingService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            ".controllers"
        ]
    )
    preprocessor = providers.Factory(PreprocessingService)