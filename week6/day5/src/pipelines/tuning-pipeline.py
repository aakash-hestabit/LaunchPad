import src.training.tuning as tuning
import src.evaluation.shap_evaluation as evaluation

def run_tuning_pipeline():
    overall_best_name, overall_best_model = tuning.run_model_tuning()

    evaluation.run_evaluation(overall_best_name, overall_best_model)

if __name__ == "__main__":
    run_tuning_pipeline()