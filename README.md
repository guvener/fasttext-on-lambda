# Dominant language detection with fastText Layer on AWS Lambda
Facebook research team's fastText library provides useful methods for text classification.
In this repository, We use [facebookresearch/fastText](https://github.com/facebookresearch/fastText) and [trained model](https://fasttext.cc/docs/en/language-identification.html) for language identification.

## AWS Layers
First, prepare fastText library and trained language models as layers to reduce the size of deployment packages.

### Layer 1 - fastText using fasttext-wheel
We install the fastText library using the fasttext-wheel python package.

#### Information
`aws-fasttext-layer-python3.10-arm64.zip` layer provided in layer directory is prepared for `Python 3.10` runtime and uses `arm64` architecture.  
You can create a layer by uploading the zip file with the given configuration or build your own using the instructions below.

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

There are two trained models: lid.176.bin is more accurate, but it requires uploading to an S3 bucket due to its large file size.
`fasttext-language-model.zip` file provided in GitHub repository uses light pre trained model `lid.176.ftz`, replace lid.176.ftz with lid.176.bin in case you build large model as below.

```bash
# create a pretrained folder, download model from fbai's public files and zip folder.
mkdir pretrained
cd pretrained
curl -O https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
cd ..
zip -r fasttext-language-model.zip pretrained
```

## Create a lambda function in Python
Configure for `Python 3.10` runtime and use `arm64` architecture (if using provided layer in this repository).  
Copy `handler.py` contents to your function and make sure you have added both layers to your function.

### Test Deployment
A test event JSON object is provided in test directory to mock the structure of request and response.

```json
{
  "text": "Perché i semiconduttori sono il pezzo di tecnologia più prezioso e conteso oggi?"
}
```
## Conclusion
fastText proves to be a cost-effective and efficient alternative to other managed dominant language detection services. Our tests have consistently shown that for texts over 100 characters, the detected languages are often the same as those produced by managed services such as AWS Comprehend and Google Language API.
