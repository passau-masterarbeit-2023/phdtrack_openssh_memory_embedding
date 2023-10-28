from dataclasses import dataclass
from typing import Dict, Union

@dataclass
class ClassificationMetrics:
    precision: float
    recall: float
    f1_score: float
    support: float

    def to_latex(self, label: str):
        return f"{label} & {self.precision} & {self.recall} & {self.f1_score} & {self.support} \\\\ \\hline\n"


@dataclass
class ClassificationResults:
    dataset_path: str
    instance: str
    class_metrics: Dict[str, ClassificationMetrics]
    accuracy: float
    macro_avg: ClassificationMetrics
    weighted_avg: ClassificationMetrics
    true_positives: int
    true_negatives: int
    false_positives: int
    false_negatives: int
    auc: float
    duration: float  # Duration of the random forest operation in seconds

    @staticmethod
    def from_dict(d: dict, additional_metrics: dict, duration: float, dataset_path: str, instance: str) -> 'ClassificationResults':
        class_metrics = {key: ClassificationMetrics(**value) for key, value in d.items() if key not in {"accuracy", "macro avg", "weighted avg"}}
        macro_avg = ClassificationMetrics(**d["macro avg"])
        weighted_avg = ClassificationMetrics(**d["weighted avg"])
        accuracy = d.get("accuracy", 0.0)
        return ClassificationResults(dataset_path=dataset_path, instance=instance, class_metrics=class_metrics, 
                                     accuracy=accuracy, macro_avg=macro_avg, weighted_avg=weighted_avg, 
                                     duration=duration, **additional_metrics)
    

    def to_latex(self):
        latex_str = "\\begin{longtable}{|c|c|c|c|c|}\n"
        latex_str += "\\caption{" + self.instance + " Classification Results on " + self.dataset_path + "} \\label{tab:" + self.instance.lower().replace(" ", "_") + "_results} \\\\\n"
        latex_str += "\\hline\n"
        latex_str += "Metric & Precision & Recall & F1 Score & Support \\\\\n"
        latex_str += "\\hline\n"
        
        # Add class metrics
        for label, metrics in self.class_metrics.items():
            latex_str += metrics.to_latex(f"Class {label}")
        
        # Add macro average
        latex_str += self.macro_avg.to_latex("Macro Avg")
        
        # Add weighted average
        latex_str += self.weighted_avg.to_latex("Weighted Avg")
        
        # Add additional metrics
        additional_metrics = [
            ("Accuracy", self.accuracy),
            ("True Positives", self.true_positives),
            ("True Negatives", self.true_negatives),
            ("False Positives", self.false_positives),
            ("False Negatives", self.false_negatives),
            ("AUC", self.auc),
            ("Duration (seconds)", self.duration),
        ]
        for label, value in additional_metrics:
            latex_str += f"{label} & & & & {value} \\\\ \\hline\n"
        
        latex_str += "\\end{longtable}\n"
        return latex_str

