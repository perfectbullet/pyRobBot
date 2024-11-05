# pyRobBot



PyRobBot 是一个 Python 包，它使用 OpenAI 的 GPT 大型语言模型 (LLM) 来实现完全可配置的个人助理，除了传统的聊天机器人界面之外，它还可以使用 AI 生成的类似人类的声音与您交谈和聆听您。



## 特点

功能包括但不限于：

1. 语音聊天

   连续语音输入和输出 

   无需按按钮：助手将继续聆听，直到您停止说话

2. 互联网访问：助手将搜索网络以查找训练数据中没有的答案

3. 网络浏览器用户界面

   1. 语音聊天：


​	熟悉的文本界面与语音聊天集成

​	动态添加/删除对话

1. 通过终端聊天

​	

5. 完全可配置
   1. 支持大量语言 (*e.g.*, `rob --lang pt-br`)
   2.  通过 OpenAI API 支持多 LLM
   3. 

## 系统要求

- Python >= 3.9

- A valid 

  OpenAI API key

  - Set it in the Web UI or through the environment variable `OPENAI_API_KEY`

- 要启用语音聊天，您还需要:

  - PortAudio
    - Install on Ubuntu with `sudo apt-get --assume-yes install portaudio19-dev python-all-dev`
    - Install on CentOS/RHEL with `sudo yum install portaudio portaudio-devel`
  - ffmpeg
    - Install on Ubuntu with `sudo apt-get --assume-yes install `
    - Install on CentOS/RHEL with `sudo yum install ffmpeg`



## gx ollama 地址

ollama 外部访问

1、首先停止ollama服务：`systemctl stop ollama`
2、修改ollama的service文件：`/etc/systemd/system/ollama.service`
在[Service]下边增加一行：`Environment="OLLAMA_HOST=0.0.0.0:8080"`，端口根据实际情况修改
3、重载daemon文件 `systemctl daemon-reload`
4、启动ollama服务 `systemctl start ollama`

**代码中所有的api key 全部是ollama**

```
api_key = 'ollama'
```


http://125.69.16.175:11434/

```python

from openai import OpenAI

client = OpenAI(
    base_url = 'http://125.69.16.175:11434/v1',
    api_key='ollama', # required, but unused
)

response = client.chat.completions.create(
  model="qwen:32b",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The LA Dodgers won in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)
print(response.choices[0].message.content)
```



## docker run ollama

```sh
docker run -d --gpus=all -v /media/zj/data2-ext4/ollama:/root/.ollama -v /home/zj/LLaMA-Factory/models:/root/models -p 11434:11434 --name ollama ollama/ollama
# Run model locally
docker exec -it ollama ollama run llama3

docker exec -it ollama ollama list
```

![image-20240914225723458](/home/zj/.config/Typora/typora-user-images/image-20240914225723458.png)



## ollama model descriptions

#### Llama3-Chinese-8B-Instruct

Llama3-Chinese-8B-Instruct基于Llama3-8B中文微调对话模型

```sh
docker exec -it ollama ollama run llamafamily/llama3-chinese-8b-instruct
```

Example using curl:

```
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llamafamily/llama3-chinese-8b-instruct",
  "prompt":"介绍一下机器学习?"
 }'
```

#### Llama中文社区

https://github.com/LlamaFamily/Llama-Chinese



## whisper-asr-webservice 启动

```shell
cd /home/zj/openai_whisper/whisper-asr-webservice
docker compose up -d
```



## EmotiVoice 启动

```bash
cd /media/zj/data2-ext4/EmotiVoice_work/EmotiVoice
docker compose up -d
docker exec -it emoti-voice-v2 bash
root@c9443d7e2aa7:~# cd EmotiVoice/
root@c9443d7e2aa7:~/EmotiVoice# python3 openaiapi.py 
```

## import  Llama3-8B-Chinese-Chat  

