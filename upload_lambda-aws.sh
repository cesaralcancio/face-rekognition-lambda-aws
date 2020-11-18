# zip the file
zip face_analyse.zip face_analyse.py
# upload the file into the lambda
aws lambda update-function-code --function-name faceAnalisis --zip-file fileb://face_analyse.zip
# remove the zip file
rm face_analyse.zip