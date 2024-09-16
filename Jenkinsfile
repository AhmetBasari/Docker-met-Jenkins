pipeline {
    agent any

    stages {
        stage('Provision EC2 with Terraform') {
            steps {
                script {
                    def output = sh(script: 'terraform apply -auto-approve -json', returnStdout: true).trim()
                    def jsonOutput = readJSON(text: output)
                    def instanceIp = jsonOutput.outputs.instance_ip.value
                    echo "Instance IP: ${instanceIp}"

                    writeFile file: 'inventory.yml', text: """
                    all:
                      hosts:
                        ${instanceIp}:
                          ansible_user: ec2-user
                          ansible_ssh_private_key_file: /path/to/your/private-key.pem
                    """
                }
            }
        }

        stage('Deploy Application with Ansible') {
            steps {
                sh 'ansible-playbook -i inventory.yml deploy-bookstore.yml'
            }
        }

        stage('Configure Prometheus') {
            steps {
                sh 'ssh -i /path/to/your/private-key.pem ec2-user@${instanceIp} sudo systemctl restart prometheus'
                echo 'Prometheus restarted for monitoring Flask app.'
            }
        }
    }
}
