.env 파일을 생성후,

```
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

를 입력하면 

```
load_dotenv()

client = OpenAI()
```

에서 자동으로 API_KEY가 입력 됩니다.