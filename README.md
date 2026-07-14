품바 — 품의서 Agent
언론사 광고/협찬 공문을 정리하고, 광고비 시트를 붙여넣으면 사내 양식 품의서를 자동 생성하는 홍보그룹 웹앱.
구조
```
app.py               Flask 서버 (Anthropic API 프록시 — 키는 서버에만 존재)
static/index.html    품바 프론트엔드
Dockerfile           Coolify 자동 빌드용
requirements.txt
```
배포 절차 (AX Store)
1. GitLab 저장소 생성 & 코드 푸시
```bash
git init
git add .
git commit -m "품바 v1"
git remote add origin https://gitlab.<사내주소>/<계정>/poomba.git
git push -u origin main        # 비밀번호 자리에 개인 액세스 토큰
```
⚠️ API 키는 절대 커밋하지 않는다 (.env는 .gitignore에 포함됨)

2. Coolify 배포
New Resource → GitLab 저장소 선택, 주소를 `ssh://git@gitlab.<사내주소>/<계정>/poomba.git` 형식으로
Build Pack: Dockerfile (자동 감지), Port: 8080
Environment Variables에 `ANTHROPIC_API_KEY` 등록
Deploy → 완료 후 `배포주소/health` 접속해 `"key_configured": true` 확인

3. Webhook 자동배포
Coolify 리소스의 Webhook URL 복사 → GitLab 프로젝트 Settings > Webhooks에 등록 (Push events 체크)
→ 이후 push만 하면 자동 재배포

5. AX Store 등록
유형: 웹앱 선택 (파일업로드 아님 — 파이썬 서버가 실행되어야 함)
앱 주소: Coolify 배포 주소
소스코드(선택): GitLab 저장소 링크 입력 권장
접근 권한 옵션이 있으면 홍보그룹으로 제한 권장
비용
Claude Sonnet 4.6 기준 공문 1건 파싱 약 20~30원, 월 1회 사용 시 월 300~500원 수준.
`app.py`의 `ALLOWED_MODEL`을 `claude-haiku-4-5-20251001`로 바꾸면 약 1/3로 절감.
로컬 테스트

```bash
pip install -r requirements.txt
set ANTHROPIC_API_KEY=sk-ant-...   # macOS/Linux: export
python app.py                       # → http://localhost:8080
```
