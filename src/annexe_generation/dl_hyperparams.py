
from dataclasses import asdict
import os
import sys
from typing import Dict, List

sys.path.append(os.path.abspath('..'))
from embedding_generation.data.hyperparams_transformers import get_transformers_hyperparams
from embedding_generation.data.hyperparams_word2vec import get_word2vec_hyperparams_instances

def has_unique_values(dict_list: List[Dict]) -> bool:
    """
    Check if each dictionary in the list has at least one value different from the others, ignoring the "index" keys.
    
    Args:
    dict_list (List[Dict]): A list of dictionaries to check.

    Returns:
    bool: True if each dictionary has at least one unique value, False otherwise.
    """
    for i in range(len(dict_list)):
        for j in range(i+1, len(dict_list)):
            # Compare dictionaries without the "index" key
            dict_i = {k: v for k, v in dict_list[i].items() if k != "index"}
            dict_j = {k: v for k, v in dict_list[j].items() if k != "index"}
            
            # Check if the dictionaries are the same
            if dict_i == dict_j:
                return False
    return True

def generate_latex_array(model_name: str, hyperparameters_instances: list):
    latex_str = ""
    num_instances = len(hyperparameters_instances)
    
    # Sort the instances based on their index
    hyperparameters_instances = sorted(hyperparameters_instances, key=lambda x: x['index'])
    
    # Extract the hyperparameter keys (excluding 'index') from the first instance
    keys = [key for key in hyperparameters_instances[0].keys() if key != 'index']

    for i in range(0, num_instances, 5):
        end = min(i + 5, num_instances)
        subset_instances = hyperparameters_instances[i:end]

        latex_str += "    \\begin{table}[ht]\n"
        latex_str += "        \\centering\n"
        latex_str += f"        \\caption{{{model_name} Hyperparameters (Configurations {subset_instances[0]['index']}–{subset_instances[-1]['index']})}}\n"
        latex_str += "        \\begin{tabular}{l" + "c" * len(subset_instances) + "}\n"
        
        # Print header
        latex_str += "            & " + " & ".join(f"Config {instance['index']}" for instance in subset_instances) + " \\\\\n"
        
        # Print hyperparameters
        for key in keys:
            latex_str += f"            {key.replace('_', ' ')} & " + " & ".join(str(instance[key]) for instance in subset_instances) + " \\\\\n"

        latex_str += "        \\end{tabular}\n"
        latex_str += "    \\end{table}\n\n"  # Two new lines for better readability

    return latex_str

transformers_instances = get_transformers_hyperparams()
word2vec_instances = get_word2vec_hyperparams_instances()

transformers_dicts = [asdict(instance) for instance in transformers_instances]
word2vec_dicts = [asdict(instance) for instance in word2vec_instances]

assert has_unique_values(transformers_dicts), "There are duplicate hyperparameter instances in the Transformers list."
assert has_unique_values(word2vec_dicts), "There are duplicate hyperparameter instances in the Word2Vec list."

transformers_latex = generate_latex_array("Transformers", transformers_dicts)
word2vec_latex = generate_latex_array("Word2Vec", word2vec_dicts)

print("\\subsection{Transformers:}")
print(transformers_latex)

print("\\subsection{Word2Vec:}")
print(word2vec_latex)
