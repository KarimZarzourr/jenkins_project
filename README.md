# jenkins_project

EECE 435L - Lab 10: Jenkins CI/CD pipeline for a small Python project.

- `app.py` - the application (`greet(name)`)
- `tests/test_app.py` - unit tests (pytest / unittest)
- `Jenkinsfile_Karim_Zarzour` - the pipeline: Setup, Lint, Test, Coverage, Security Scan, Deploy
- `deploy.py` - local deployment: copies the app to a release folder outside the workspace and runs a smoke test

Jenkins job: `Python-CI-CD`, Pipeline script from SCM, Git, branch `main`, script path `Jenkinsfile_Karim_Zarzour`.
