from dependency_injector import containers, providers
from services import PreprocessingService, \
                     ImageReadingService, \
                     CheckboxDetectionService, \
                     LineDetectionService, \
                     WordDetectionService, \
                     CharInputDetectionService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "controllers"
        ]
    )
    image_reader = providers.Factory(ImageReadingService)
    preprocessor = providers.Factory(PreprocessingService)
    checkbox_detector = providers.Factory(CheckboxDetectionService, preprocessor=preprocessor)
    line_detector = providers.Factory(LineDetectionService, preprocessor=preprocessor)
    word_detector = providers.Factory(WordDetectionService, preprocessor=preprocessor)
    char_input_detector = providers.Factory(CharInputDetectionService, preprocessor=preprocessor)