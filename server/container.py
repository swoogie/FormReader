from dependency_injector import containers, providers
from services import PreprocessingService, ImageReadingService, CheckboxDetectionService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "controllers"
        ]
    )
    image_reader = providers.Factory(ImageReadingService)
    preprocessor = providers.Factory(PreprocessingService)
    checkbox_detector = providers.Factory(CheckboxDetectionService)