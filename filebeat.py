import subprocess
import yaml
from yaml.loader import SafeLoader
import json
import socket

#Install Filebeat

def runcmd(cmd, verbose = False):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

hostname = socket.gethostname()

## su dung file de nhap path

# with open('/etc/filebeat/path.txt', 'r') as g:
#     dt = yaml.safe_load(g)

print("Do you need install filebeat or edit filebeat")
print("Nhap vao lua chon: setup || edit: ")
choose = str(input())
counter = 0
while choose != "setup" and  choose != "edit":
  counter = counter + 1
  if counter == 3:
    print("Max input exceeded")
    exit()
    
  print("Incorrect choose: ", choose)
  choose = str(input())


# print("Correct choose: ", choose)


if choose == 'setup':

    runcmd('wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -', verbose = True)
    runcmd('apt-get install apt-transport-https', verbose = True)
    runcmd('echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-8.x.list', verbose = True)
    runcmd('apt-get update', verbose = True)
    runcmd('apt-get install filebeat', verbose = True)
    runcmd('touch /etc/filebeat/filebeat.yml')
    runcmd('cd', verbose = True)
    runcmd('chown root:root /etc/filebeat/filebeat.yml', verbose = True)
    runcmd('systemctl start filebeat', verbose = True)
    runcmd('systemctl enable filebeat', verbose = True)


## su dung cmd de nhap path

    try:
        n = int(input("Nhap so path muon thuc hien: "))
        if n <= 0:
            exit()
    except:
        print('Phai nhap so tu nhien')
        exit()

    dt = []

    for i in range(n):
        dt.append(input('Nhap path thu %d: ' % (i+1)))

    data = {
    "filebeat.inputs": [
        {
            "type": "log",
            "enabled": True,
            "tags": hostname,
            "paths": dt
        }
    ],
    "setup.template.settings": {
        "index.number_of_shards": 1
    },
    "output.logstash": {
        "hosts": [
            "172.25.210.213:5033"
        ]
    },
    "processors": [
        {
            "add_host_metadata": {
                "when.not.contains.tags": "forwarded"
            }
        },
        {
            "add_cloud_metadata": None
        },
        {
            "add_docker_metadata": None
        },
        {
            "add_kubernetes_metadata": None
        }
    ]
    }

        # Write in filebeat.yml

    with open('/etc/filebeat/filebeat.yml', 'w') as dump_file:
        yaml.dump(data, dump_file)
        print(json.dumps(data, indent=4))

elif choose == 'edit':

    try:
        n = int(input("Nhap so path muon thuc hien: "))
        if n <= 0:
            exit()
    except:
        print('Phai nhap so tu nhien')
        exit()

    dt = []
    for i in range(n):
        dt.append(input('Nhap path thu %d: ' % (i+1)))

    data = {
    "filebeat.inputs": [
        {
            "type": "log",
            "enabled": True,
            "tags": hostname,
            "paths": dt
        }
    ],
    "setup.template.settings": {
        "index.number_of_shards": 1
    },
    "output.logstash": {
        "hosts": [
            "172.25.210.213:5033"
        ]
    },
    "processors": [
        {
            "add_host_metadata": {
                "when.not.contains.tags": "forwarded"
            }
        },
        {
            "add_cloud_metadata": None
        },
        {
            "add_docker_metadata": None
        },
        {
            "add_kubernetes_metadata": None
        }
    ]
    }

            # Write in filebeat.yml

    with open('/etc/filebeat/filebeat.yml', 'w') as dump_file:
        yaml.dump(data, dump_file)
        print(json.dumps(data, indent=4))
    runcmd('systemctl restart filebeat', verbose = True)

else:
    exit
