#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('FlagAlpha/Llama3-Chinese-8B-Instruct', local_dir='./Llama3-Chinese-8B-Instruct')
