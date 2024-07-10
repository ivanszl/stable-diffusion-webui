import os
import gradio
import gradio.blocks
import gradio.routes
import ujson
import hashlib
import shutil

old_get_api_info = gradio.blocks.get_api_info

def hijack_api_info(config: dict, serialize: bool = True):
  data = ujson.dumps(config).encode('utf-8')
  md5_hash = hashlib.md5(data).hexdigest()
  file_path = f'./__cache__/{md5_hash}_{serialize}_api_info.json'
  if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
      json_data = file.read()
      return ujson.loads(json_data)
  
  json_data = old_get_api_info(config, serialize)
  with open(file_path, 'w', encoding='utf-8') as file:
    ujson.dump(json_data, file)
  return json_data

def hijack_get_api_info():
  gradio.blocks.get_api_info = hijack_api_info

def build_api_info(app: gradio.routes.App):
  config = app.get_blocks().config
  data = ujson.dumps(config).encode('utf-8')
  md5_hash = hashlib.md5(data).hexdigest()
  shutil.rmtree('./__cache__')
  os.makedirs("./__cache__", mode=644, exist_ok=True)
  file_path = f'./__cache__/{md5_hash}_True_api_info.json'
  if not os.path.exists(file_path):
    json_data = old_get_api_info(config)
    with open(file_path, 'w', encoding='utf-8') as file:
      ujson.dump(json_data, file)
  