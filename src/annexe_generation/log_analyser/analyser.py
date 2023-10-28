import argparse
import os
import sys







sys.path.append(os.path.abspath('../..'))
from annexe_generation.log_analyser.clustering_analyser.extractor import clustering_extractor
from annexe_generation.log_analyser.common_extractor import extract_all_dataset_results
from annexe_generation.log_analyser.random_forest_analyser.extractor import random_forest_extractor
from annexe_generation.log_analyser.random_forest_analyser.classifier_data import ClassificationResults, plot_metrics

def read_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file]
            return lines
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read a file and print its contents.')
    parser.add_argument('file_path', type=str, help='Path to the file to be read')
    parser.add_argument('output', type=str, help='Path to the output directory')
    args = parser.parse_args()
    
    lines: list[str] = read_file(args.file_path)

    # extract the clustering results
    clustering_results = extract_all_dataset_results(lines, clustering_extractor)
    # print clustering results
    print(clustering_results)

    # extract classification results
    classification_results : list[ClassificationResults] =  extract_all_dataset_results(lines, random_forest_extractor)
    # print classification results
    for result in classification_results:
        latex_content = result.to_latex()

        output_file_path = f"{args.output}/{result.dataset_name}_random_forest_results.txt"
        with open(output_file_path, 'a') as output_file:
            output_file.write(latex_content + '\n\n')
    
    plot_metrics(classification_results, args.output)