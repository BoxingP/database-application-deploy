# Build an Application

   ```shell
   $ ansible-galaxy collection install -r requirements.yaml
   ```

   ```shell
   $ ansible-playbook playbook.yaml --extra-vars "deploy_environment={{ environment }}"
   ```

where the optional values of the environment variable are `dev` and `test`