schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'properties': {'mask': {'type': 'string', 'title': 'Mask', 'format': 'uri', 'x-order': 3, 'description': 'Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted.'}, 'seed': {'type': 'integer', 'title': 'Seed', 'x-order': 11, 'description': 'Random seed. Leave blank to randomize the seed'}, 'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 2, 'description': 'Input image for img2img or inpaint mode'}, 'width': {'type': 'integer', 'title': 'Width', 'default': 1024, 'x-order': 4, 'description': 'Width of output image. Recommended 1024 or 1280'}, 'height': {'type': 'integer', 'title': 'Height', 'default': 1024, 'x-order': 5, 'description': 'Height of output image. Recommended 1024 or 1280'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'default': 'black fluffy gorgeous dangerous cat animal creature, large orange eyes, big fluffy ears, piercing gaze, full moon, dark ambiance, best quality, extremely detailed', 'x-order': 0, 'description': 'Input prompt'}, 'scheduler': {'allOf': [{'$ref': '#/components/schemas/scheduler'}], 'default': 'DPM++2MSDE', 'x-order': 7, 'description': 'scheduler'}, 'num_outputs': {'type': 'integer', 'title': 'Num Outputs', 'default': 1, 'maximum': 4, 'minimum': 1, 'x-order': 6, 'description': 'Number of images to output.'}, 'guidance_scale': {'type': 'number', 'title': 'Guidance Scale', 'default': 7.5, 'maximum': 50, 'minimum': 1, 'x-order': 9, 'description': 'Scale for classifier-free guidance. Recommended 4-6'}, 'apply_watermark': {'type': 'boolean', 'title': 'Apply Watermark', 'default': True, 'x-order': 12, 'description': 'Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking.'}, 'negative_prompt': {'type': 'string', 'title': 'Negative Prompt', 'default': 'nsfw, bad quality, bad anatomy, worst quality, low quality, low resolutions, extra fingers, blur, blurry, ugly, wrongs proportions, watermark, image artifacts, lowres, ugly, jpeg artifacts, deformed, noisy image', 'x-order': 1, 'description': 'Negative Input prompt'}, 'prompt_strength': {'type': 'number', 'title': 'Prompt Strength', 'default': 0.8, 'maximum': 1, 'minimum': 0, 'x-order': 10, 'description': 'Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image'}, 'num_inference_steps': {'type': 'integer', 'title': 'Num Inference Steps', 'default': 20, 'maximum': 100, 'minimum': 1, 'x-order': 8, 'description': 'Number of denoising steps. 20 to 60 steps for more detail, 20 steps for faster results.'}, 'disable_safety_checker': {'type': 'boolean', 'title': 'Disable Safety Checker', 'default': False, 'x-order': 13, 'description': 'Disable safety checker for generated images. This feature is only available through the API. See https://replicate.com/docs/how-does-replicate-work#safety'}}}, 'Output': {'type': 'array', 'items': {'type': 'string', 'format': 'uri'}, 'title': 'Output'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'scheduler': {'enum': ['DDIM', 'DPMSolverMultistep', 'HeunDiscrete', 'KarrasDPM', 'K_EULER_ANCESTRAL', 'K_EULER', 'PNDM', 'DPM++2MSDE'], 'type': 'string', 'title': 'scheduler', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'lucataco/proteus-v0.4'
model_version = '34a427535a3c45552b94369280b823fcd0e5c9710e97af020bf445c033d4569e'
model_info = {'cover_image_url': 'https://replicate.delivery/pbxt/3WJYR5U1mhJCHhWQKCKnr2ZifNcIeaAIBrZrZqijemJtZS1kA/out-0.png', 'created_at': '2024-02-26T19:01:05.593762Z', 'default_example': {'completed_at': '2024-02-26T19:06:31.668926Z', 'created_at': '2024-02-26T19:06:21.151363Z', 'error': None, 'id': 'rgulir3bekj5fwkiiauzxqwnim', 'input': {'width': 1024, 'height': 1024, 'prompt': '3 fish in a fish tank wearing adorable outfits, best quality, hd', 'scheduler': 'DPM++2MSDE', 'num_outputs': 1, 'guidance_scale': 7.5, 'apply_watermark': True, 'negative_prompt': 'nsfw, bad quality, bad anatomy, worst quality, low quality, low resolutions, extra fingers, blur, blurry, ugly, wrongs proportions, watermark, image artifacts, lowres, ugly, jpeg artifacts, deformed, noisy image', 'prompt_strength': 0.8, 'num_inference_steps': 20}, 'logs': 'Using seed: 1471417868\nPrompt: 3 fish in a fish tank wearing adorable outfits, best quality, hd\ntxt2img mode\n  0%|          | 0/20 [00:00<?, ?it/s]\n  5%|▌         | 1/20 [00:00<00:07,  2.46it/s]\n 10%|█         | 2/20 [00:00<00:07,  2.45it/s]\n 15%|█▌        | 3/20 [00:01<00:06,  2.44it/s]\n 20%|██        | 4/20 [00:01<00:06,  2.45it/s]\n 25%|██▌       | 5/20 [00:02<00:06,  2.45it/s]\n 30%|███       | 6/20 [00:02<00:05,  2.45it/s]\n 35%|███▌      | 7/20 [00:02<00:05,  2.45it/s]\n 40%|████      | 8/20 [00:03<00:04,  2.45it/s]\n 45%|████▌     | 9/20 [00:03<00:04,  2.45it/s]\n 50%|█████     | 10/20 [00:04<00:04,  2.45it/s]\n 55%|█████▌    | 11/20 [00:04<00:03,  2.45it/s]\n 60%|██████    | 12/20 [00:04<00:03,  2.45it/s]\n 65%|██████▌   | 13/20 [00:05<00:02,  2.44it/s]\n 70%|███████   | 14/20 [00:05<00:02,  2.44it/s]\n 75%|███████▌  | 15/20 [00:06<00:02,  2.44it/s]\n 80%|████████  | 16/20 [00:06<00:01,  2.44it/s]\n 85%|████████▌ | 17/20 [00:06<00:01,  2.44it/s]\n 90%|█████████ | 18/20 [00:07<00:00,  2.44it/s]\n 95%|█████████▌| 19/20 [00:07<00:00,  2.44it/s]\n100%|██████████| 20/20 [00:07<00:00,  2.87it/s]\n100%|██████████| 20/20 [00:07<00:00,  2.51it/s]', 'metrics': {'predict_time': 10.468228, 'total_time': 10.517563}, 'output': ['https://replicate.delivery/pbxt/3WJYR5U1mhJCHhWQKCKnr2ZifNcIeaAIBrZrZqijemJtZS1kA/out-0.png'], 'started_at': '2024-02-26T19:06:21.200698Z', 'status': 'succeeded', 'urls': {'get': 'https://api.replicate.com/v1/predictions/rgulir3bekj5fwkiiauzxqwnim', 'cancel': 'https://api.replicate.com/v1/predictions/rgulir3bekj5fwkiiauzxqwnim/cancel'}, 'model': 'lucataco/proteus-v0.4', 'version': '34a427535a3c45552b94369280b823fcd0e5c9710e97af020bf445c033d4569e', 'webhook_completed': None}, 'description': 'ProteusV0.4: The Style Update', 'github_url': 'https://github.com/lucataco/cog-proteus-v0.4', 'latest_version': {'id': '34a427535a3c45552b94369280b823fcd0e5c9710e97af020bf445c033d4569e', 'created_at': '2024-02-26T19:03:19.515256Z', 'cog_version': '0.9.3', 'openapi_schema': {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'properties': {'mask': {'type': 'string', 'title': 'Mask', 'format': 'uri', 'x-order': 3, 'description': 'Input mask for inpaint mode. Black areas will be preserved, white areas will be inpainted.'}, 'seed': {'type': 'integer', 'title': 'Seed', 'x-order': 11, 'description': 'Random seed. Leave blank to randomize the seed'}, 'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 2, 'description': 'Input image for img2img or inpaint mode'}, 'width': {'type': 'integer', 'title': 'Width', 'default': 1024, 'x-order': 4, 'description': 'Width of output image. Recommended 1024 or 1280'}, 'height': {'type': 'integer', 'title': 'Height', 'default': 1024, 'x-order': 5, 'description': 'Height of output image. Recommended 1024 or 1280'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'default': 'black fluffy gorgeous dangerous cat animal creature, large orange eyes, big fluffy ears, piercing gaze, full moon, dark ambiance, best quality, extremely detailed', 'x-order': 0, 'description': 'Input prompt'}, 'scheduler': {'allOf': [{'$ref': '#/components/schemas/scheduler'}], 'default': 'DPM++2MSDE', 'x-order': 7, 'description': 'scheduler'}, 'num_outputs': {'type': 'integer', 'title': 'Num Outputs', 'default': 1, 'maximum': 4, 'minimum': 1, 'x-order': 6, 'description': 'Number of images to output.'}, 'guidance_scale': {'type': 'number', 'title': 'Guidance Scale', 'default': 7.5, 'maximum': 50, 'minimum': 1, 'x-order': 9, 'description': 'Scale for classifier-free guidance. Recommended 4-6'}, 'apply_watermark': {'type': 'boolean', 'title': 'Apply Watermark', 'default': True, 'x-order': 12, 'description': 'Applies a watermark to enable determining if an image is generated in downstream applications. If you have other provisions for generating or deploying images safely, you can use this to disable watermarking.'}, 'negative_prompt': {'type': 'string', 'title': 'Negative Prompt', 'default': 'nsfw, bad quality, bad anatomy, worst quality, low quality, low resolutions, extra fingers, blur, blurry, ugly, wrongs proportions, watermark, image artifacts, lowres, ugly, jpeg artifacts, deformed, noisy image', 'x-order': 1, 'description': 'Negative Input prompt'}, 'prompt_strength': {'type': 'number', 'title': 'Prompt Strength', 'default': 0.8, 'maximum': 1, 'minimum': 0, 'x-order': 10, 'description': 'Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image'}, 'num_inference_steps': {'type': 'integer', 'title': 'Num Inference Steps', 'default': 20, 'maximum': 100, 'minimum': 1, 'x-order': 8, 'description': 'Number of denoising steps. 20 to 60 steps for more detail, 20 steps for faster results.'}, 'disable_safety_checker': {'type': 'boolean', 'title': 'Disable Safety Checker', 'default': False, 'x-order': 13, 'description': 'Disable safety checker for generated images. This feature is only available through the API. See https://replicate.com/docs/how-does-replicate-work#safety'}}}, 'Output': {'type': 'array', 'items': {'type': 'string', 'format': 'uri'}, 'title': 'Output'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'scheduler': {'enum': ['DDIM', 'DPMSolverMultistep', 'HeunDiscrete', 'KarrasDPM', 'K_EULER_ANCESTRAL', 'K_EULER', 'PNDM', 'DPM++2MSDE'], 'type': 'string', 'title': 'scheduler', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}}, 'license_url': 'https://huggingface.co/models?license=license%3Agpl-3.0', 'name': 'proteus-v0.4', 'owner': 'lucataco', 'paper_url': None, 'run_count': 12918, 'url': 'https://replicate.com/lucataco/proteus-v0.4', 'visibility': 'public', 'hardware': 'Nvidia A40 (Large) GPU'}
