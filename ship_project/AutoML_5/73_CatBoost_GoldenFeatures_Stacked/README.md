# Summary of 73_CatBoost_GoldenFeatures_Stacked

[<< Go back](../README.md)


## CatBoost
- **n_jobs**: -1
- **learning_rate**: 0.025
- **depth**: 9
- **rsm**: 0.8
- **loss_function**: MAPE
- **eval_metric**: MAE
- **explain_level**: 0

## Validation
 - **validation_type**: kfold
 - **k_folds**: 5
 - **shuffle**: True
 - **random_seed**: 42

## Optimized metric
mae

## Training time

286.6 seconds

### Metric details:
| Metric   |          Score |
|:---------|---------------:|
| MAE      |    45.7129     |
| MSE      | 25787.6        |
| RMSE     |   160.585      |
| R2       |     0.116144   |
| MAPE     |     4.1329e+12 |



## Learning curves
![Learning curves](learning_curves.png)
## True vs Predicted

![True vs Predicted](true_vs_predicted.png)


## Predicted vs Residuals

![Predicted vs Residuals](predicted_vs_residuals.png)



[<< Go back](../README.md)
