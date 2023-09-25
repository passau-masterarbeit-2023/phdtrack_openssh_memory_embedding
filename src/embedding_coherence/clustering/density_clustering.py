

from sklearn.cluster import DBSCAN, OPTICS
from sklearn.discriminant_analysis import StandardScaler
from sklearn.metrics import pairwise_distances, silhouette_score
import numpy as np
import pandas as pd
from research_base.utils.results_utils import time_measure_result

from commons.data_loading.data_types import SamplesAndLabels

from embedding_coherence.params.params import ProgramParams

# $ python main_value_node.py -p ds_density_clustering -otr testing -b undersampling -d load_data_structure_dataset

def density_clustering_pipeline(
        params : ProgramParams,
        samples_and_sample_str_train: SamplesAndLabels,
) -> None:
    """
    Density clustering pipeline.
    """
    # Split data into training and test sets
    samples_train, _ = samples_and_sample_str_train.sample, samples_and_sample_str_train.labels
    #samples_test, _ = samples_and_sample_str_test # not working, need to split data into training if no testing data is provided

    # Track best silhouette score, best eps and the corresponding labels
    best_score = -1
    best_eps = None
    best_n_clusters = None
    best_labels = None

    # Scale data (required for DBSCAN)
    with time_measure_result(
            f'scaling_duration', 
            params.RESULTS_LOGGER, 
            params.get_results_writer(),
            "scaling_duration"
        ):
        # But not for cosine similarity
        #scaler = StandardScaler()
        #df_scaled = pd.DataFrame(scaler.fit_transform(samples_train), columns=samples_train.columns).astype('float32')
        df_scaled = samples_train.iloc[:20000].astype('float32')
        print(f"df_scaled: {df_scaled.shape}")
    # precompute cosine similarity matrix
    # reduce memory usage and save time (avoid to compute the same cosine similarity multiple times)
    # too much memory usage for large datasets : 84to
    #with time_measure_result(
    #        f'distance_matrix_computation', 
    #        params.RESULTS_LOGGER, 
    #        params.get_results_writer(),
    #        "distance_matrix_computation_time"
    #    ):
    #    distance_matrix = pairwise_distances(df_scaled, metric="cosine")

    # Define the range of eps values we want to try
    #eps_values = np.linspace(0.5, 0.9, num=2)  # customize as necessary
    eps_values = [0.6]

    for eps in eps_values:
        # density clustering
        #dbscan = DBSCAN(
        #    eps=eps, 
        #    min_samples=50, 
        #    metric='cosine', 
        #    algorithm='ball_tree', 
        #    n_jobs=params.MAX_ML_WORKERS,
        #)  # customize min_samples as necessary
        #dbscan.fit(df_scaled)

        optics = OPTICS(min_samples=50, metric='cosine', n_jobs=params.MAX_ML_WORKERS, algorithm='brute', cluster_method="xi")
        
        with np.errstate(divide='ignore'): # ignore divide by zero warning
            optics.fit_predict(df_scaled)

        # Get labels for training set
        labels = optics.labels_

        # Number of clusters, ignoring noise if present
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        # Calculate silhouette score if there's more than one cluster
        if n_clusters > 1:
            score = silhouette_score(df_scaled, labels)
            print(f"eps: {eps}, number of clusters: {n_clusters}, silhouette score: {score}")

            if score > best_score:
                best_score = score
                best_eps = eps
                best_n_clusters = n_clusters
                best_labels = labels
        else:
            print(f"WARN: n_clusters <= 1 !!! eps: {eps}, number of clusters: {n_clusters}")

    # check that we found a good eps value
    if best_eps is None:
        raise Exception("No good eps value found")

    n_noise = np.sum(best_labels == -1)
    print(f"Best eps: {best_eps}, number of clusters: {best_n_clusters}, silhouette score: {best_score}, noise points: {n_noise}")

