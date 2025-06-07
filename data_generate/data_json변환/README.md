# JSONL to JSON & Merge Transformer Script

이 리포지토리는 `parsed_gpt_response.jsonl` 형식의 로그 파일을 읽어 `questions_fixed` 형태로 변환(transform)하고, `question.json` 파일의 `Question_Number` 기준으로 `Answer`와 `Link`를 병합(merge)하여 최종 JSON 파일을 생성하는 파이썬 스크립트를 포함합니다.

---

## 📝 기능 요약

1. **Transform**: `.jsonl` 파일을 파싱해 `questions_fixed` 포맷의 레코드로 변환
2. **Merge**: 기준이 되는 `question.json`의 `Question_Number`에 따라 각 레코드에 `Answer`와 `Link` 필드 추가
3. **Export**: 최종 결과를 하나의 JSON 파일로 저장

---

## 🚀 요구사항

* Python 3.6 이상

---

## 📦 설치 및 실행

1. 저장소 클론:

   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. (선택) 가상 환경 생성 및 활성화:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\\Scripts\\activate     # Windows
   ```

3. 스크립트 실행:

   ```bash
   python transform_and_merge.py \
     -i <input_file.jsonl> \
     -q <question_file.json> \
     -o <output_file.json>
   ```

---

## ⚙️ 옵션 설명

| 옵션            | 약칭   | 필수 여부 | 설명                           |
| ------------- | ---- | ----- | ---------------------------- |
| `--input`     | `-i` | 예     | 변환할 입력 `.jsonl` 파일 경로        |
| `--questions` | `-q` | 예     | 기준이 되는 `question.json` 파일 경로 |
| `--output`    | `-o` | 예     | 생성될 출력 `.json` 파일 경로         |

---

## 📖 사용 예시

```bash
python transform_and_merge.py \
  -i /mnt/data/parsed_gpt_response.jsonl \
  -q /mnt/data/question.json \
  -o /mnt/data/questions_fixed_complete.json
```

위 명령을 실행하면, 입력된 JSONL 파일을 변환하면서 `question.json`에서 `Answer`와 `Link`를 병합하여 `/mnt/data/questions_fixed_complete.json` 파일로 출력합니다.

---

## ⚠️ 에러 처리

* **입력 파일 없음**: 지정한 경로에 파일이 없으면 에러를 출력하고 종료
* **JSON 파싱 오류**: 잘못된 JSON 구조일 경우 오류를 출력하고 종료
* **출력 쓰기 오류**: 파일 쓰기 불가 시 오류를 출력하고 종료

---

## 🏷️ 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.
