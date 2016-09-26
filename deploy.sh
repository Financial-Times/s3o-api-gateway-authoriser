zip authoriser.zip authoriser.py
aws lambda update-function-code --zip-file fileb://authoriser.zip --function-name s3o-api-gateway-custom-authoriser --publish --region eu-west-1