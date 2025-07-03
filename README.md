# Forward-Github-Actions-Workflows-logs-to-elasticsearch


Everything should work if you configure your ES cluster and Workflow code right!


```yaml
- name: Forward Actions workflows logs to Elastic
  uses: zypeaLLas/upload-github-workflow-logs-to-elastic@1.16.0
  with:
    github_token: "${{ secrets.GITHUB }}"
    github_org: "yourOrg/User"
    github_repository: "yourRepo"
    github_run_id: "${{ github.run_id}}"
    elastic_host: "${{ secrets.ELASTIC_HOST }}"
    elastic_username: "${{ secrets.ELASTIC_USERNAME}}"
    elastic_password: "${{ secrets.ELASTIC_PASSWORD}}"
    elastic_index: "ci-cd"


![image](https://github.com/user-attachments/assets/5f595315-966d-4578-a406-1078cb5dabee)

![image](https://github.com/user-attachments/assets/37b0a178-3f32-48ac-9a5c-19f365786ac9)
