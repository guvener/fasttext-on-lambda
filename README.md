# Dominant language detection with fastText Layer on AWS Lambda
Facebook research team's fastText library provides useful methods for text classification.

## AWS Layers
First prepare fastText library and trained language models as layers to reduce the size of deployment packages.

### Layer 1 - fastText using fasttext-wheel
We install fastText library using fasttext-wheel python library.

#### Information
`aws-fasttext-layer-python3.10-arm64.zip` file provided in layer directory is prepared for `Python 3.10` runtime and using `arm64` architecture.
You can create a layer uploading zip file with this configuration or build your own using instructions below.

# FastText Predict Dominant Language
https://github.com/facebookresearch/fastText

### fastText using fasttext-wheel
We install fastText library using fasttext-wheel python library.

```console
docker run -it ubuntu
```
The flag “-it” is used to open an interactive shell.

```console
apt update
apt install python3.10
apt install python3-pip
# Use pip install
mkdir -p layer/python/lib/python3.10/site-packages
pip3 install fasttext-wheel -t layer/python/lib/python3.10/site-packages/
cd layer
# apt install zip
zip -r mypackage.zip *
# Now we have to copy the zip file mypackage.zip to our local folder.
# open a new command prompt and get the container ID by running:
docker ps -a
docker cp <Container-ID:path_of_zip_file>
# for example:
docker cp 79e3e2cdc863:/layer/mypackage.zip /Users/guvenergokce
```


### Layer 2 - Language identification model

There are two trained models, lid.176.bin is more accurate though due to large file size, needs to be uploaded from s3 bucket.

#### Information
`fasttext-language-model.zip` file provided in layer directory uses light pretrained model `lid.176.ftz`, replace lid.176.ftz with lid.176.bin in case you build large model as below.

```bash
# create a pretrained folder, download model from fbai's public files and zip folder.
mkdir pretrained
cd pretrained
curl -O https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
cd ..
zip -r fasttext-language-model.zip pretrained
```

## Create a lambda function in Python
Configure for `Python 3.10` runtime and using `arm64` architecture (if you are using layer provided in this repostirory).
Copy contents from `handler.py` file to your function and make sure your 2 layers are attached to new function.

### Test Deployment
A test event JSON object is provided in test directory to mock the structure of request and response.
