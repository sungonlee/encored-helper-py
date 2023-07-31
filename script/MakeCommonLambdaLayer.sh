#!/bin/bash

pwd=$PWD
zip_dir=$pwd/lambdaLayer/commonLambdaLayer/python
zip_vfilelist=""
cd lambdaLayer/commonLambdaLayer
for file in "python/*"; do
    echo $file
    zip_filelist+="$file "
    echo $zip_filelist
done
zip -r "layer.zip" $zip_filelist


aws lambda publish-layer-version --layer-name "fefew" --zip-file "fileb://$HOME/WorkSpace/forDevelopment/encored-helper-py/lambdaLayer/commonLambdaLayer/layer.zip" --profile "dev-derms-profile" 