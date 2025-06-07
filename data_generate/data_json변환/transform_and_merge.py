#!/usr/bin/env python3
# transform_and_merge.py

import argparse
import json
import sys

def load_json(path, mode='r'):
    try:
        with open(path, mode, encoding='utf-8') as f:
            return json.load(f) if mode == 'r' else None
    except FileNotFoundError:
        print(f"Error: File not found '{path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding failed for '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def transform_records(records_jsonl):
    transformed = []
    for rec in records_jsonl:
        out = {
            'Question_Number': rec.get('Question_Number'),
            'Question_Description': rec.get('Question_Description'),
            'Answer': rec.get('Answer'),
            'Link': rec.get('Link'),
            'AnswerDescription': rec.get('Commentary'),
        }
        for key, val in rec.get('Selections', {}).items():
            out[key] = val.get('Select')
            out[f"{key}_Commentary"] = val.get('Commentary')
        transformed.append(out)
    return transformed

def merge_answers(transformed, question_list):
    qmap = {
        q['Question_Number']: {
            'Answer': q.get('Answer'),
            'Link': q.get('Link')
        }
        for q in question_list
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
        description="Transform JSONL and merge Answer/Link from question.json"
    )
    parser.add_argument('-i', '--input',
                        dest='input_file',
                        required=True,
                        help="입력 JSONL 파일 경로")
    parser.add_argument('-q', '--questions',
                        dest='question_file',
                        required=True,
                        help="매칭 기준 question.json 파일 경로")
    parser.add_argument('-o', '--output',
                        dest='output_file',
                        required=True,
                        help="출력 JSON 파일 경로")
    args = parser.parse_args()

    # Load and process
    raw_lines = []
    try:
        # JSONL load: read line by line
        with open(args.input_file, 'r', encoding='utf-8') as f:
            for line in f:
                raw_lines.append(json.loads(line))
    except Exception as e:
        print(f"Error reading input JSONL: {e}", file=sys.stderr)
        sys.exit(1)

    transformed = transform_records(raw_lines)
    questions = load_json(args.question_file)
    merged = merge_answers(transformed, questions)
    save_output(merged, args.output_file)

if __name__ == "__main__":
    main()
