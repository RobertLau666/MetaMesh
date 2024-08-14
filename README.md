# MetaMesh
## Install
```
git clone https://github.com/RobertLau666/MetaMesh.git
cd MetaMesh
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
## Prepare
1. set ```openai_api_key```
   ```
   export OPENAI_API_KEY=your_openai_api_key
   ```
2. download model [csebuetnlp/mT5_multilingual_XLSum](https://huggingface.co/csebuetnlp/mT5_multilingual_XLSum), put it under ```models/```

## Run
```
python app.py
```
