# Encored Japan Python Common Helper Library


## パッケージ作成

```
python setup.py sdist

```

## Lambdaレイヤーのライブラリ管理

1. 共通ライブラリ（commonLambdaLayer）

- retry関連ライブラリ
  - retry==0.9.2
  - decorator==5.1.1
  - py == 1.11.0
- pymysql==1.0.2
- hashids==1.3.1
- requests関連ライブラリ
  - requests==2.82.2
  - charset-normalizer==2.1.1
  - idna==3.4
  - urllib3==1.26.12
  - certifi==2022.9.14
- requests_pkcs12関連ライブラリ
  - cryptography==41.0.2
  - pyOpenSSL==23.2.0
  - cffi==1.15.1
  - pycparser==2.21


2. 分析用ライブラリ（analyzeLambdaLayer）
- pandas関連ライブラリ
  - pandas==2.0.3
  - python-dateutil==2.8.2
  - pytz==2022.2.1
  - numpy==1.23.3
  - six==1.16.0