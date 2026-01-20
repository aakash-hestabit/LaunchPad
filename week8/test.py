from vllm import LLM, SamplingParams

def main():
    llm = LLM(
        model="quantized/merged_model",
        enforce_eager=True,
        disable_log_stats=True,
    )

    params = SamplingParams(max_tokens=100)

    out = llm.generate(["Hello, who are you?"], params)

    print(out[0].outputs[0].text)


if __name__ == "__main__":
    main()
