CodeReviewAl
- 
- Solution's author: Ponomarenko Kyrylo, @Allcash5412
- Last revision: 2025-01-07

#### Table of contents:
- [Description](#description)
- [Dependencies to run the app](#requirements-to-run-the-app)
- [Steps to run app](#steps-to-run-app)
- [Types of commits](#types-of-commits)
- [License](#license)


---

#### Description:
- In this assignment, your goal is to create a backend prototype for a Coding Assignment Auto-Review Tool using
Python. This tool will help automate the process of reviewing coding assignments by leveraging OpenAl's GPT
API (or alternative) for code analysis and the GitHub API for repository access. The task will be divided into two
#### Minimum requirements:
- The code should be written in Python and FastAPI.
- The project should have a descriptive name (e.g., "CodeReviewAl").
- The service must integrate OpenAl's API (or alternative API) for code analysis and the GitHub API for
repository access.
- Implement a single POST endpoint for code review (detailed below).
- Code should be covered by tests (using pytest and HTTPX). Aim for 70-80% test coverage.
- Nice to have: Use Redis for caching and performance optimization.
- Nice to have: Provide a Docker Compose file to run a Redis instance.
- The project should be easily compiled and packaged using poetry.
- Push the project's code to GitHub and provide access for review.
- Provide instructions on how to configure and run the project locally

---

#### P.S. Unfortunately, I didn't meet the deadline and implemented as AI reviewer: https://github.com/xtekky/gpt4free, 
#### which is on my local server. I also didn't have time to add tests, and in general I didn't finish the correct response output and error handling, and other items of minimum requirements

---

#### Requirements to run the app:

- Python: app was developed and tested using **3.12** version, but it should work with 3.10+ version
- have on your local machine  https://github.com/xtekky/gpt4free

---

#### Steps to run app

To start the project correctly, you need to follow these steps: 
1. Create an .env file similar to this one
```ini
    # Github api token
    GITHUB_API_TOKEN=ksdsisklkmklcmpokdkwidkpimaskop
    
    # AI chat url on your local machine
    AI_CHAT_API_URL=http://localhost/v1/chat/completions
    
    # Setting for Logger
    START_SETTING=DEV
  ```

2. To install all dependencies, from `requirements.txt` 
you have to create a virtual environment:
- 2.1
```bash
  python -m venv venv
```

- 2.2

Activate the virtual environment:

    Windows: venv\Scripts\activate

    Linux/MacOS: source venv/bin/activate

- 2.3

Install Dependencies:

Download and install all dependencies from the requirements.txt file using pip:
```bash
  pip install -r requirements.txt
  ```

- 2.4

Verify Installation:

After installation, verify that all dependencies are installed:
```bash
  pip list
```
3. Now you can easily run the application 
with the command `uvicorn src.main:app --reload`


4. Go to localhost:8000/docs or http://127.0.0.1:8000/docs
to view the endpoint

---

#### Types of commits

- `chore`: changes that do not directly affect the code, something that the end user will not see (installing/removing dependencies, project/tool settings)
- `docs`: changes related to documentation
- `feat`: new feature
- `fix`:  bug fix
- `perf`: changes related to performance improvement
- `refactor`: changes that are not related to feat or fix
- `revert`: revert a commit
- `test`: adding new tests or fixing existing ones

---

#### License

This project is licensed under the MIT License.