# Summary of 68_NeuralNetwork_SelectedFeatures_Stacked

[<< Go back](../README.md)


## Neural Network
- **n_jobs**: -1
- **dense_1_size**: 32
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

109.9 seconds

### Metric details:
| Metric   |           Score |
|:---------|----------------:|
| MAE      |    55.4351      |
| MSE      | 20218.2         |
| RMSE     |   142.191       |
| R2       |     0.307031    |
| MAPE     |     8.89348e+15 |



## Learning curves
![Learning curves](learning_curves.png)
## True vs Predicted

![True vs Predicted](true_vs_predicted.png)


## Predicted vs Residuals

![Predicted vs Residuals](predicted_vs_residuals.png)



[<< Go back](../README.md)
