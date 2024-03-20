schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'properties': {'seed': {'type': 'integer', 'title': 'Seed', 'x-order': 8, 'description': 'Fix the random seed for reproducibility'}, 'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 0, 'description': 'An image of a person to be converted'}, 'style': {'allOf': [{'$ref': '#/components/schemas/style'}], 'default': '3D', 'x-order': 1, 'description': 'Style to convert to'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'default': 'a person', 'x-order': 2}, 'lora_scale': {'type': 'number', 'title': 'Lora Scale', 'default': 1, 'maximum': 1, 'minimum': 0, 'x-order': 10, 'description': 'How strong the LoRA will be'}, 'custom_lora_url': {'type': 'string', 'title': 'Custom Lora Url', 'x-order': 9, 'description': 'URL to a Replicate custom LoRA. Must be in the format https://replicate.delivery/pbxt/[id]/trained_model.tar or https://pbxt.replicate.delivery/[id]/trained_model.tar'}, 'negative_prompt': {'type': 'string', 'title': 'Negative Prompt', 'default': '', 'x-order': 3, 'description': 'Things you do not want in the image'}, 'prompt_strength': {'type': 'number', 'title': 'Prompt Strength', 'default': 4.5, 'maximum': 20, 'minimum': 0, 'x-order': 5, 'description': 'Strength of the prompt. This is the CFG scale, higher numbers lead to stronger prompt, lower numbers will keep more of a likeness to the original.'}, 'denoising_strength': {'type': 'number', 'title': 'Denoising Strength', 'default': 0.65, 'maximum': 1, 'minimum': 0, 'x-order': 4, 'description': 'How much of the original image to keep. 1 is the complete destruction of the original image, 0 is the original image'}, 'instant_id_strength': {'type': 'number', 'title': 'Instant Id Strength', 'default': 1, 'maximum': 1, 'minimum': 0, 'x-order': 7, 'description': 'How strong the InstantID will be.'}, 'control_depth_strength': {'type': 'number', 'title': 'Control Depth Strength', 'default': 0.8, 'maximum': 1, 'minimum': 0, 'x-order': 6, 'description': 'Strength of depth controlnet. The bigger this is, the more controlnet affects the output.'}}}, 'style': {'enum': ['3D', 'Emoji', 'Video game', 'Pixels', 'Clay', 'Toy'], 'type': 'string', 'title': 'style', 'description': 'An enumeration.'}, 'Output': {'type': 'array', 'items': {'type': 'string', 'format': 'uri'}, 'title': 'Output'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'fofr/face-to-many'
model_version = '35cea9c3164d9fb7fbd48b51503eabdb39c9d04fdaef9a68f368bed8087ec5f9'
