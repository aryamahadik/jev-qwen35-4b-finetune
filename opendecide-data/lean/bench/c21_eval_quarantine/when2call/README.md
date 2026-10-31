---
license: cc-by-4.0
configs:
- config_name: test
  data_files:
  - split: llm_judge
    path: test/when2call_test_llm_judge.jsonl
  - split: mcq
    path: test/when2call_test_mcq.jsonl
  default: true
- config_name: train_sft
  data_files:
  - split: train
    path: train/when2call_train_sft.jsonl
- config_name: train_pref
  data_files:
  - split: train
    path: train/when2call_train_pref.jsonl
task_categories:
- text-generation
language:
- en
tags:
- function-calling
- tool-calling
- synthetic
- nvidia
---

# When2Call

<p align="center">
 💾 <a href="https://github.com/NVIDIA/When2Call">Github</a>&nbsp&nbsp | &nbsp&nbsp 📄 <a href="https://aclanthology.org/2025.naacl-long.174/">Paper</a>
</p>

## Dataset Description:

When2Call is a benchmark designed to evaluate tool-calling decision-making for large language models (LLMs), including when to generate a tool call, when to ask follow-up questions, when to admit the question can't be answered with the tools provided, and what to do if the question seems to require tool use but a tool call can't be made. 

We find that state-of-the-art tool-calling LMs show significant room for improvement on When2Call, indicating the importance of this benchmark. The dataset offers a training set for When2Call and leverages the multiple-choice nature of the benchmark to develop a preference optimization training regime, which shows considerable improvement over traditional fine-tuning for tool calling.

This dataset is ready for commercial use.

Evaluation code and the synthetic data generation scripts used to generate the datasets can be found in the [GitHub repo](https://github.com/NVIDIA/When2Call).

## Load Test/Train Data:

### Test data

The test set has two files: Multi-Choice Question evaluation (`mcq`) and LLM-as-a-judge (`llm_judge`), which is a subset of the MCQ evaluation set so you can download the two datasets as a single `DatasetDict`.

```python
>>> from datasets import load_dataset
>>> test_ds = load_dataset("nvidia/When2Call", "test")
>>> test_ds

DatasetDict({
    llm_judge: Dataset({
        features: ['uuid', 'source', 'source_id', 'question', 'correct_answer', 'answers', 'target_tool', 'tools', 'orig_tools', 'orig_question', 'held_out_param'],
        num_rows: 300
    })
    mcq: Dataset({
        features: ['uuid', 'source', 'source_id', 'question', 'correct_answer', 'answers', 'target_tool', 'tools', 'orig_tools', 'orig_question', 'held_out_param'],
        num_rows: 3652
    })
})
```

### Train data

When2Call has two training datasets available: one for Supervised Fine-Tuning (`train_sft`) and one for Preference Tuning such as DPO (`train_pref`). As `train_pref` has additional fields `chosen_response` and `rejected_response`, these datasets need to be loaded separately.

#### SFT

```python
>>> train_sft_ds = load_dataset("nvidia/When2Call", "train_sft")
>>> train_sft_ds
DatasetDict({
    train: Dataset({
        features: ['tools', 'messages'],
        num_rows: 15000
    })
```

#### Preference Tuning

```python
>>> train_pref_ds = load_dataset("nvidia/When2Call", "train_pref")
>>> train_pref_ds

DatasetDict({
    train: Dataset({
        features: ['tools', 'messages', 'chosen_response', 'rejected_response'],
        num_rows: 9000
    })
})
```

## Dataset Owner:

NVIDIA Corporation

## Dataset Creation Date:

September 2024

## License/Terms of Use: 

This dataset is licensed under a Creative Commons Attribution 4.0 International License available at https://creativecommons.org/licenses/by/4.0/legalcode.

## Intended Usage:

Evaluate and train LLMs’ tool-calling capabilities. 

## Dataset Characterization
** Data Collection Method<br>
* Synthetic <br>

** Labeling Method<br>
* Automated <br>

## Dataset Format
Text (.jsonl)

## Dataset Quantification

The training dataset contains examples consisting of tool specification(s), user input, multiple choices, and the expected response. The preference dataset includes chosen and rejected responses instead of expected responses. The test dataset follows the same format.
- Training set
    - SFT dataset: 15,000 examples
    - Preference dataset: 9,000 examples
-  Test set
    - MCQ dataset: 3,652 examples
    - LLM-as-a-judge dataset: 300 examples
Measurement of total data storage: 56MB

## References:

- [Hayley Ross, Ameya Sunil Mahabaleshwarka, Yoshi Suhara, “When2Call: When (not) to Call Tools”, NAACL 2025.](https://aclanthology.org/2025.naacl-long.174/)

## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.   

Please report security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).