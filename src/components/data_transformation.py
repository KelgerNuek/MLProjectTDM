import sys
import os
from dataclasses import dataclass

from src.exception import CustomException
from logger import logging

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_ob_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns=["writing_score","reading_score"]
            categorical_columns=[
                "gender",
                "race_ethinicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
                ]

            num_pipeline=Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ])
        
            cat_pipeline=Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="most_fequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler())
                ]
                )
            logging.info("Numerical Columns standard scalingcompleted")
            logging.info("Categorical Columns encoding completed")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns)
                ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
                )

            return preprocessor
        
        
        except Exception as e:
            raise CustomException(e,sys) 
        
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train & test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns=["writing_score","reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying the preprocessing object on training dataframe and testing dataframe"
            )

            input_feature_train_array=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array=preprocessing_obj.transform(input_feature_train_df)

            train_arr=np.c_[
                input_feature_train_array,np.array(target_feature_train_df)
            ]
            test_arr=np.c_[
                input_feature_test_array,np.array(target_feature_test_df)
            ]

            logging.info(f"Saved preprocessing object")

            save_object(

                file_path=self.data_transformation_config.preprocessor_ob_file_path,
                obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_ob_file_path,
            )

        except:
            pass