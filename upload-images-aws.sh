# list faces
aws rekognition list-faces --collection-id faces
# create collection for faces
aws rekognition create-collection --collection-id faces
# delete collections for faces
aws rekognition delete-collection --collection-id faces
# run python to setup
python3 rekognition_setup_images.py
# list faces
aws rekognition list-faces --collection-id faces | grep External
# upload all images
aws s3 sync ./la-casa-de-papel-images s3://alcancio-fa-images
# delete file
aws s3 rm s3://alcancio-fa-images/for_analysis.jpeg
# copy file
aws s3 cp ./la-casa-de-papel-for-analysis/for_analysis.jpeg s3://alcancio-fa-images/for_analysis.jpeg