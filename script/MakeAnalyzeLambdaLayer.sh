#!/bin/bash


usages() {
  echo "Usage.."
  echo " $1 [arm64|x86_64]"
  echo " $2 [python3.6|python3.7|python3.8|python3.9]"
  echo " $3 [dev|test|stg|prod]"
  echo " $4 [cloud|""]"

  echo " e.g.)"
  echo "  ./MakeanalyzeLambdaLayer.sh arm64 3.9 dev"

  exit 1
}

if [ "$1" = "" ]; then
  usages
fi

# The layer name can contain only letters, numbers, hyphens, and underscores.
LAYER_NAME=""
if ["$2" -ne ""]; then
  PYTHON_VERSION="$2"
  PYTHON_VERSION="${PYTHON_VERSION//./_}"
  echo "PYTHON_VERSION: " $PYTHON_VERSION
  LAYER_NAME="layer_$1_$PYTHON_VERSION""_common"
fi
echo "LAYER_NAME:" $LAYER_NAME

AWS_PROFILE=""
if [ "$3" = "dev" ]; then
  AWS_PROFILE="dev-derms-profile"
elif [ "$3" = "test" ]; then
  AWS_PROFILE="test-derms-profile"
elif [ "$3" = "stg" ]; then
  AWS_PROFILE="stg-derms-profile"
elif [ "$3" = "prod" ]; then
  AWS_PROFILE="prod-derms-profile"
else
  usages
fi
echo "AWS_PROFILE:" $AWS_PROFILE

zip_dir=$PWD/lambdaLayer/analyzeLambdaLayer/python
zip_filelist=""
cd lambdaLayer/analyzeLambdaLayer
for file in "python/*"; do
    echo $file
    zip_filelist+="$file "
    echo $zip_filelist
done
zip -r "layer.zip" $zip_filelist

ZIP_FILE_DIR="$PWD/layer.zip"
echo "ZIP_FILE_DIR:" $ZIP_FILE_DIR
if [ "$4" = "cloud" ]; then 
    aws lambda publish-layer-version --layer-name $LAYER_NAME --zip-file "fileb://"$ZIP_FILE_DIR
else
    aws lambda publish-layer-version --layer-name $LAYER_NAME --zip-file "fileb://"$ZIP_FILE_DIR --profile $AWS_PROFILE
fi