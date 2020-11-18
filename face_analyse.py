import boto3
import json

client = boto3.client('rekognition')
s3 = boto3.resource('s3')


def detect_face():
    detected_faces = client.index_faces(
        CollectionId='faces',
        DetectionAttributes=['DEFAULT'],
        # remove the .jpeg
        ExternalImageId='temporary-image',
        Image={
            'S3Object': {
                'Bucket': 'alcancio-fa-images',
                'Name': 'for_analysis.jpeg'
            },
        },
    )
    return detected_faces


def extract_face_id(detected_faces):
    extracted_face_id = []
    for i in range(len(detected_faces['FaceRecords'])):
        extracted_face_id.append(detected_faces['FaceRecords'][i]['Face']['FaceId'])
    return extracted_face_id


def compare_faces(detected_faces):
    resultado = []
    for faceids in detected_faces:
        resultado.append(
            client.search_faces(
                CollectionId='faces',
                FaceId=faceids,
                FaceMatchThreshold=80,
                MaxFaces=10,
            )
        )
    return resultado


def gera_dados_front(compared_faces):
    dados_json = []
    for face in compared_faces:
        if(len(face.get('FaceMatches'))) > 0:
            perfil = dict(nome=face.get('FaceMatches')[0]['Face']['ExternalImageId'],
                          faceMatch=round(face.get('FaceMatches')[0]['Similarity'], 2))
            dados_json.append(perfil)
    return dados_json


def publica_dados(dados_json):
    arquivo = s3.Object('alcancio-fa-site', 'dados.json')
    arquivo.put(Body=json.dumps(dados_json))


def exclui_imagem_colecao(faceid_detectadas):
    client.delete_faces(
        CollectionId='faces',
        FaceIds=faceid_detectadas,
    )


def main(event, context):
    detected_faces_global = detect_face()
    extract_face_id_global = extract_face_id(detected_faces_global)
    compared_faces = compare_faces(extract_face_id_global)
    dados_front = gera_dados_front(compared_faces)
    exclui_imagem_colecao(extract_face_id_global)
    publica_dados(dados_json=dados_front)

    print(json.dumps(detected_faces_global, indent=4))
    print(extract_face_id_global)
    print(json.dumps(compared_faces, indent=4))
    print(json.dumps(gera_dados_front(compared_faces), indent=4))
