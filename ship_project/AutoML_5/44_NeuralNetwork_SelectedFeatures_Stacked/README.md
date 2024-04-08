# Summary of 44_NeuralNetwork_SelectedFeatures_Stacked

[<< Go back](../README.md)


## Neural Network
- **n_jobs**: -1
- **dense_1_size**: 16
- **dense_2_size**: 16
- **learning_rate**: 0.01
- **explain_level**: 0

## Validation
 - **validation_type**: kfold
 - **k_folds**: 5
 - **shuffle**: True
 - **random_seed**: 42

## Optimized metric
mae

## Training time

71.0 seconds

### Metric details:
| Metric   |           Score |
|:---------|----------------:|
| MAE      |    53.9621      |
| MSE      | 19937.1         |
| RMSE     |   141.199       |
| R2       |     0.316666    |
| MAPE     |     5.23026e+15 |



## Learning curves
![Learning curves](learning_curves.png)
## True vs Predicted

![True vs Predicted](true_vs_predicted.png)


## Predicted vs Residuals

![Predicted vs Residuals](predicted_vs_residuals.png)



[<< Go back](../README.md)
