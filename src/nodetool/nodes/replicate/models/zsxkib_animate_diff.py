schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'properties': {'seed': {'type': 'integer', 'title': 'Seed', 'default': -1, 'x-order': 8, 'description': 'Seed for different images and reproducibility. Use -1 to randomise seed'}, 'steps': {'type': 'integer', 'title': 'Steps', 'default': 25, 'maximum': 100, 'minimum': 1, 'x-order': 3, 'description': 'Number of inference steps'}, 'width': {'type': 'integer', 'title': 'Width', 'default': 512, 'x-order': 6, 'description': 'Width in pixels'}, 'frames': {'type': 'integer', 'title': 'Frames', 'default': 16, 'maximum': 32, 'minimum': 1, 'x-order': 5, 'description': 'Length of the video in frames (playback is at 8 fps e.g. 16 frames @ 8 fps is 2 seconds)'}, 'height': {'type': 'integer', 'title': 'Height', 'default': 512, 'x-order': 7, 'description': 'Height in pixels'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'default': 'photo of vocano, rocks, storm weather, wind, lava waves, lightning, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3', 'x-order': 0}, 'base_model': {'allOf': [{'$ref': '#/components/schemas/base_model'}], 'default': 'realisticVisionV20_v20', 'x-order': 2, 'description': 'Select a base model (DreamBooth checkpoint)'}, 'output_format': {'allOf': [{'$ref': '#/components/schemas/output_format'}], 'default': 'mp4', 'x-order': 17, 'description': "Output format of the video. Can be 'mp4' or 'gif'"}, 'guidance_scale': {'type': 'number', 'title': 'Guidance Scale', 'default': 7.5, 'maximum': 20, 'minimum': 0, 'x-order': 4, 'description': 'Guidance Scale. How closely do we want to adhere to the prompt and its contents'}, 'negative_prompt': {'type': 'string', 'title': 'Negative Prompt', 'default': 'blur, haze, deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers, deformed, distorted, disfigured, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation', 'x-order': 1}, 'pan_up_motion_strength': {'type': 'number', 'title': 'Pan Up Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 13, 'description': 'Strength of Pan Up Motion LoRA. 0 disables the LoRA'}, 'zoom_in_motion_strength': {'type': 'number', 'title': 'Zoom In Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 9, 'description': 'Strength of Zoom In Motion LoRA. 0 disables the LoRA'}, 'pan_down_motion_strength': {'type': 'number', 'title': 'Pan Down Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 14, 'description': 'Strength of Pan Down Motion LoRA. 0 disables the LoRA'}, 'pan_left_motion_strength': {'type': 'number', 'title': 'Pan Left Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 11, 'description': 'Strength of Pan Left Motion LoRA. 0 disables the LoRA'}, 'zoom_out_motion_strength': {'type': 'number', 'title': 'Zoom Out Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 10, 'description': 'Strength of Zoom Out Motion LoRA. 0 disables the LoRA'}, 'pan_right_motion_strength': {'type': 'number', 'title': 'Pan Right Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 12, 'description': 'Strength of Pan Right Motion LoRA. 0 disables the LoRA'}, 'rolling_clockwise_motion_strength': {'type': 'number', 'title': 'Rolling Clockwise Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 15, 'description': 'Strength of Rolling Clockwise Motion LoRA. 0 disables the LoRA'}, 'rolling_anticlockwise_motion_strength': {'type': 'number', 'title': 'Rolling Anticlockwise Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 16, 'description': 'Strength of Rolling Anticlockwise Motion LoRA. 0 disables the LoRA'}}}, 'Output': {'type': 'array', 'items': {'type': 'string', 'format': 'uri'}, 'title': 'Output'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'base_model': {'enum': ['realisticVisionV20_v20', 'lyriel_v16', 'majicmixRealistic_v5Preview', 'rcnzCartoon3d_v10', 'toonyou_beta3'], 'type': 'string', 'title': 'base_model', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'output_format': {'enum': ['mp4', 'gif'], 'type': 'string', 'title': 'output_format', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'zsxkib/animate-diff'
model_version = '269a616c8b0c2bbc12fc15fd51bb202b11e94ff0f7786c026aa905305c4ed9fb'
model_info = {'cover_image_url': 'https://tjzk.replicate.delivery/models_models_cover_image/336d5c4e-4fd1-415a-a3f7-4a40fa5bdf2b/a_middle-aged_woman_utilizing__zo.gif', 'created_at': '2023-09-26T19:55:56.734880Z', 'default_example': {'completed_at': '2023-10-03T15:49:45.880669Z', 'created_at': '2023-10-03T15:47:58.527484Z', 'error': None, 'id': 'ficctqlbvnqq6w3eqvc3gep5si', 'input': {'seed': -1, 'steps': 25, 'width': 768, 'frames': 16, 'height': 512, 'prompt': 'a medium shot of a vibrant coral reef with a variety of marine life, rainbow, visual effects, prores, cineon, royal, monumental, hyperrealistic, exceptional, visually stunning', 'base_model': 'realisticVisionV20_v20', 'guidance_scale': 7.5, 'negative_prompt': '', 'pan_up_motion_strength': 0, 'zoom_in_motion_strength': 0, 'pan_down_motion_strength': 0, 'pan_left_motion_strength': 0, 'zoom_out_motion_strength': 0, 'pan_right_motion_strength': 0.75, 'rolling_clockwise_motion_strength': 0, 'rolling_anticlockwise_motion_strength': 0}, 'logs': '--------------------------------------------------------------------------------\nCog:\ninference_config: "configs/inference/inference-v2.yaml"\nmotion_module:\n- "models/Motion_Module/mm_sd_v15_v2.ckpt"\nmotion_module_lora_configs:\n- path:  "models/MotionLoRA/v2_lora_PanRight.ckpt"\nalpha: 0.75\ndreambooth_path: "models/DreamBooth_LoRA/realisticVisionV20_v20.safetensors"\nlora_model_path: ""\nseed:           -1\nsteps:          25\nguidance_scale: 7.5\nprompt:\n- "a medium shot of a vibrant coral reef with a variety of marine life, rainbow, visual effects, prores, cineon, royal, monumental, hyperrealistic, exceptional, visually stunning"\nn_prompt:\n- ""\n--------------------------------------------------------------------------------\ncurrent seed: 14398808075592566791\nsampling a medium shot of a vibrant coral reef with a variety of marine life, rainbow, visual effects, prores, cineon, royal, monumental, hyperrealistic, exceptional, visually stunning ...\n  0%|          | 0/25 [00:00<?, ?it/s]\n  4%|▍         | 1/25 [00:04<01:38,  4.11s/it]\n  8%|▊         | 2/25 [00:08<01:34,  4.12s/it]\n 12%|█▏        | 3/25 [00:12<01:30,  4.12s/it]\n 16%|█▌        | 4/25 [00:16<01:26,  4.12s/it]\n 20%|██        | 5/25 [00:20<01:22,  4.12s/it]\n 24%|██▍       | 6/25 [00:24<01:18,  4.12s/it]\n 28%|██▊       | 7/25 [00:28<01:14,  4.12s/it]\n 32%|███▏      | 8/25 [00:32<01:10,  4.12s/it]\n 36%|███▌      | 9/25 [00:37<01:05,  4.12s/it]\n 40%|████      | 10/25 [00:41<01:01,  4.12s/it]\n 44%|████▍     | 11/25 [00:45<00:57,  4.13s/it]\n 48%|████▊     | 12/25 [00:49<00:53,  4.13s/it]\n 52%|█████▏    | 13/25 [00:53<00:49,  4.13s/it]\n 56%|█████▌    | 14/25 [00:57<00:45,  4.13s/it]\n 60%|██████    | 15/25 [01:01<00:41,  4.13s/it]\n 64%|██████▍   | 16/25 [01:06<00:37,  4.14s/it]\n 68%|██████▊   | 17/25 [01:10<00:33,  4.14s/it]\n 72%|███████▏  | 18/25 [01:14<00:28,  4.14s/it]\n 76%|███████▌  | 19/25 [01:18<00:24,  4.14s/it]\n 80%|████████  | 20/25 [01:22<00:20,  4.14s/it]\n 84%|████████▍ | 21/25 [01:26<00:16,  4.14s/it]\n 88%|████████▊ | 22/25 [01:30<00:12,  4.14s/it]\n 92%|█████████▏| 23/25 [01:35<00:08,  4.14s/it]\n 96%|█████████▌| 24/25 [01:39<00:04,  4.14s/it]\n100%|██████████| 25/25 [01:43<00:00,  4.14s/it]\n100%|██████████| 25/25 [01:43<00:00,  4.13s/it]\n  0%|          | 0/16 [00:00<?, ?it/s]\n 31%|███▏      | 5/16 [00:00<00:00, 26.35it/s]\n 50%|█████     | 8/16 [00:00<00:00, 12.33it/s]\n 62%|██████▎   | 10/16 [00:00<00:00, 10.37it/s]\n 75%|███████▌  | 12/16 [00:01<00:00,  9.33it/s]\n 88%|████████▊ | 14/16 [00:01<00:00,  8.72it/s]\n 94%|█████████▍| 15/16 [00:01<00:00,  8.47it/s]\n100%|██████████| 16/16 [00:01<00:00,  8.21it/s]\n100%|██████████| 16/16 [00:01<00:00,  9.73it/s]\nsave to samples/99a6f7b49d305094d1391b37d153ab22-2023-10-03T15-47-58/sample/amediumshotofa.mp4', 'metrics': {'predict_time': 107.357321, 'total_time': 107.353185}, 'output': ['https://pbxt.replicate.delivery/tWckdpnVflzJZyOesJqVdnueqxEyvcPi30BygYDtI3KwQ9UjA/0-amediumshotofa.mp4'], 'started_at': '2023-10-03T15:47:58.523348Z', 'status': 'succeeded', 'urls': {'get': 'https://api.replicate.com/v1/predictions/ficctqlbvnqq6w3eqvc3gep5si', 'cancel': 'https://api.replicate.com/v1/predictions/ficctqlbvnqq6w3eqvc3gep5si/cancel'}, 'model': 'zsxkib/animate-diff', 'version': '5feed37289b3e23f46e103b778b7acd64e69ecac1d89347e131c642fbfd3eaef', 'webhook_completed': None}, 'description': '🎨 AnimateDiff (w/ MotionLoRAs for Panning, Zooming, etc): Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning', 'github_url': 'https://github.com/guoyww/AnimateDiff', 'latest_version': {'id': '269a616c8b0c2bbc12fc15fd51bb202b11e94ff0f7786c026aa905305c4ed9fb', 'created_at': '2023-10-05T22:23:31.341354Z', 'cog_version': '0.8.6', 'openapi_schema': {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'properties': {'seed': {'type': 'integer', 'title': 'Seed', 'default': -1, 'x-order': 8, 'description': 'Seed for different images and reproducibility. Use -1 to randomise seed'}, 'steps': {'type': 'integer', 'title': 'Steps', 'default': 25, 'maximum': 100, 'minimum': 1, 'x-order': 3, 'description': 'Number of inference steps'}, 'width': {'type': 'integer', 'title': 'Width', 'default': 512, 'x-order': 6, 'description': 'Width in pixels'}, 'frames': {'type': 'integer', 'title': 'Frames', 'default': 16, 'maximum': 32, 'minimum': 1, 'x-order': 5, 'description': 'Length of the video in frames (playback is at 8 fps e.g. 16 frames @ 8 fps is 2 seconds)'}, 'height': {'type': 'integer', 'title': 'Height', 'default': 512, 'x-order': 7, 'description': 'Height in pixels'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'default': 'photo of vocano, rocks, storm weather, wind, lava waves, lightning, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3', 'x-order': 0}, 'base_model': {'allOf': [{'$ref': '#/components/schemas/base_model'}], 'default': 'realisticVisionV20_v20', 'x-order': 2, 'description': 'Select a base model (DreamBooth checkpoint)'}, 'output_format': {'allOf': [{'$ref': '#/components/schemas/output_format'}], 'default': 'mp4', 'x-order': 17, 'description': "Output format of the video. Can be 'mp4' or 'gif'"}, 'guidance_scale': {'type': 'number', 'title': 'Guidance Scale', 'default': 7.5, 'maximum': 20, 'minimum': 0, 'x-order': 4, 'description': 'Guidance Scale. How closely do we want to adhere to the prompt and its contents'}, 'negative_prompt': {'type': 'string', 'title': 'Negative Prompt', 'default': 'blur, haze, deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers, deformed, distorted, disfigured, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation', 'x-order': 1}, 'pan_up_motion_strength': {'type': 'number', 'title': 'Pan Up Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 13, 'description': 'Strength of Pan Up Motion LoRA. 0 disables the LoRA'}, 'zoom_in_motion_strength': {'type': 'number', 'title': 'Zoom In Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 9, 'description': 'Strength of Zoom In Motion LoRA. 0 disables the LoRA'}, 'pan_down_motion_strength': {'type': 'number', 'title': 'Pan Down Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 14, 'description': 'Strength of Pan Down Motion LoRA. 0 disables the LoRA'}, 'pan_left_motion_strength': {'type': 'number', 'title': 'Pan Left Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 11, 'description': 'Strength of Pan Left Motion LoRA. 0 disables the LoRA'}, 'zoom_out_motion_strength': {'type': 'number', 'title': 'Zoom Out Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 10, 'description': 'Strength of Zoom Out Motion LoRA. 0 disables the LoRA'}, 'pan_right_motion_strength': {'type': 'number', 'title': 'Pan Right Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 12, 'description': 'Strength of Pan Right Motion LoRA. 0 disables the LoRA'}, 'rolling_clockwise_motion_strength': {'type': 'number', 'title': 'Rolling Clockwise Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 15, 'description': 'Strength of Rolling Clockwise Motion LoRA. 0 disables the LoRA'}, 'rolling_anticlockwise_motion_strength': {'type': 'number', 'title': 'Rolling Anticlockwise Motion Strength', 'default': 0, 'maximum': 1, 'minimum': 0, 'x-order': 16, 'description': 'Strength of Rolling Anticlockwise Motion LoRA. 0 disables the LoRA'}}}, 'Output': {'type': 'array', 'items': {'type': 'string', 'format': 'uri'}, 'title': 'Output'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'base_model': {'enum': ['realisticVisionV20_v20', 'lyriel_v16', 'majicmixRealistic_v5Preview', 'rcnzCartoon3d_v10', 'toonyou_beta3'], 'type': 'string', 'title': 'base_model', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'output_format': {'enum': ['mp4', 'gif'], 'type': 'string', 'title': 'output_format', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}}, 'license_url': 'https://github.com/guoyww/AnimateDiff/blob/main/LICENSE.txt', 'name': 'animate-diff', 'owner': 'zsxkib', 'paper_url': 'https://arxiv.org/abs/2307.04725', 'run_count': 31300, 'url': 'https://replicate.com/zsxkib/animate-diff', 'visibility': 'public', 'hardware': 'Nvidia A40 GPU'}
