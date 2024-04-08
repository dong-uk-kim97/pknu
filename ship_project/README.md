# 프로젝트 배경
코로나19 이후 물류 정체로 인해 다수의 항만에서 선박 대기 시간이 길어지고, 이로 인한 물류 지연이 화두가 되고 있습니다. 

특히 전 세계 물동량의 85%를 차지하는 해운 물류 분야에서 항만 정체는 큰 문제로 인식되고 있는 상황입니다. 

저희 조는 접안 전에 선박이 해상에 정박하는 시간을 대기시간으로 정의하고, 선박의 제원 및 운항 정보를 활용하여 산출된 항차 데이터를 활용해 항만 內 선박의 대기 시간을 예측하는 AI 알고리즘을 개발하였습니다.

# 데이터 수집
HD 현대 AI Challenge

https://dacon.io/competitions/official/236158/overview/description

# 프로젝트 기간
2024년 4월 1일~ 4월 8일까지

# 데이터 분석
![히트맵](heatmap.png)

# 팀원 소개
| 이름 | 역할 |
|:-:|:-:|
|김동욱|데이터 전처리,    데이터 시각화,   데이터 분석,   발표|
|박재현|데이터 전처리,    데이터 분석,   PPT제작,    발표|
|이보윤|데이터 전처리,    데이터 분석,   총괄 지휘|
|조재경|데이터 분석,   PPT제작,   발표|
|최서윤|데이터 분석,   문서 작업|

