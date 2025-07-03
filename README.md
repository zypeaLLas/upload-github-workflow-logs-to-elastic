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
```

![upload_tomd1](https://github.com/user-attachments/assets/80c1ef3f-9dc1-4b21-8f7c-67de7cf88ce0)
![upload_tomd2](https://github.com/user-attachments/assets/faa1c3b6-6e33-42c8-a44a-88e9c2407b18)
