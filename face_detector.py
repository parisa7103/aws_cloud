import boto3


def detect(image_url):
    client = boto3.client('rekognition')
    image_address = image_url
    with open(image_address, "rb") as image_file:
        response = client.detect_faces(
            Image={
                'Bytes': image_file.read()
            }
        )
        for face in response['FaceDetails']:
            print('Face detected:')
            print(f'  Age range: {face["AgeRange"]["Low"]}-{face["AgeRange"]["High"]}')
            print(f'  Gender: {face["Gender"]["Value"]}')
            print(f'  Smile: {face["Smile"]["Value"]}')
            print(f'  Emotions: {[emotion["Type"] for emotion in face["Emotions"]]}')