```shell
# convert to gguf
cd /data/zh_work/llama.cpp-master
python3 convert_hf_to_gguf.py /data/llama_index_work/LLaMA-Factory/models/Llama3-8B-Chinese-Chat-bak20240914

# add Modelfile
(llama_cpp) ubuntu@ubuntu-desktop-2204:/data/llama_index_work/LLaMA-Factory/models/Llama3-8B-Chinese-Chat-bak20240914$ cat Modelfile 
FROM ./ggml-model-f16.gguf
(llama_cpp) ubuntu@ubuntu-desktop-2204:/data/llama_index_work/LLaMA-Factory/models/Llama3-8B-Chinese-Chat-bak20240914$ 

# import to ollama
(llama_cpp) ubuntu@ubuntu-desktop-2204:/data/llama_index_work/LLaMA-Factory/models/Llama3-8B-Chinese-Chat-bak20240914$ ollama create Llama3-8B-Chinese-Chat -f ./Modelfile
......
using existing layer sha256:af19aaee85bbd4b9fac8dcf6cc5b0c92872e876836a5431c74b368795d84b638 
creating new layer sha256:76c4d40c7affa9f1b7bd28dca8022c555bc469ba189e866afb726de6c529408f 
writing manifest 
success 

# check resutl
ollama run Llama3-8B-Chinese-Chat:latest
```

## 问题和bug

![image-20240923162803301](/home/zj/.config/Typora/typora-user-images/image-20240923162803301.png)

## 问题 ： conda环境下 streamlit: command not found

(pyrobot2) ubuntu@ubuntu-desktop-2204:/data/zj_work/pyRobBot$ streamlit
streamlit: command not found
(pyrobot2) ubuntu@ubuntu-desktop-2204:/data/zj_work/pyRobBot$ 


解决方法
1. 在虚拟环境的bin目录下，新增streamlit
(pyrobot2) ubuntu@ubuntu-desktop-2204:~/miniconda3/envs/pyrobot2/bin$ vim streamlit
2. 写入内容

```python
#!/home/ubuntu/miniconda3/envs/pyrobot2/bin/python3.10

# -*- coding: utf-8 -*-

import re
import sys
from streamlit.web.cli import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```

3. 修改可执行权限
(pyrobot2) ubuntu@ubuntu-desktop-2204:~/miniconda3/envs/pyrobot2/bin$ chmod +x streamlit 

4. 测试命令
(pyrobot2) ubuntu@ubuntu-desktop-2204:~/miniconda3/envs/pyrobot2/bin$ streamlit
Usage: streamlit [OPTIONS] COMMAND [ARGS]..................



# 模型微调的技术细节



## 灾难遗忘问题

​	大模型的灾难遗忘是指在连续学习多个任务的过程中，学习新知识会导致模型忘记或破坏之前学习到的旧知识，从而使模型在旧任务上的性能急剧下降。这是一个机器学习领域的重要挑战，尤其是对于大规模语言模型和多模态大语言模型，它们需要在不同的数据集和领域上进行微调或适应。

​	为了缓解灾难遗忘问题，我们可以使用其他数据来增强模型的泛化能力。例如，可以使用一个包含逻辑推理和问答类的数据集，用于和广告数据集一起进行微调。

比如我们构建的新数据集，它包含了一些逻辑推理和问答类的数据。您需要将这个文件转换成模型可以接受的输入格式。

新的数据集涵盖了数学应用题、选择题、填空题等多种不同类型的数据，比之前的广告数据集ADGEN更加丰富和多样。我们可以将这两个数据集合并在一起，对模型进行重新微调，以提高模型的泛化能力和稳定性。





# 模型导入导出

## LLaMa-Factory模型导出

**注意这里最大分块不要太大**

![sunlogin_20240918102932_0](/home/zj/Documents/sunlogin_20240918102932_0.bmp)



## 模型格式转换

1. 激活llama-cpp的虚拟环境：

   ```bash
   conda activate llama_cpp
   ```

2. change your dir

   ```bash
   cd /data/zh_work/llama.cpp-master/
   ```

3. 将经过微调并且合并后的saftensor格式的模型转换为gguf格式：

   ```bash
   python3 convert_hf_to_gguf.py /path_to_you_origin_model_path
   # examples 
   python3 convert_hf_to_gguf.py /data/llama_index_work/LLaMA-Factory/models/LLama3-8B-Chinese-Chat-medical
   ```

   ![image-20240918110618968](/home/zj/.config/Typora/typora-user-images/image-20240918110618968.png)

4. 转化后的模型在原来模型目录下后缀是gguf

## Ollama 导入 GGUF 模型文件

创建一个文件名为`Modelfile`的文件，该文件的内容如下

![image-20240918113548484](/home/zj/.config/Typora/typora-user-images/image-20240918113548484.png)

```bash
ollama create LLama3-8B-Chinese-Chat-medical -f ./Modelfile
```

![image-20240918113838368](/home/zj/.config/Typora/typora-user-images/image-20240918113838368.png)



# 测试截图

没有微调

![image-20240918173744731](/home/zj/.config/Typora/typora-user-images/image-20240918173744731.png)