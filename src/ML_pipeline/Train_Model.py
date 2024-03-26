# Importing required packages
import pandas as pd
from neuralprophet import NeuralProphet
from sklearn.metrics import mean_absolute_percentage_error
from greykite.framework.templates.autogen.forecast_config import ForecastConfig
from greykite.framework.templates.forecaster import Forecaster
from greykite.framework.templates.model_templates import ModelTemplateEnum
from greykite.framework.templates.autogen.forecast_config import ModelComponentsParam

# Function to train silverkite model
def train_greykite(data, metadata, regressor_col):
    forecaster = Forecaster()
    result = forecaster.run_forecast_config(
        df=data.reset_index(),
        config=ForecastConfig(
            model_template=ModelTemplateEnum.SILVERKITE.name,
            forecast_horizon=20,  # forecasts 20 steps ahead
            coverage=0.95,  # 95% prediction intervals
            metadata_param=metadata,
            model_components_param=ModelComponentsParam(
                autoregression=None,
                regressors=regressor_col,
                events={
                    "holidays_to_model_separately": "auto",
                    "holiday_lookup_countries": ["UnitedStates"]
                },
                growth={
                    "growth_term": "linear"
                },
                changepoints={
                    "changepoints_dict": dict(
                        method="auto",
                        yearly_seasonality_order=10,
                        regularization_strength=0.5,
                        potential_changepoint_n=5,
                        yearly_seasonality_change_freq="365D",
                        no_changepoint_distance_from_end="365D"
                    )
                }
            )
        )
    )
    # Making evaluation dataframe and printing it
    evaluation_grekite_df= pd.DataFrame(result.forecast.compute_evaluation_metrics_split())
    print("evaluation matrix for fitted silverkite model \n ",evaluation_grekite_df)
    return result

# Function to train Neural Prophet model
def train_neural_prophet(data, future_reg):
    test_length = 20
    df_train = data.iloc[:-test_length]
    df_test = data.iloc[-test_length:]
    model = NeuralProphet(loss_func='MSE', n_changepoints=2, seasonality_mode='additive')
    for col in future_reg:
        model.add_future_regressor(col)
    metrics = model.fit(df_train, freq="W")
    future_df = model.make_future_dataframe(df_test, periods=test_length, n_historic_predictions=len(df_test),
                                            regressors_df=df_test)
    forecast = model.predict(future_df)
    print(f"Mean absolute percentage error for fitted NeuralProphet model is \t{mean_absolute_percentage_error(df_test['y'], forecast.iloc[-test_length:]['yhat1']):.4f}")
    return model

