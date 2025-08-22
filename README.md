# MetaMesh
MetaMesh is a project that collects and categorizes online news information for display. Its main functionality involves gathering news content from various online sources and organizing it by topic or category. With MetaMesh, users can conveniently browse and find news that interests them, enjoying a personalized news reading experience.
## Install
```
git clone https://github.com/RobertLau666/MetaMesh.git
cd MetaMesh
conda create -n metamesh python=3.10
conda activate metamesh
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
