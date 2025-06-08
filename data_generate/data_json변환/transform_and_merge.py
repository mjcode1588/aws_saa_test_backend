import argparse
import json
import sys

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found '{path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding failed for '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def transform_records(records_jsonl):
    """
    JSONL 레코드를 읽어 questions_fixed 포맷으로 변환.
    Domain, Tasks, Keywords, Terms 포함.
    """
    transformed = []
    for rec in records_jsonl:
        out = {
            'Question_Number': rec.get('Question_Number'),
            'Question_Description': rec.get('Question_Description'),
            'Answer': rec.get('Answer'),
            'Link': rec.get('Link'),
            'AnswerDescription': rec.get('Commentary'),
            'Domain': rec.get('Domain'),
            'Tasks': rec.get('Tasks'),
            'Keywords': rec.get('Keywords'),
            'Terms': rec.get('Terms'),
        }
        # Selections 플래트닝
        for key, val in rec.get('Selections', {}).items():
            out[key] = val.get('Select')
            out[f"{key}_Commentary"] = val.get('Commentary')
        transformed.append(out)
    return transformed

def merge_answers(transformed, question_list):
    """
    question.json의 Question_Number별로:
    - 'Answers' 필드가 리스트일 경우: ','.join
    - 'Answers' 필드가 문자열일 경우: 각 문자별로 ','.join
    - 그 외: 단일 'Answer' 사용
    """
    qmap = {}
    for q in question_list:
        qn = q.get('Question_Number')
        ans = q['Answer']
        if isinstance(ans, list):
            merged_ans = ','.join(str(a) for a in ans)
        elif isinstance(ans, str) and len(ans) > 1:
            merged_ans = ','.join(list(ans))
        else:
            merged_ans = ans
        qmap[qn] = {
            'Answer': merged_ans,
            'Link': q.get('Link')
        }

    for rec in transformed:
        qn = rec.get('Question_Number')
        if qn in qmap:
            rec['Answer'] = qmap[qn]['Answer']
            rec['Link']   = qmap[qn]['Link']
        else:
            print(f"Warning: Question_Number '{qn}' not found in question.json", file=sys.stderr)
    return transformed

def save_output(data, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f_out:
            json.dump(data, f_out, ensure_ascii=False, indent=2)
        print(f"Successfully generated: {output_path}")
    except IOError as e:
        print(f"Error writing output file '{output_path}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Transform JSONL and merge Answers(리스트/문자열) from question.json"
    )
    parser.add_argument('-i', '--input',
                        dest='input_file',
                        required=False,
                        help="입력 JSONL 파일 경로 (parsed_gpt_response.jsonl)")
    parser.add_argument('-q', '--questions',
                        dest='question_file',
                        required=False,
                        help="기준 question.json 파일 경로")
    parser.add_argument('-o', '--output',
                        dest='output_file',
                        required=False,
                        help="출력 JSON 파일 경로 (questions_fixed_complete.json)")
    args = parser.parse_args()


    # 1) JSONL 읽기
    raw_lines = []
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            for line in f:
                raw_lines.append(json.loads(line))
    except Exception as e:
        print(f"Error reading input JSONL: {e}", file=sys.stderr)
        sys.exit(1)

    # 2) 변환(transform)
    transformed = transform_records(raw_lines)

    # 3) question.json 로드 & Answers 병합
    questions = load_json(args.question_file)
    merged = merge_answers(transformed, questions)

    # 4) 출력 저장
    save_output(merged, args.output_file)

if __name__ == "__main__":
    import sys
    # 디버깅 세션(dbg)가 붙어있으면 기본 인자 세팅
    if sys.gettrace() and len(sys.argv) == 1:
        sys.argv += [
            "-i", "parsed_gpt_response.jsonl",
            "-q", "question.json",
            "-o", "questions_fixed_complete.json"
        ]
    main()
