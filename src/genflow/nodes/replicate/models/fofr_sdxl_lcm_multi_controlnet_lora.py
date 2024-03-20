schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'properties': {'mask': {'type': 'string', 'title': 'Mask', 'format': 'uri', 'x-order': 3, 'description': 'Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted.'}, 'seed': {'type': 'integer', 'title': 'Seed', 'x-order': 11, 'description': 'Random seed. Leave blank to randomize the seed'}, 'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 2, 'description': 'Input image for img2img or inpaint mode'}, 'width': {'type': 'integer', 'title': 'Width', 'default': 768, 'x-order': 4, 'description': 'Width of output image'}, 'height': {'type': 'integer', 'title': 'Height', 'default': 768, 'x-order': 5, 'description': 'Height of output image'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'default': 'An astronaut riding a rainbow unicorn', 'x-order': 0, 'description': 'Input prompt'}, 'refine': {'allOf': [{'$ref': '#/components/schemas/refine'}], 'default': 'no_refiner', 'x-order': 12, 'description': 'Which refine style to use'}, 'lora_scale': {'type': 'number', 'title': 'Lora Scale', 'default': 0.6, 'maximum': 1, 'minimum': 0, 'x-order': 15, 'description': 'LoRA additive scale. Only applicable on trained models.'}, 'num_outputs': {'type': 'integer', 'title': 'Num Outputs', 'default': 1, 'maximum': 4, 'minimum': 1, 'x-order': 7, 'description': 'Number of images to output'}, 'controlnet_1': {'allOf': [{'$ref': '#/components/schemas/controlnet_1'}], 'default': 'none', 'x-order': 18, 'description': 'Controlnet'}, 'controlnet_2': {'allOf': [{'$ref': '#/components/schemas/controlnet_2'}], 'default': 'none', 'x-order': 23, 'description': 'Controlnet'}, 'controlnet_3': {'allOf': [{'$ref': '#/components/schemas/controlnet_3'}], 'default': 'none', 'x-order': 28, 'description': 'Controlnet'}, 'lora_weights': {'type': 'string', 'title': 'Lora Weights', 'x-order': 16, 'description': 'Replicate LoRA weights to use. Leave blank to use the default weights.'}, 'refine_steps': {'type': 'integer', 'title': 'Refine Steps', 'x-order': 13, 'description': 'For base_image_refiner, the number of steps to refine, defaults to num_inference_steps'}, 'guidance_scale': {'type': 'number', 'title': 'Guidance Scale', 'default': 1.1, 'maximum': 50, 'minimum': 0, 'x-order': 9, 'description': 'Scale for classifier-free guidance'}, 'apply_watermark': {'type': 'boolean', 'title': 'Apply Watermark', 'default': True, 'x-order': 14, 'description': 'Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking.'}, 'negative_prompt': {'type': 'string', 'title': 'Negative Prompt', 'default': '', 'x-order': 1, 'description': 'Negative Prompt'}, 'prompt_strength': {'type': 'number', 'title': 'Prompt Strength', 'default': 0.8, 'maximum': 1, 'minimum': 0, 'x-order': 10, 'description': 'Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image'}, 'sizing_strategy': {'allOf': [{'$ref': '#/components/schemas/sizing_strategy'}], 'default': 'width_height', 'x-order': 6, 'description': 'Decide how to resize images – use width/height, resize based on input image or control image'}, 'controlnet_1_end': {'type': 'number', 'title': 'Controlnet 1 End', 'default': 1, 'maximum': 1, 'minimum': 0, 'x-order': 22, 'description': 'When controlnet conditioning ends'}, 'controlnet_2_end': {'type': 'number', 'title': 'Controlnet 2 End', 'default': 1, 'maximum': 1, 'minimum': 0, 'x-order': 27, 'description': 'When controlnet conditioning ends'}, 'controlnet_3_end': {'type': 'number', 'title': 'Controlnet 3 End', 'default': 1, 'maximum': 1, 'minimum': 0, 'x-order': 32, 'description': 'When controlnet conditioning ends'}, 'controlnet_1_image': {'type': 'string', 'title': 'Controlnet 1 Image', 'format': 'uri', 'x-order': 19, 'description': 'Input image for first controlnet'}, 'controlnet_1_start': {'type': 'number', 'title': 'Controlnet 1 Start', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 21, 'description': 'When controlnet conditioning starts'}, 'controlnet_2_image': {'type': 'string', 'title': 'Controlnet 2 Image', 'format': 'uri', 'x-order': 24, 'description': 'Input image for second controlnet'}, 'controlnet_2_start': {'type': 'number', 'title': 'Controlnet 2 Start', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 26, 'description': 'When controlnet conditioning starts'}, 'controlnet_3_image': {'type': 'string', 'title': 'Controlnet 3 Image', 'format': 'uri', 'x-order': 29, 'description': 'Input image for third controlnet'}, 'controlnet_3_start': {'type': 'number', 'title': 'Controlnet 3 Start', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 31, 'description': 'When controlnet conditioning starts'}, 'num_inference_steps': {'type': 'integer', 'title': 'Num Inference Steps', 'default': 4, 'maximum': 30, 'minimum': 1, 'x-order': 8, 'description': 'Number of denoising steps'}, 'disable_safety_checker': {'type': 'boolean', 'title': 'Disable Safety Checker', 'default': False, 'x-order': 17, 'description': 'Disable safety checker for generated images. This feature is only available through the API. See [https://replicate.com/docs/how-does-replicate-work#safety](https://replicate.com/docs/how-does-replicate-work#safety)'}, 'controlnet_1_conditioning_scale': {'type': 'number', 'title': 'Controlnet 1 Conditioning Scale', 'default': 0.75, 'maximum': 4, 'minimum': 0, 'x-order': 20, 'description': 'How strong the controlnet conditioning is'}, 'controlnet_2_conditioning_scale': {'type': 'number', 'title': 'Controlnet 2 Conditioning Scale', 'default': 0.75, 'maximum': 4, 'minimum': 0, 'x-order': 25, 'description': 'How strong the controlnet conditioning is'}, 'controlnet_3_conditioning_scale': {'type': 'number', 'title': 'Controlnet 3 Conditioning Scale', 'default': 0.75, 'maximum': 4, 'minimum': 0, 'x-order': 30, 'description': 'How strong the controlnet conditioning is'}}}, 'Output': {'type': 'array', 'items': {'type': 'string', 'format': 'uri'}, 'title': 'Output'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'refine': {'enum': ['no_refiner', 'base_image_refiner'], 'type': 'string', 'title': 'refine', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'controlnet_1': {'enum': ['none', 'edge_canny', 'illusion', 'depth_leres', 'depth_midas', 'soft_edge_pidi', 'soft_edge_hed', 'lineart', 'lineart_anime', 'openpose'], 'type': 'string', 'title': 'controlnet_1', 'description': 'An enumeration.'}, 'controlnet_2': {'enum': ['none', 'edge_canny', 'illusion', 'depth_leres', 'depth_midas', 'soft_edge_pidi', 'soft_edge_hed', 'lineart', 'lineart_anime', 'openpose'], 'type': 'string', 'title': 'controlnet_2', 'description': 'An enumeration.'}, 'controlnet_3': {'enum': ['none', 'edge_canny', 'illusion', 'depth_leres', 'depth_midas', 'soft_edge_pidi', 'soft_edge_hed', 'lineart', 'lineart_anime', 'openpose'], 'type': 'string', 'title': 'controlnet_3', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'sizing_strategy': {'enum': ['width_height', 'input_image', 'controlnet_1_image', 'controlnet_2_image', 'controlnet_3_image', 'mask_image'], 'type': 'string', 'title': 'sizing_strategy', 'description': 'An enumeration.'}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'fofr/sdxl-lcm-multi-controlnet-lora'
model_version = '750b7665e4eb1c02f65f374317e3d8dfe690ee42f3101a9c686cfd6d533534b7'
