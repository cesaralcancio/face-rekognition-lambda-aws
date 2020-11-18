import boto3

s3 = boto3.resource('s3')
client = boto3.client('rekognition')


def list_images():
    images = []
    bucket = s3.Bucket('alcancio-fa-images')
    for image in bucket.objects.all():
        images.append(image.key)
    print(images)
    return images


def apply_index_colecao(local_images):
    for image in local_images:
        response = client.index_faces(
            CollectionId='faces',
            DetectionAttributes=[
            ],
            # remove the .jpeg
            ExternalImageId=image[:-5],
            Image={
                'S3Object': {
                    'Bucket': 'alcancio-fa-images',
                    'Name': image
                },
            },
        )


general_images = list_images()
apply_index_colecao(general_images)
