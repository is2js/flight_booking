- https://www.youtube.com/watch?v=1aRokwIizGo&list=PLdtwawCR2QjmdfhM-7SzDOVGop373bbgW&index=4
- https://github.com/KNehe/aero_bound_ventures-public/blob/main/backend/main.py
- structure: https://medium.com/@amirm.lavasani/how-to-structure-your-fastapi-projects-0219a6600a8f
- docker using uv:  https://docs.astral.sh/uv/guides/integration/fastapi/#deployment
- pre-commit: https://pre-commit.com/#install
- FastApi-Mail: https://sabuhish.github.io/fastapi-mail/
- backend/docker-compose.yaml
    - web: 8080 -> 80
    - db: 5438 -> 5432
        - username: postgres
        - password: postgres
        - dbname: postgres
        - host: localhost
    - smtp: 587
- AWS 
    - 파이참 터미널 > 새 SSH > AWS public ip 복사 + ubuntu + pem파일( 내문서 > security폴더) 
    - 일반터미널  
    ```shell
    #ssh -i <pem키 경로> ubuntu@<복사한ip>
    ssh -i 'C:\Users\cho_desktop\Documents\security\flight_booking_keypair.pem' ubuntu@15.165.203.18
    exit # 접속종료
    ```
  

```shell
cd backend
.\.venv\Scripts\activate
```
```shell
# uv run main.py
# docker build -t fastapi-app .
# docker run -p 8080:80 fastapi-app

# docker compose up --build
fastapi dev --port 8080 # 캐쉬때문에 db만 docker로 켜놓고, fastapi dev로 돌리는게 편함
```

### error
- 400: user register시 이미 존재 in create
- 401: user login시 잘못된 email or 잘못된 password in login


### git
- commit이후 작성한 것 중 일부폴더만 롤백
```shell
git status
git restore `crud/user.py`
```