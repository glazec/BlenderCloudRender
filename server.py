import os
import requests
import sys
import subprocess
import json

# render
def render():
    frame = settings['Frame']
    fileName = settings['BlenderFile']
    os.system('blender -b {fileName} -o {output} -f {frame} > script.log'.format(fileName=fileName,frame=frame,output=fileName))


# save image
def saveBackblaze():
    print('Uploading File to BackBlaze')
    files = getUploadFile()
    os.system('b2 authorize-account {id} {key}'.format(id=settings['B2Id'],key=settings['B2Key']))
    for i in files:
        os.system('b2 upload-file {bucketName} {localFilePath} {remoteFileName}'.format(bucketName='blender-cloud',localFilePath='/root/'+i,remoteFileName=i))

def getUploadFile():
    path = './'
    files =  [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    result = [i for i in files if ('blend') not in i and i[0]!='.' and i[-2:]!='py' and i!='StackScript']
    return result
    

def deleteServer():
    url = "https://api.linode.com/v4/linode/instances/{linodeId}".format(linodeId=settings['LinodeId'])
    headers = {"Authorization": "Bearer "+settings['LinodeToken'],
               "Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print("Successfully delete cloud server")
    else:
        print(response.json())
        raise Exception('Unable to delete server')

if __name__ == "__main__":
    settings = {}
    with open('settings.json') as f:
        settings = json.load(f)
    render()
    saveBackblaze()
    deleteServer()
    
