from sklearn.ensemble import RandomForestClassifier

from research_base.utils.ml_utils.ml_evaluate import evaluate
from commons.data_loading.data_types import SamplesAndLabels
from params.common_params import CommonProgramParams


def ml_random_forest_pipeline(
        params: CommonProgramParams, 
        samples_and_labels_train: SamplesAndLabels,
        samples_and_labels_test: SamplesAndLabels,
    ) -> None:
    """
    A pipeline for training a RandomForestClassifier.
    """
    # Train a RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=params.RANDOM_SEED, n_jobs = params.MAX_ML_WORKERS)
    clf.fit(samples_and_labels_train.sample, samples_and_labels_train.labels)
    
    # Evaluate model
    evaluate(
        clf,
        samples_and_labels_test.sample, # type: ignore
        samples_and_labels_test.labels, # type: ignore
        params.RESULTS_LOGGER,
        params.get_results_writer(),
    )
