

from commons.results.commons_results_writer import CommonResultsWriter
from research_base.utils.ml_utils.ml_evaluate import EVALUATE_RESULT_KEYS


class ResultsWriter(CommonResultsWriter):
    """
    This class is used to write the results of a classification pipeline to a CSV file.
    It keeps track of the headers of the CSV file and the results to write.
    It stores everything related to classification results.
    """
    ADDITIONAL_HEADERS: list[str] = [
        # data balancing results
        "data_balancing_duration",
        "nb_samples_before_balancing",
        "nb_samples_after_balancing",
    ]

    def __init__(self, pipeline_name: str):
        super().__init__(
            "/home/clement/Documents/github/phdtrack_openssh_memory_embedding/results/embedding_quality/result.csv", 
            self.ADDITIONAL_HEADERS + EVALUATE_RESULT_KEYS, 
            pipeline_name
        )