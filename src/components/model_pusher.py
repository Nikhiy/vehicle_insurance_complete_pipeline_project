import sys
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.utils.main_utils import save_object, load_object
from dataclasses import dataclass

@dataclass
class ModelPusherArtifact:
    model_path: str

class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact, model_pusher_config: ModelPusherConfig):
        self.model_pusher_config = model_pusher_config
        self.model_evaluation_artifact = model_evaluation_artifact

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered initiate_model_pusher method of ModelPusher class")
        try:
            print("------------------------------------------------------------------------------------------------")
            if self.model_evaluation_artifact.is_model_accepted:
                logging.info("Saving best model locally")
                trained_model = load_object(self.model_evaluation_artifact.trained_model_path)
                save_object(
                    file_path=self.model_pusher_config.model_file_path,
                    obj=trained_model
                )
                model_pusher_artifact = ModelPusherArtifact(model_path=self.model_pusher_config.model_file_path)
            else:
                logging.info("Model not accepted, no push")
                model_pusher_artifact = ModelPusherArtifact(model_path=None)
            
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e, sys) from e



