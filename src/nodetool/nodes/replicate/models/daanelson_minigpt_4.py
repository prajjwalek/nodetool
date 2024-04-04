schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'required': ['image', 'prompt'], 'properties': {'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 0, 'description': 'Image to discuss'}, 'top_p': {'type': 'number', 'title': 'Top P', 'default': 0.9, 'maximum': 1, 'minimum': 0, 'x-order': 4, 'description': 'Sample from the top p percent most likely tokens'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'x-order': 1, 'description': 'Prompt for mini-gpt4 regarding input image'}, 'num_beams': {'type': 'integer', 'title': 'Num Beams', 'default': 3, 'maximum': 10, 'minimum': 1, 'x-order': 2, 'description': 'Number of beams for beam search decoding'}, 'max_length': {'type': 'integer', 'title': 'Max Length', 'default': 4000, 'minimum': 1, 'x-order': 7, 'description': 'Total length of prompt and output in tokens'}, 'temperature': {'type': 'number', 'title': 'Temperature', 'default': 1, 'maximum': 2, 'minimum': 0.01, 'x-order': 3, 'description': 'Temperature for generating tokens, lower = more predictable results'}, 'max_new_tokens': {'type': 'integer', 'title': 'Max New Tokens', 'default': 3000, 'minimum': 1, 'x-order': 6, 'description': 'Maximum number of new tokens to generate'}, 'repetition_penalty': {'type': 'number', 'title': 'Repetition Penalty', 'default': 1, 'maximum': 5, 'minimum': 0.01, 'x-order': 5, 'description': 'Penalty for repeated words in generated text; 1 is no penalty, values greater than 1 discourage repetition, less than 1 encourage it.'}}}, 'Output': {'type': 'string', 'title': 'Output'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['output', 'logs', 'completed', 'start'], 'uniqueItems': True}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'daanelson/minigpt-4'
model_version = 'b96a2f33cc8e4b0aa23eacfce731b9c41a7d9466d9ed4e167375587b54db9423'
model_info = {'cover_image_url': 'https://tjzk.replicate.delivery/models_models_cover_image/af717919-83de-46e8-9b1a-9c66f4f747bf/out_0.png', 'created_at': '2023-05-16T19:05:24.691944Z', 'default_example': {'completed_at': '2023-05-17T23:27:47.968519Z', 'created_at': '2023-05-17T23:27:31.030303Z', 'error': None, 'id': 'u6yurll6v5f6xjl2q47dudq3sy', 'input': {'image': 'https://replicate.delivery/pbxt/IqG1MbemhULihtfr62URRZbI29XtcPsnOYASrTDQ6u5oSqv9/llama_13b.png', 'top_p': 0.9, 'prompt': "This llama's name is Dave. Write me a story about how Dave found his skateboard.", 'num_beams': 5, 'max_length': 4000, 'temperature': 1.32, 'max_new_tokens': 3000, 'repetition_penalty': 1}, 'logs': None, 'metrics': {'predict_time': 16.967653, 'total_time': 16.938216}, 'output': 'Dave the llama was feeling very bored one day. He had been wandering around the city for hours, but there was nothing interesting to do. Suddenly, he saw a skateboard lying on the ground. He decided to try it out, and as soon as he started riding it, he felt a rush of excitement. He rode around the city, enjoying the feeling of the wind in his hair and the freedom of being on his own. As he rode, he saw all sorts of interesting things that he had never noticed before. He even met some new friends along the way. After a while, Dave realized that he had found his true passion - skateboarding. From then on, he spent all his free time riding his skateboard and exploring the city.', 'started_at': '2023-05-17T23:27:31.000866Z', 'status': 'succeeded', 'urls': {'get': 'https://api.replicate.com/v1/predictions/u6yurll6v5f6xjl2q47dudq3sy', 'cancel': 'https://api.replicate.com/v1/predictions/u6yurll6v5f6xjl2q47dudq3sy/cancel'}, 'model': 'daanelson/minigpt-4', 'version': 'b96a2f33cc8e4b0aa23eacfce731b9c41a7d9466d9ed4e167375587b54db9423', 'webhook_completed': None}, 'description': 'A model which generates text in response to an input image and prompt.', 'github_url': 'https://github.com/daanelson/MiniGPT-4', 'latest_version': {'id': 'b96a2f33cc8e4b0aa23eacfce731b9c41a7d9466d9ed4e167375587b54db9423', 'created_at': '2023-05-16T22:51:57.306442Z', 'cog_version': 'v0.7.0-beta17+dev', 'openapi_schema': {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'required': ['image', 'prompt'], 'properties': {'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 0, 'description': 'Image to discuss'}, 'top_p': {'type': 'number', 'title': 'Top P', 'default': 0.9, 'maximum': 1, 'minimum': 0, 'x-order': 4, 'description': 'Sample from the top p percent most likely tokens'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'x-order': 1, 'description': 'Prompt for mini-gpt4 regarding input image'}, 'num_beams': {'type': 'integer', 'title': 'Num Beams', 'default': 3, 'maximum': 10, 'minimum': 1, 'x-order': 2, 'description': 'Number of beams for beam search decoding'}, 'max_length': {'type': 'integer', 'title': 'Max Length', 'default': 4000, 'minimum': 1, 'x-order': 7, 'description': 'Total length of prompt and output in tokens'}, 'temperature': {'type': 'number', 'title': 'Temperature', 'default': 1, 'maximum': 2, 'minimum': 0.01, 'x-order': 3, 'description': 'Temperature for generating tokens, lower = more predictable results'}, 'max_new_tokens': {'type': 'integer', 'title': 'Max New Tokens', 'default': 3000, 'minimum': 1, 'x-order': 6, 'description': 'Maximum number of new tokens to generate'}, 'repetition_penalty': {'type': 'number', 'title': 'Repetition Penalty', 'default': 1, 'maximum': 5, 'minimum': 0.01, 'x-order': 5, 'description': 'Penalty for repeated words in generated text; 1 is no penalty, values greater than 1 discourage repetition, less than 1 encourage it.'}}}, 'Output': {'type': 'string', 'title': 'Output'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['output', 'logs', 'completed', 'start'], 'uniqueItems': True}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}}, 'license_url': 'https://github.com/Vision-CAIR/MiniGPT-4/blob/main/LICENSE.md', 'name': 'minigpt-4', 'owner': 'daanelson', 'paper_url': 'https://arxiv.org/pdf/2304.10592.pdf', 'run_count': 1228987, 'url': 'https://replicate.com/daanelson/minigpt-4', 'visibility': 'public', 'hardware': 'Nvidia A100 (40GB) GPU'}
