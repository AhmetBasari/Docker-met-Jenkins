pipeline {
    agent any

    stages {
        stage('Provision EC2 with Terraform') {
            steps {
                script {
                    // Run Terraform and capture output
                    def output = sh(script: 'terraform apply -auto-approve -json', returnStdout: true).trim()
                    def jsonOutput = readJSON(text: output)
                    def instanceIp = jsonOutput.outputs.instance_ip.value
                    echo "Instance IP: ${instanceIp}"

                    // Dynamically create Ansible inventory file
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
                // Deploy with Ansible
                sh 'ansible-playbook -i inventory.yml deploy-bookstore.yml'
            }
        }
    }
}
