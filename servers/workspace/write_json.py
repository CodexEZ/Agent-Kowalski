
import json

data_to_save = [
    {
        "_id": "68a6efe95be39351e91d808a",
        "content_summary": {
            "how_to_use": {
                "attention_overflow_issue": "Known to have an attention overflow issue with FP16; suggests enabling/disabling autocast on `PhiAttention.forward()` function if facing this issue.",
                "integration": "Integrated into `transformers` version 4.37.0 and higher."
            },
            "intended_uses": {
                "best_suited_for": "Prompts using QA format, chat format, and code format.",
                "caution": "Model-generated text/code should be treated as a starting point, not definitive solutions. Users should be cautious and evaluate before direct adoption for production tasks.",
                "chat_format": "Example of a multi-turn conversation.",
                "code_format": "Example of generating code after comments.",
                "qa_format": "Examples provided for standalone questions and \"Instruct: <prompt>\\nOutput:\" format."
            },
            "license": "MIT license.",
            "limitations_of_phi_2": {
                "inaccurate_code_and_facts": "May produce incorrect code snippets and statements.",
                "language_limitations": "Primarily designed for standard English; informal English, slang, or other languages may pose challenges.",
                "limited_scope_for_code": "Primarily trained on Python with common packages. Users should verify code using other packages or languages.",
                "potential_societal_biases": "Not entirely free from societal biases; may generate content reflecting these biases if prompted.",
                "toxicity": "Can produce harmful content if explicitly prompted. Released to help the open-source community develop methods to reduce toxicity directly after pretraining.",
                "unreliable_responses_to_instruction": "Has not undergone instruction fine-tuning, may struggle with intricate or nuanced instructions.",
                "verbosity": "Being a base model, it often produces irrelevant or extra text/responses due to its textbook-like training data."
            },
            "model_summary": {
                "fine_tuning": "Not fine-tuned through reinforcement learning from human feedback.",
                "name": "Phi-2",
                "parameters": "2.7 billion",
                "performance": "Nearly state-of-the-art among models under 13 billion parameters in common sense, language understanding, and logical reasoning benchmarks.",
                "purpose": "To provide the research community with a non-restricted small model to explore safety challenges (reducing toxicity, understanding societal biases, enhancing controllability, etc.).",
                "training_data": "Same as Phi-1.5, augmented with new NLP synthetic texts and filtered websites (for safety and educational value)."
            },
            "trademarks": "Mentions Microsoft\'s Trademark & Brand Guidelines and third-party policies.",
            "training_model_software": {
                "architecture": "Transformer-based with next-word prediction objective.",
                "context_length": "2048 tokens.",
                "dataset_size": "250B tokens (NLP synthetic data by AOAI GPT-3.5 and filtered web data from Falcon RefinedWeb and SlimPajama, assessed by AOAI GPT-4).",
                "gpus": "96x A100-80G.",
                "software": "PyTorch, DeepSpeed, Flash-Attention.",
                "training_time": "14 days.",
                "training_tokens": "1.4T tokens."
            }
        },
        "source": "Hugging Face",
        "url": "https://huggingface.co/microsoft/phi-2"
    },
    {
        "_id": "68a6f0375be39351e91d808b",
        "summary": "Qwen-Image-Edit is an image editing version of the 20B Qwen-Image model. It extends text rendering capabilities to image editing, enabling precise text editing. It also incorporates Qwen2.5-VL for visual semantic control and VAE Encoder for visual appearance control, achieving capabilities in both semantic and appearance editing. Key features include semantic and appearance editing, precise bilingual text editing, and strong benchmark performance, achieving state-of-the-art results. It can be used with the `diffusers` library and is showcased with various examples like character consistency, object rotation, style transfer, element addition/removal, and accurate text editing. The model is licensed under Apache 2.0.",
        "url": "https://huggingface.co/Qwen/Qwen-Image-Edit"
    }
]

json_output = json.dumps(data_to_save, indent=4)

with open("web_data.json", "w") as f:
    f.write(json_output)

print("Data successfully written to web_data.json")
