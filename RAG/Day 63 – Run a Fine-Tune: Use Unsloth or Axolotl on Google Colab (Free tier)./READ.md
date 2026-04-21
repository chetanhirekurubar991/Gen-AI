# Day 63 — Fine-Tuned Llama-3-8B with QLoRA

## What I did
- Loaded Llama-3-8B in 4-bit quantization using Unsloth on Google Colab free T4 GPU
- Configured LoRA (r=16, alpha=32) targeting attention projections
- Fine-tuned on 5 examples from Day 62 dataset
- Tested inference — model responded in correct format
- Saved adapters (adapter_model.safetensors + adapter_config.json)

## Key learnings
- 4-bit quantization reduces 16GB model to ~5GB
- LoRA only trains 0.52% of parameters (41M of 8B)
- Loss went from 1.864 → 1.758 (small drop due to tiny dataset)

## Stack
- Google Colab Free T4 GPU
- Unsloth 2026.3.17
- Llama-3-8B
- QLoRA (bitsandbytes)