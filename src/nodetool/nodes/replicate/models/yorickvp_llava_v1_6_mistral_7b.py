schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'required': ['prompt'], 'properties': {'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 0, 'description': 'Input image'}, 'top_p': {'type': 'number', 'title': 'Top P', 'default': 1, 'maximum': 1, 'minimum': 0, 'x-order': 2, 'description': 'When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'x-order': 1, 'description': 'Prompt to use for text generation'}, 'history': {'type': 'array', 'items': {'type': 'string'}, 'title': 'History', 'x-order': 5, 'description': 'List of earlier chat messages, alternating roles, starting with user input. Include <image> to specify which message to attach the image to.'}, 'max_tokens': {'type': 'integer', 'title': 'Max Tokens', 'default': 1024, 'minimum': 0, 'x-order': 4, 'description': 'Maximum number of tokens to generate. A word is generally 2-3 tokens'}, 'temperature': {'type': 'number', 'title': 'Temperature', 'default': 0.2, 'minimum': 0, 'x-order': 3, 'description': 'Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic'}}}, 'Output': {'type': 'array', 'items': {'type': 'string'}, 'title': 'Output', 'x-cog-array-type': 'iterator', 'x-cog-array-display': 'concatenate'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'yorickvp/llava-v1.6-mistral-7b'
model_version = '19be067b589d0c46689ffa7cc3ff321447a441986a7694c01225973c2eafc874'
model_info = {'cover_image_url': 'https://tjzk.replicate.delivery/models_models_cover_image/6bc7974c-7209-4877-98f5-23e77ef1c6da/fa58799b-aa47-4117-bf1f-25149e2d.webp', 'created_at': '2024-02-01T11:42:00.607356Z', 'default_example': {'completed_at': '2024-02-01T11:47:16.816746Z', 'created_at': '2024-02-01T11:44:51.978072Z', 'error': None, 'id': 'qlua7w3b5y2fcputi27al53qgy', 'input': {'image': 'https://replicate.delivery/pbxt/KKNB7w6pjN79j5pHDSyYXa5EwaQE9FL5fx6Qa83XMn1HYuKm/extreme_ironing.jpg', 'top_p': 1, 'prompt': 'What is unusual about this image?', 'max_tokens': 1024, 'temperature': 0.2}, 'logs': "The attention mask and the pad token id were not set. As a consequence, you may observe unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results.\nSetting `pad_token_id` to `eos_token_id`:2 for open-end generation.", 'metrics': {'predict_time': 4.445047, 'total_time': 144.838674}, 'output': ['The ', 'unusual ', 'aspect ', 'of ', 'this ', 'image ', 'is ', 'that ', 'a ', 'man ', 'is ', 'standing ', 'on ', 'the ', 'back ', 'of ', 'a ', 'yellow ', 'SUV, ', 'ironing ', 'clothes. ', 'This ', 'is ', 'not ', 'a ', 'typical ', 'scene, ', 'as ', 'one ', 'would ', 'expect ', 'to ', 'see ', 'the ', 'man ', 'either ', 'inside ', 'the ', 'vehicle ', 'or ', 'on ', 'the ', 'ground, ', 'rather ', 'than ', 'standing ', 'on ', 'the ', 'back ', 'of ', 'the ', 'SUV. ', 'The ', 'act ', 'of ', 'ironing ', 'clothes ', 'while ', 'standing ', 'on ', 'the ', 'back ', 'of ', 'a ', 'moving ', 'vehicle ', 'is ', 'both ', 'unusual ', 'and ', 'potentially ', 'dangerous. '], 'started_at': '2024-02-01T11:47:12.371699Z', 'status': 'succeeded', 'urls': {'stream': 'https://streaming-api.svc.us.c.replicate.net/v1/streams/523buztgaalgf6aipreduz2zsudl3edwknku3wftgaw4sdlbdtta', 'get': 'https://api.replicate.com/v1/predictions/qlua7w3b5y2fcputi27al53qgy', 'cancel': 'https://api.replicate.com/v1/predictions/qlua7w3b5y2fcputi27al53qgy/cancel'}, 'model': 'yorickvp/llava-v1.6-mistral-7b', 'version': '6d853ae87b782cd5f659578c807aa5cc03075e40b28fc3ff83e8aee98f9f94c7', 'webhook_completed': None}, 'description': 'LLaVA v1.6: Large Language and Vision Assistant (Mistral-7B)', 'github_url': 'https://github.com/haotian-liu/LLaVA', 'latest_version': {'id': '19be067b589d0c46689ffa7cc3ff321447a441986a7694c01225973c2eafc874', 'created_at': '2024-02-02T16:42:35.328982Z', 'cog_version': '0.9.2', 'openapi_schema': {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'required': ['prompt'], 'properties': {'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 0, 'description': 'Input image'}, 'top_p': {'type': 'number', 'title': 'Top P', 'default': 1, 'maximum': 1, 'minimum': 0, 'x-order': 2, 'description': 'When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'x-order': 1, 'description': 'Prompt to use for text generation'}, 'history': {'type': 'array', 'items': {'type': 'string'}, 'title': 'History', 'x-order': 5, 'description': 'List of earlier chat messages, alternating roles, starting with user input. Include <image> to specify which message to attach the image to.'}, 'max_tokens': {'type': 'integer', 'title': 'Max Tokens', 'default': 1024, 'minimum': 0, 'x-order': 4, 'description': 'Maximum number of tokens to generate. A word is generally 2-3 tokens'}, 'temperature': {'type': 'number', 'title': 'Temperature', 'default': 0.2, 'minimum': 0, 'x-order': 3, 'description': 'Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic'}}}, 'Output': {'type': 'array', 'items': {'type': 'string'}, 'title': 'Output', 'x-cog-array-type': 'iterator', 'x-cog-array-display': 'concatenate'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}}, 'license_url': 'https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2', 'name': 'llava-v1.6-mistral-7b', 'owner': 'yorickvp', 'paper_url': None, 'run_count': 147705, 'url': 'https://replicate.com/yorickvp/llava-v1.6-mistral-7b', 'visibility': 'public', 'hardware': 'Nvidia A40 (Large) GPU'}
