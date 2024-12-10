from flask import Flask, jsonify, render_template
import subprocess
import json

app = Flask(__name__)

def get_deployments(cluster_name):
    try:
        result = subprocess.run(
            ["kubectl", "get", "deployments", "--context", cluster_name, "-o", "json", "--all-namespaces", "--field-selector", "metadata.namespace!=kube-system"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return str(e)

def parse_deployments(deployments_json):
    deployments = json.loads(deployments_json)
    deployment_info = []
    for item in deployments['items']:
        name = item['metadata']['name']
        image = item['spec']['template']['spec']['containers'][0]['image']
        deployment_info.append({'name': name, 'image': image})
    return deployment_info

deployments_json = get_deployments("aks-01")
deployment_info = parse_deployments(deployments_json)

def uat_deployments():
    deployments = get_deployments("aks-01")
    parsed_deployments = parse_deployments(deployments)
    return parsed_deployments

def production_deployments():
    deployments = get_deployments("aks-01")
    parsed_deployments = parse_deployments(deployments)
    return parsed_deployments

@app.route('/')
def home():
    print('Some code .....')
    uat_deployments_data=uat_deployments()
    # print(uat_deployments_data)
    # create a for loop to iterate through the list of deployments, print the name and image of each deployment
    # for deployment in uat_deployments_data:
    #     print(deployment['name'], deployment['image'])
    return render_template('home.html', uat_deployments=uat_deployments_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)