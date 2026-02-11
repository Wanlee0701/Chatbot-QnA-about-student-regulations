import json
import time
from typing import Dict, Any
from dotenv import load_dotenv
import os
from openai import OpenAI

# =========================
# CONFIG
# =========================
INPUT_FILE = "C:\\Users\\PC\\Desktop\\Project2\\data\\sft_dataset_new\\sft_dataset.jsonl"
OUTPUT_FILE = "C:\\Users\\PC\\Desktop\\Project2\\data\\sft_dataset_new\\review_results.jsonl"
MODEL_NAME = "gpt-4o-mini"   # đổi nếu cần
SLEEP_TIME = 0.8             # tránh rate limit


# =========================
# PROMPT TEMPLATE
# =========================
JUDGE_PROMPT = """
Bạn là chuyên gia đánh giá chất lượng dữ liệu huấn luyện cho chatbot hỏi đáp quy chế sinh viên.

Nhiệm vụ của bạn là đánh giá MỘT mẫu dữ liệu SFT theo các tiêu chí dưới đây.

=== DỮ LIỆU CẦN ĐÁNH GIÁ ===
Instruction:
{instruction}

Input (Context):
{input}

Output (Answer):
{output}

=== TIÊU CHÍ ĐÁNH GIÁ ===
1. Answer có dựa trực tiếp vào nội dung trong Input hay không?
2. Answer có trích rõ Điều và Khoản hay không?
3. Answer có nhắc tới nguồn tài liệu (doc_type) với vai trò là căn cứ pháp lý hay không?
4. Answer có suy luận hoặc bổ sung thông tin không có trong Input hay không?
5. Trong trường hợp Input không đủ thông tin, Answer có nên từ chối trả lời không?

=== YÊU CẦU OUTPUT ===
Chỉ trả về MỘT đối tượng JSON, KHÔNG giải thích thêm, theo cấu trúc:

{{
  "pass": true | false,
  "issues": [danh sách ngắn gọn các lỗi nếu có],
  "should_be_refusal": true | false,
  "confidence": số từ 0 đến 1
}}

""".strip()


# =========================
# CALL LLM (PLACEHOLDER)
# =========================
def call_llm(prompt: str) -> Dict[str, Any]:
    load_dotenv(override=True)
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY','your_api_key')
    client = OpenAI()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Bạn chỉ trả JSON hợp lệ."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "pass": False,
            "issues": ["Judge output không phải JSON hợp lệ"],
            "should_be_refusal": False,
            "confidence": 0.0
        }


# =========================
# MAIN REVIEW LOOP
# =========================
def review_dataset():
    total = 0
    passed = 0
    failed = 0
    refusal = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as fout:

        for idx, line in enumerate(fin, start=1):
            sample = json.loads(line)
            total += 1

            sample_id = sample.get("id", idx)

            prompt = JUDGE_PROMPT.format(
                instruction=sample.get("instruction", ""),
                input=sample.get("input", ""),
                output=sample.get("output", "")
            )

            review = call_llm(prompt)

            result = {
                "id": sample_id,
                "pass": review.get("pass", False),
                "issues": review.get("issues", []),
                "should_be_refusal": review.get("should_be_refusal", False),
                "confidence": review.get("confidence", 0.0)
            }

            if result["pass"]:
                passed += 1
            else:
                failed += 1

            if result["should_be_refusal"]:
                refusal += 1

            fout.write(json.dumps(result, ensure_ascii=False) + "\n")

            time.sleep(SLEEP_TIME)

    print("=== REVIEW SUMMARY ===")
    print(f"Total samples      : {total}")
    print(f"Passed             : {passed}")
    print(f"Failed             : {failed}")
    print(f"Should be refusal  : {refusal}")
    print(f"Pass rate          : {passed / total:.2%}")


if __name__ == "__main__":
    review_dataset()