# 개발 환경
```
absl-py                   2.1.0                    pypi_0    pypi
accelerate                0.21.0                   pypi_0    pypi
aiohttp                   3.9.3                    pypi_0    pypi
aiohttp-cors              0.7.0                    pypi_0    pypi
aiosignal                 1.3.1                    pypi_0    pypi
alembic                   1.13.1                   pypi_0    pypi
aliyun-python-sdk-core    2.15.0                   pypi_0    pypi
aliyun-python-sdk-kms     2.16.2                   pypi_0    pypi
ansicon                   1.89.0                   pypi_0    pypi
antlr4-python3-runtime    4.9.3                    pypi_0    pypi
anyio                     4.3.0                    pypi_0    pypi
argon2-cffi               23.1.0                   pypi_0    pypi
argon2-cffi-bindings      21.2.0           py39h2bbff1b_0
arrow                     1.3.0                    pypi_0    pypi
asttokens                 2.4.1                    pypi_0    pypi
async-lru                 2.0.4                    pypi_0    pypi
async-timeout             4.0.3                    pypi_0    pypi
attrs                     23.2.0                   pypi_0    pypi
autogluon                 1.0.0                    pypi_0    pypi
autogluon-common          1.0.0                    pypi_0    pypi
autogluon-core            1.0.0                    pypi_0    pypi
autogluon-features        1.0.0                    pypi_0    pypi
autogluon-multimodal      1.0.0                    pypi_0    pypi
autogluon-tabular         1.0.0                    pypi_0    pypi
autogluon-timeseries      1.0.0                    pypi_0    pypi
babel                     2.14.0                   pypi_0    pypi
backcall                  0.2.0              pyhd3eb1b0_0
backoff                   2.2.1                    pypi_0    pypi
beautifulsoup4            4.12.3                   pypi_0    pypi
bleach                    6.1.0                    pypi_0    pypi
blessed                   1.20.0                   pypi_0    pypi
blis                      0.7.11                   pypi_0    pypi
boto3                     1.34.75                  pypi_0    pypi
botocore                  1.34.75                  pypi_0    pypi
branca                    0.7.1                    pypi_0    pypi
ca-certificates           2024.3.11            haa95532_0
cachetools                5.3.3                    pypi_0    pypi
catalogue                 2.0.10                   pypi_0    pypi
catboost                  1.2.3                    pypi_0    pypi
category-encoders         2.6.3                    pypi_0    pypi
certifi                   2024.2.2                 pypi_0    pypi
cffi                      1.16.0           py39h2bbff1b_0
charset-normalizer        3.3.2                    pypi_0    pypi
click                     8.1.7                    pypi_0    pypi
cloudpathlib              0.16.0                   pypi_0    pypi
cloudpickle               3.0.0                    pypi_0    pypi
colorama                  0.4.6            py39haa95532_0
colorful                  0.5.6                    pypi_0    pypi
colorlog                  6.8.2                    pypi_0    pypi
colour                    0.1.5                    pypi_0    pypi
comm                      0.2.2                    pypi_0    pypi
confection                0.1.4                    pypi_0    pypi
contourpy                 1.2.0                    pypi_0    pypi
crcmod                    1.7                      pypi_0    pypi
croniter                  1.4.1                    pypi_0    pypi
cryptography              42.0.5                   pypi_0    pypi
cycler                    0.12.1                   pypi_0    pypi
cymem                     2.0.8                    pypi_0    pypi
datasets                  2.10.1                   pypi_0    pypi
dateutils                 0.6.12                   pypi_0    pypi
debugpy                   1.8.1                    pypi_0    pypi
decorator                 5.1.1              pyhd3eb1b0_0
deepdiff                  6.7.1                    pypi_0    pypi
defusedxml                0.7.1              pyhd3eb1b0_0
dill                      0.3.6                    pypi_0    pypi
distlib                   0.3.8                    pypi_0    pypi
dtreeviz                  2.2.2                    pypi_0    pypi
editor                    1.6.6                    pypi_0    pypi
eli5                      0.13.0                   pypi_0    pypi
entrypoints               0.4              py39haa95532_0
et-xmlfile                1.1.0                    pypi_0    pypi
evaluate                  0.4.1                    pypi_0    pypi
exceptiongroup            1.2.0            py39haa95532_0
executing                 2.0.1                    pypi_0    pypi
fastai                    2.7.14                   pypi_0    pypi
fastapi                   0.110.1                  pypi_0    pypi
fastcore                  1.5.29                   pypi_0    pypi
fastdownload              0.0.7                    pypi_0    pypi
fastjsonschema            2.19.1                   pypi_0    pypi
fastprogress              1.0.3                    pypi_0    pypi
filelock                  3.13.3                   pypi_0    pypi
folium                    0.16.0                   pypi_0    pypi
fonttools                 4.50.0                   pypi_0    pypi
fqdn                      1.5.1                    pypi_0    pypi
frozenlist                1.4.1                    pypi_0    pypi
fsspec                    2024.3.1                 pypi_0    pypi
future                    1.0.0                    pypi_0    pypi
gdown                     5.1.0                    pypi_0    pypi
gluonts                   0.14.4                   pypi_0    pypi
google-api-core           2.18.0                   pypi_0    pypi
google-auth               2.29.0                   pypi_0    pypi
googleapis-common-protos  1.63.0                   pypi_0    pypi
gpustat                   1.1.1                    pypi_0    pypi
greenlet                  3.0.3                    pypi_0    pypi
grpcio                    1.62.1                   pypi_0    pypi
h11                       0.14.0                   pypi_0    pypi
httpcore                  1.0.5                    pypi_0    pypi
httpx                     0.27.0                   pypi_0    pypi
huggingface-hub           0.22.2                   pypi_0    pypi
hyperopt                  0.2.7                    pypi_0    pypi
idna                      3.6                      pypi_0    pypi
imageio                   2.34.0                   pypi_0    pypi
importlib-metadata        7.1.0                    pypi_0    pypi
importlib-resources       6.4.0                    pypi_0    pypi
iniconfig                 2.0.0                    pypi_0    pypi
inquirer                  3.2.4                    pypi_0    pypi
ipykernel                 6.29.4                   pypi_0    pypi
ipython                   8.18.1                   pypi_0    pypi
ipython_genutils          0.2.0              pyhd3eb1b0_1
ipywidgets                8.1.2                    pypi_0    pypi
isoduration               20.11.0                  pypi_0    pypi
itsdangerous              2.1.2                    pypi_0    pypi
jedi                      0.19.1                   pypi_0    pypi
jinja2                    3.1.3            py39haa95532_0
jinxed                    1.2.1                    pypi_0    pypi
jmespath                  0.10.0                   pypi_0    pypi
joblib                    1.3.2                    pypi_0    pypi
json5                     0.9.24                   pypi_0    pypi
jsonpointer               2.4                      pypi_0    pypi
jsonschema                4.17.3                   pypi_0    pypi
jsonschema-specifications 2023.12.1                pypi_0    pypi
jupyter                   1.0.0                    pypi_0    pypi
jupyter-client            8.6.1                    pypi_0    pypi
jupyter-console           6.6.3                    pypi_0    pypi
jupyter-core              5.7.2                    pypi_0    pypi
jupyter-events            0.10.0                   pypi_0    pypi
jupyter-lsp               2.2.4                    pypi_0    pypi
jupyter-server            2.13.0                   pypi_0    pypi
jupyter-server-terminals  0.5.3                    pypi_0    pypi
jupyter_client            7.4.9            py39haa95532_0
jupyter_core              5.5.0            py39haa95532_0
jupyter_events            0.8.0            py39haa95532_0
jupyter_server            2.10.0           py39haa95532_0
jupyter_server_terminals  0.4.4            py39haa95532_1
jupyterlab                4.1.5                    pypi_0    pypi
jupyterlab-pygments       0.3.0                    pypi_0    pypi
jupyterlab-server         2.25.4                   pypi_0    pypi
jupyterlab-widgets        3.0.10                   pypi_0    pypi
jupyterlab_pygments       0.2.2            py39haa95532_0
kiwisolver                1.4.5                    pypi_0    pypi
langcodes                 3.3.0                    pypi_0    pypi
lazy-loader               0.3                      pypi_0    pypi
libsodium                 1.0.18               h62dcd97_0
lightgbm                  4.1.0                    pypi_0    pypi
lightning                 2.0.9.post0              pypi_0    pypi
lightning-cloud           0.5.65                   pypi_0    pypi
lightning-utilities       0.11.2                   pypi_0    pypi
llvmlite                  0.42.0                   pypi_0    pypi
mako                      1.3.2                    pypi_0    pypi
mariadb                   1.1.10                   pypi_0    pypi
markdown                  3.6                      pypi_0    pypi
markdown-it-py            3.0.0                    pypi_0    pypi
markupsafe                2.1.5                    pypi_0    pypi
matplotlib                3.8.3                    pypi_0    pypi
matplotlib-inline         0.1.6            py39haa95532_0
mdurl                     0.1.2                    pypi_0    pypi
mistune                   3.0.2                    pypi_0    pypi
mlforecast                0.10.0                   pypi_0    pypi
mljar-supervised          1.1.6                    pypi_0    pypi
model-index               0.1.11                   pypi_0    pypi
mpmath                    1.3.0                    pypi_0    pypi
msgpack                   1.0.8                    pypi_0    pypi
multidict                 6.0.5                    pypi_0    pypi
multiprocess              0.70.14                  pypi_0    pypi
murmurhash                1.0.10                   pypi_0    pypi
mysqlclient               2.2.4                    pypi_0    pypi
nb_conda_kernels          2.3.1            py39haa95532_0
nbclassic                 1.0.0            py39haa95532_0
nbclient                  0.10.0                   pypi_0    pypi
nbconvert                 7.16.3                   pypi_0    pypi
nbformat                  5.10.3                   pypi_0    pypi
nest-asyncio              1.6.0            py39haa95532_0
networkx                  3.2.1                    pypi_0    pypi
nlpaug                    1.1.11                   pypi_0    pypi
nltk                      3.8.1                    pypi_0    pypi
notebook                  7.1.2                    pypi_0    pypi
notebook-shim             0.2.4                    pypi_0    pypi
nptyping                  2.4.1                    pypi_0    pypi
numba                     0.59.1                   pypi_0    pypi
numpy                     1.24.4                   pypi_0    pypi
nvidia-ml-py              12.535.133               pypi_0    pypi
nvidia-ml-py3             7.352.0                  pypi_0    pypi
omegaconf                 2.2.3                    pypi_0    pypi
opencensus                0.11.4                   pypi_0    pypi
opencensus-context        0.1.3                    pypi_0    pypi
opendatalab               0.0.10                   pypi_0    pypi
openmim                   0.3.9                    pypi_0    pypi
openpyxl                  3.1.2                    pypi_0    pypi
openssl                   3.0.13               h2bbff1b_0
openxlab                  0.0.37                   pypi_0    pypi
optuna                    3.6.1                    pypi_0    pypi
ordered-set               4.1.0                    pypi_0    pypi
orjson                    3.10.0                   pypi_0    pypi
oss2                      2.17.0                   pypi_0    pypi
overrides                 7.7.0                    pypi_0    pypi
packaging                 24.0                     pypi_0    pypi
pandas                    2.1.4                    pypi_0    pypi
pandocfilters             1.5.1                    pypi_0    pypi
parso                     0.8.3              pyhd3eb1b0_0
patsy                     0.5.6                    pypi_0    pypi
pickleshare               0.7.5           pyhd3eb1b0_1003
pillow                    10.2.0                   pypi_0    pypi
pip                       24.0                     pypi_0    pypi
platformdirs              3.11.0                   pypi_0    pypi
plotly                    5.20.0                   pypi_0    pypi
pluggy                    1.4.0                    pypi_0    pypi
preshed                   3.0.9                    pypi_0    pypi
prometheus-client         0.20.0                   pypi_0    pypi
prometheus_client         0.14.1           py39haa95532_0
prompt-toolkit            3.0.43           py39haa95532_0
proto-plus                1.23.0                   pypi_0    pypi
protobuf                  4.25.3                   pypi_0    pypi
psutil                    5.9.8                    pypi_0    pypi
pure_eval                 0.2.2              pyhd3eb1b0_0
py-spy                    0.3.14                   pypi_0    pypi
py4j                      0.10.9.7                 pypi_0    pypi
pyarrow                   6.0.1                    pypi_0    pypi
pyasn1                    0.6.0                    pypi_0    pypi
pyasn1-modules            0.4.0                    pypi_0    pypi
pycparser                 2.22                     pypi_0    pypi
pycryptodome              3.20.0                   pypi_0    pypi
pydantic                  1.10.14                  pypi_0    pypi
pygments                  2.17.2                   pypi_0    pypi
pyjwt                     2.8.0                    pypi_0    pypi
pymysql                   1.1.0                    pypi_0    pypi
pyparsing                 3.1.2                    pypi_0    pypi
pyrsistent                0.20.0                   pypi_0    pypi
pysocks                   1.7.1                    pypi_0    pypi
pytesseract               0.3.10                   pypi_0    pypi
pytest                    8.1.1                    pypi_0    pypi
python                    3.9.19               h1aa4202_0
python-dateutil           2.9.0.post0              pypi_0    pypi
python-fastjsonschema     2.16.2           py39haa95532_0
python-graphviz           0.20.3                   pypi_0    pypi
python-json-logger        2.0.7            py39haa95532_0
python-multipart          0.0.9                    pypi_0    pypi
pytorch-lightning         2.0.9.post0              pypi_0    pypi
pytorch-metric-learning   1.7.3                    pypi_0    pypi
pytz                      2023.4                   pypi_0    pypi
pywavelets                1.6.0                    pypi_0    pypi
pywin32                   306                      pypi_0    pypi
pywinpty                  2.0.13                   pypi_0    pypi
pyyaml                    6.0.1            py39h2bbff1b_0
pyzmq                     25.1.2                   pypi_0    pypi
qtconsole                 5.5.1                    pypi_0    pypi
qtpy                      2.4.1                    pypi_0    pypi
ray                       2.6.3                    pypi_0    pypi
readchar                  4.0.6                    pypi_0    pypi
referencing               0.34.0                   pypi_0    pypi
regex                     2023.12.25               pypi_0    pypi
requests                  2.28.2                   pypi_0    pypi
responses                 0.18.0                   pypi_0    pypi
rfc3339-validator         0.1.4            py39haa95532_0
rfc3986-validator         0.1.1            py39haa95532_0
rich                      13.4.2                   pypi_0    pypi
rpds-py                   0.18.0                   pypi_0    pypi
rsa                       4.9                      pypi_0    pypi
runs                      1.2.2                    pypi_0    pypi
s3transfer                0.10.1                   pypi_0    pypi
safetensors               0.4.2                    pypi_0    pypi
scikit-image              0.20.0                   pypi_0    pypi
scikit-learn              1.4.1.post1              pypi_0    pypi
scikit-plot               0.3.7                    pypi_0    pypi
scipy                     1.9.1                    pypi_0    pypi
seaborn                   0.13.2                   pypi_0    pypi
send2trash                1.8.2            py39haa95532_0
sentencepiece             0.2.0                    pypi_0    pypi
seqeval                   1.2.2                    pypi_0    pypi
setuptools                60.2.0                   pypi_0    pypi
shap                      0.45.0                   pypi_0    pypi
six                       1.16.0             pyhd3eb1b0_1
slicer                    0.0.7                    pypi_0    pypi
smart-open                6.4.0                    pypi_0    pypi
sniffio                   1.3.1                    pypi_0    pypi
soupsieve                 2.5              py39haa95532_0
spacy                     3.7.4                    pypi_0    pypi
spacy-legacy              3.0.12                   pypi_0    pypi
spacy-loggers             1.0.5                    pypi_0    pypi
sqlalchemy                2.0.29                   pypi_0    pypi
sqlite                    3.41.2               h2bbff1b_0
srsly                     2.4.8                    pypi_0    pypi
stack-data                0.6.3                    pypi_0    pypi
stack_data                0.2.0              pyhd3eb1b0_0
starlette                 0.37.2                   pypi_0    pypi
starsessions              1.3.0                    pypi_0    pypi
statsforecast             1.4.0                    pypi_0    pypi
statsmodels               0.14.1                   pypi_0    pypi
sympy                     1.12                     pypi_0    pypi
tabulate                  0.9.0                    pypi_0    pypi
tenacity                  8.2.3                    pypi_0    pypi
tensorboard               2.16.2                   pypi_0    pypi
tensorboard-data-server   0.7.2                    pypi_0    pypi
tensorboardx              2.6.2.2                  pypi_0    pypi
terminado                 0.18.1                   pypi_0    pypi
text-unidecode            1.3                      pypi_0    pypi
thinc                     8.2.3                    pypi_0    pypi
threadpoolctl             3.4.0                    pypi_0    pypi
tifffile                  2024.2.12                pypi_0    pypi
timm                      0.9.16                   pypi_0    pypi
tinycss2                  1.2.1            py39haa95532_0
tokenizers                0.13.3                   pypi_0    pypi
tomli                     2.0.1                    pypi_0    pypi
toolz                     0.12.1                   pypi_0    pypi
torch                     2.0.1                    pypi_0    pypi
torchmetrics              1.1.2                    pypi_0    pypi
torchvision               0.15.2                   pypi_0    pypi
tornado                   6.4                      pypi_0    pypi
tqdm                      4.65.2                   pypi_0    pypi
traitlets                 5.14.2                   pypi_0    pypi
transformers              4.31.0                   pypi_0    pypi
typer                     0.9.4                    pypi_0    pypi
types-python-dateutil     2.9.0.20240316           pypi_0    pypi
typing-extensions         4.10.0                   pypi_0    pypi
typing_extensions         4.9.0            py39haa95532_1
tzdata                    2024.1                   pypi_0    pypi
uri-template              1.3.0                    pypi_0    pypi
urllib3                   1.26.18                  pypi_0    pypi
utilsforecast             0.0.10                   pypi_0    pypi
uvicorn                   0.29.0                   pypi_0    pypi
vc                        14.2                 h21ff451_1
virtualenv                20.21.0                  pypi_0    pypi
vs2015_runtime            14.27.29016          h5e58377_2
wasabi                    1.1.2                    pypi_0    pypi
wcwidth                   0.2.13                   pypi_0    pypi
weasel                    0.3.4                    pypi_0    pypi
webcolors                 1.13                     pypi_0    pypi
webencodings              0.5.1                    pypi_0    pypi
websocket-client          1.7.0                    pypi_0    pypi
websockets                12.0                     pypi_0    pypi
werkzeug                  3.0.2                    pypi_0    pypi
wheel                     0.41.2           py39haa95532_0
widgetsnbextension        4.0.10                   pypi_0    pypi
window-ops                0.0.15                   pypi_0    pypi
winpty                    0.4.3                         4
wordcloud                 1.9.3                    pypi_0    pypi
xgboost                   2.0.3                    pypi_0    pypi
xlrd                      2.0.1                    pypi_0    pypi
xmod                      1.8.1                    pypi_0    pypi
xxhash                    3.4.1                    pypi_0    pypi
xyzservices               2023.10.1                pypi_0    pypi
yaml                      0.2.5                he774522_0
yarl                      1.9.4                    pypi_0    pypi
zeromq                    4.3.5                hd77b12b_0
zipp                      3.18.1                   pypi_0    pypi
```
