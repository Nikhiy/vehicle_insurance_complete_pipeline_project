# TODO: Jenkins CI/CD + Remove AWS

## Steps from Approved Plan (3/13 complete)

### 1. Create TODO.md [COMPLETE]
### 2. Delete AWS files [PENDING - manual delete empty dirs]
### 3. Edit src/components/model_pusher.py: Remove S3, save local [COMPLETE]
### 4. Edit src/components/model_evaluation.py: Use local model paths, remove S3 [COMPLETE]
### 5. Edit src/pipline/prediction_pipeline.py: Load local [COMPLETE]
### 6. Edit entity/config_entity.py & artifact_entity.py: Remove S3 fields [COMPLETE]
### 7. Edit src/constants/__init__.py: Remove AWS vars [COMPLETE]
### 8. Edit requirements.txt: Remove boto3 [COMPLETE]
### 9. Create Jenkinsfile [COMPLETE]
### 10. Edit README.md: Jenkins + no AWS [COMPLETE]
### 11. Cleanup flow.txt, Dockerfile [COMPLETE]
### 12. Test changes [READY - run pip install -r requirements.txt && python app.py]
### 13. [DONE]

