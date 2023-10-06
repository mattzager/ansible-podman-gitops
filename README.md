# ansible-podman-gitops
The basic demo walkthrough uses a basic gitops approach with Ansible to deploy, test and promote a simple web application in a podman container. Changes made to the repository in a new branch will trigger a deployment to development hosts. Branch merges to the main trunk will trigger a deployment to production hosts. Deployments happen on the host using an Ansible playbook that clones the git repository to the host, creates a new podman image and then starts a podman container running the application. 

Prerequisites
1. RHDP
    2. Ansible Workshop - Ansible for Red Hat Enterprise Linux  
2. Github
    1. Import Repository
        1. https://github.com/mattzager/ansible-podman-gitops.git
3. AAP
    1. Projects
        1. Create AAP project from this repository
            1. ansible-podman-gitops
    2. Workshop Inventory
        1. Groups
            1. Add groups
                1. appnodes
                2. devnodes
                3. qanodes
                4. prodnodes
        2. Hosts
            1. Add groups to nodes
                1. node1=appnodes, devnodes
                2. node2=appnodes, qanodes
                3. node3=appnodes, prodnodes
    3. Templates
        1. Add job templates
            1. prep_hosts
                1. Inventory: Workshop Inventory
                2. Project: ansible-podman-gitops
                3. Execution Environment: Default execution environment
                4. Playbook: prep_hosts.yml
                5. Credentials: Workshop Credentials
                6. Save->Launch
            2. webhook
                1. Inventory: Workshop Inventory
                2. Project: ansible-podman-gitops
                3. Execution Environment: Default execution environment
                4. Playbook: webhook.yml
                5. Credentials: Workshop Credentials
                6. Enable Webhook
                    1. Choose a Webhook Service
                        1. Github
                7. Save
    4. Github
        1. Settings
            1. Webhooks
                1. Add Webhook
                    1. Payload URL = webhook Template Webhook URL
                    2. Content type = application/json
                    3. Secret = webhook Template Webhook Key
                    4. SSL verification = Disable
                    5. Which events would you like to trigger this webhook?
                        1. Let me select individual events
                            1. Pull requests
                            2. Pushes
                    6. Add webhook
4. VSCode
    1. Terminal Proxy Tunnels (needed to use local browser to access apps in sandbox env)
        1. New Terminal
            1. ssh -L 8881:localhost:8881 -N node1 &
        2. New Terminal
            1. ssh -L 8880:localhost:8880 -N node3 &

System Walkthrough
1. RHDP Overview
    1. This is IaC - environment deployed by Ansible on AWS
        1. Developer Host
        2. AAP
        3. VSCode Server
        4. 3x Linux Hosts
2. AAP Overview
    1. Projects, Inventories, Templates
3. Github
    1. /app
        1. Simple demo Python Flask app and Dockerfile
    2. /playbooks
        1. Ansible playbooks used in AAP for responding to webhooks
    3. deploy.yml
        1. Ansible playbook run on hosts to deploy app in podman container

Demo Walkthrough
1. Deploy Dev
    1. Github
        1. Edit deploy.yml
            1. Change color: to color of choice
            2. Commit changes…
                1. Create a new branch for this commit and start a pull request
                2. Propose changes
    2. AAP
        1. Jobs
            1. [#]-webhook
                1. Observe task trigger
                2. Observe on_pr tasks
    3. VSCode
        1. Copy browser URL
        2. Open new tab, paste URL, add proxy/8881
        3. View application is your color
2. Promote to Prod
    1. Github 
        1. Merge pull request
        2. Confirm merge
    2. AAP
        1. Jobs
            1. [#]-webhook
                1. Observe task trigger
                2. Observe on_push tasks
    3. VSCode
        1. Copy app browser URL
        2. Open new tab, paste URL, change 8881 to 8880
        3. View application is your color
3. Deploy new Dev
    1. Github
        1. Edit deploy.yml
            1. Change color: to different color of choice
            2. Commit changes…
                1. Create a new branch for this commit and start a pull request
                2. Propose changes
                3. Create pull request
    2. AAP
        1. Jobs
            1. [#]-webhook
                1. Observe task trigger
                2. Observe on_pr tasks
    3. VSCode
        1. Browser /editor/proxy/8881 - view application is your new color
        2. Browser /editor/proxy/8880 - view production application has not changed
