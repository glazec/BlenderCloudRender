import os
import requests
import sys

# render
def render():
    os.system('blender -b script.blend -o script.png -f 1 > scriptLog')


# save image
def saveBackblaze():
    files = getUploadFile()
    os.system('b2 authorize-account {id} {key}'.format(id=os.environ.get('B2Id'),key=os.environ.get('B2Key')))
    for i in files:
        os.system('b2 upload-file {bucketName} {localFilePath} {remoteFileName}'.format(bucketName='blender-cloud',localFilePath='/root/'+i,remoteFileName=i))

def getUploadFile():
    path = './'
    files =  [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    result = [i for i in files if ('blend') not in i and i[0]!='.' and i[-2:]!='py' and i!='StackScript']
    return result
    

def deleteServer():
    url = "https://api.linode.com/v4/linode/instances/{linodeId}".format(linodeId=os.environ.get('LinodeId'))
    headers = {"Authorization": "Bearer "+os.environ.get('LinodeToken'),
               "Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print("Successfully delete cloud server")
    else:
        print(response.json())
        raise Exception('Unable to delete server')

if __name__ == "__main__":
    render()
    saveBackblaze()
    deleteServer()
    